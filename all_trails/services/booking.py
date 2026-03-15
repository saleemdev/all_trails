from __future__ import annotations

from typing import Any

import frappe
from frappe import _
from frappe.utils import cint, cstr, flt, now_datetime

from all_trails.payments import (
	PAYMENT_STATUS_CANCELLED,
	PAYMENT_STATUS_FAILED,
	PAYMENT_STATUS_PAID,
	PAYMENT_STATUS_PROMPT_SENT,
	PAYMENT_STATUS_TIMEOUT,
	get_mpesa_payment_status,
	initiate_mpesa_payment,
)
from all_trails.services.common import (
	append_status_log,
	ensure_authenticated_user,
	log_illegal_transition,
	parse_json_input,
)


BOOKING_STATUS_PENDING = "Pending"
BOOKING_STATUS_CONFIRMED = "Confirmed"
BOOKING_STATUS_CANCELLED = "Cancelled"
BOOKING_STATUS_COMPLETED = "Completed"

BOOKING_ALLOWED_TRANSITIONS = {
	BOOKING_STATUS_PENDING: {BOOKING_STATUS_CONFIRMED, BOOKING_STATUS_CANCELLED},
	BOOKING_STATUS_CONFIRMED: {BOOKING_STATUS_COMPLETED, BOOKING_STATUS_CANCELLED},
	BOOKING_STATUS_CANCELLED: set(),
	BOOKING_STATUS_COMPLETED: set(),
}


PAYMENT_FAILURE_STATUSES = {
	PAYMENT_STATUS_FAILED,
	PAYMENT_STATUS_CANCELLED,
	PAYMENT_STATUS_TIMEOUT,
}



def _normalize_selected_activities(selected_activities: Any) -> list[dict[str, Any]]:
	parsed = parse_json_input(selected_activities, [])
	if not isinstance(parsed, list):
		return []

	normalized: list[dict[str, Any]] = []
	for row in parsed:
		if not isinstance(row, dict):
			continue
		activity_id = cstr(row.get("activity_id") or row.get("id")).strip()
		quantity = cint(row.get("quantity") or 0)
		if not activity_id or quantity <= 0:
			continue
		normalized.append(
			{
				"activity_id": activity_id,
				"quantity": quantity,
			}
		)
	return normalized



def _get_booking_activities(booking_name: str) -> list[dict[str, Any]]:
	rows = frappe.get_all(
		"Trail Booking Activity",
		filters={
			"parent": booking_name,
			"parenttype": "Trail Booking",
			"parentfield": "selected_activities",
		},
		fields=["activity_id", "activity_name", "quantity", "unit_price", "total_price"],
		order_by="idx asc",
	)

	return [
		{
			"activity_id": row.activity_id,
			"activity_name": row.activity_name,
			"quantity": cint(row.quantity),
			"price": flt(row.unit_price),
			"total_price": flt(row.total_price),
		}
		for row in rows
	]



def serialize_booking(booking: dict[str, Any] | frappe.model.document.Document) -> dict[str, Any]:
	if hasattr(booking, "as_dict"):
		row = booking  # type: ignore[assignment]
		name = row.name
	else:
		row = booking
		name = row.get("name")

	if not name:
		frappe.throw(_("Booking not found"))

	result = {
		"id": name,
		"name": name,
		"user": row.user,
		"trail_id": row.trail,
		"trail_title": row.trail_title,
		"trail_location": row.trail_location,
		"trail_scheduled_date": row.trail_scheduled_date,
		"booking_date": row.booking_date,
		"status": row.status,
		"spots_booked": cint(row.spots_booked),
		"base_price": flt(row.base_price),
		"activities_price": flt(row.activities_price),
		"total_price": flt(row.total_price),
		"currency": row.currency,
		"payment_status": row.payment_status,
		"payment": row.payment,
		"payment_ticket": row.payment_ticket,
		"payment_method": row.payment_method,
		"payment_attempt_count": cint(row.payment_attempt_count),
		"last_payment_attempt_on": row.last_payment_attempt_on,
		"mpesa_phone_number": row.mpesa_phone_number,
		"mpesa_receipt_number": row.mpesa_receipt_number,
		"mpesa_transaction_id": row.mpesa_transaction_id,
		"confirmation_code": row.confirmation_code,
		"cancellation_reason": row.cancellation_reason,
		"cancellation_date": row.cancelled_on,
		"completed_on": row.completed_on,
		"created_at": row.creation,
		"updated_at": row.modified,
		"selected_activities": _get_booking_activities(name),
	}
	return result



def _enforce_booking_owner(booking) -> None:
	if frappe.session.user == "Administrator":
		return
	if booking.user != frappe.session.user:
		frappe.throw(_("You are not allowed to access this booking"), frappe.PermissionError)



def _transition_booking_status(
	booking,
	new_status: str,
	*,
	context: dict[str, Any],
	strict: bool,
) -> bool:
	current = cstr(booking.status or BOOKING_STATUS_PENDING)
	if current == new_status:
		return True

	allowed = BOOKING_ALLOWED_TRANSITIONS.get(current, set())
	if new_status not in allowed:
		log_illegal_transition("Booking", booking.name, current, new_status, context)
		if strict:
			frappe.throw(
				_("Illegal booking status transition from {0} to {1}").format(current, new_status),
				frappe.ValidationError,
			)
		return False

	booking.status = new_status
	booking.status_log = append_status_log(
		booking.status_log,
		f"Status changed from {current} to {new_status}",
	)
	return True



def _set_booking_payment_fields_from_payment(booking, payment) -> None:
	booking.payment = payment.name
	booking.payment_status = payment.status
	booking.payment_ticket = payment.mpesa_ticket
	booking.mpesa_phone_number = payment.phone_number
	booking.payment_attempt_count = cint(payment.current_attempt_no)
	booking.last_payment_attempt_on = payment.last_attempted_on

	if payment.status == PAYMENT_STATUS_PAID:
		booking.payment_status = PAYMENT_STATUS_PAID
		booking.mpesa_receipt_number = payment.receipt_number
		booking.mpesa_transaction_id = payment.provider_transaction_id



def sync_booking_payment_state_from_payment(
	*,
	payment,
	status: str | None = None,
	context: dict[str, Any] | None = None,
) -> None:
	if payment.reference_doctype != "Trail Booking" or not payment.reference_name:
		return

	if not frappe.db.exists("Trail Booking", payment.reference_name):
		return

	context = context or {}
	booking = frappe.get_doc("Trail Booking", payment.reference_name, for_update=True)
	target_payment_status = status or payment.status

	_set_booking_payment_fields_from_payment(booking, payment)
	booking.payment_status = target_payment_status

	if target_payment_status == PAYMENT_STATUS_PAID:
		_transition_booking_status(
			booking,
			BOOKING_STATUS_CONFIRMED,
			context={"reason": "payment_success", **context},
			strict=False,
		)
	elif target_payment_status in PAYMENT_FAILURE_STATUSES:
		# Keep booking pending on payment failures, unless already progressed.
		if booking.status == BOOKING_STATUS_PENDING:
			booking.status = BOOKING_STATUS_PENDING

	booking.status_log = append_status_log(
		booking.status_log,
		f"Payment status synced to {target_payment_status}",
	)
	booking.flags.ignore_permissions = True
	booking.save(ignore_permissions=True)



def _generate_confirmation_code() -> str:
	for _ in range(6):
		candidate = f"AT-{frappe.generate_hash(length=8).upper()}"
		if not frappe.db.exists("Trail Booking", {"confirmation_code": candidate}):
			return candidate
	frappe.throw(_("Could not generate confirmation code"))



def _load_trail_for_booking(trail_id: str):
	if not frappe.db.exists("Trail", trail_id):
		frappe.throw(_("Trail not found"))

	trail = frappe.get_doc("Trail", trail_id, for_update=True)
	if cint(trail.published) != 1 or trail.status != "Active":
		frappe.throw(_("Trail is not available for booking"))

	frappe.db.sql(
		"""
			select name
			from `tabTrail Activity`
			where parent = %s and parenttype = 'Trail' and parentfield = 'activities'
			for update
		""",
		trail_id,
	)
	return trail



def create_booking(
	trail_id: str,
	spots_booked: int,
	selected_activities: list[dict[str, Any]] | str | None = None,
	idempotency_key: str | None = None,
):
	user = ensure_authenticated_user()
	spots = cint(spots_booked)
	if spots <= 0:
		frappe.throw(_("Spots booked must be greater than zero"))

	idempotency_key = cstr(idempotency_key or "").strip()
	if not idempotency_key:
		frappe.throw(_("idempotency_key is required"))

	existing = frappe.db.get_value(
		"Trail Booking",
		{"user": user, "idempotency_key": idempotency_key},
		"name",
	)
	if existing:
		return get_booking_detail(existing)

	activities = _normalize_selected_activities(selected_activities)

	save_point = f"all_trails_booking_create_{frappe.generate_hash(length=8)}"
	frappe.db.savepoint(save_point)
	try:
		existing = frappe.db.get_value(
			"Trail Booking",
			{"user": user, "idempotency_key": idempotency_key},
			"name",
		)
		if existing:
			frappe.db.rollback(save_point=save_point)
			return get_booking_detail(existing)

		trail = _load_trail_for_booking(trail_id)
		if cint(trail.available_spots) < spots:
			frappe.throw(
				_("Only {0} spot(s) left on this trail").format(cint(trail.available_spots)),
			)

		activity_rows = {row.name: row for row in trail.activities}
		activities_payload: list[dict[str, Any]] = []
		activities_total = 0.0

		for item in activities:
			activity_id = item["activity_id"]
			quantity = cint(item["quantity"])
			if quantity <= 0:
				continue

			if activity_id not in activity_rows:
				frappe.throw(_("Selected activity is no longer available"))

			activity = activity_rows[activity_id]
			if cint(activity.available) != 1:
				frappe.throw(_("Activity {0} is unavailable").format(activity.activity_name))

			if activity.available_spots is not None and cint(activity.available_spots) < quantity:
				frappe.throw(
					_("Not enough spots available for activity {0}").format(activity.activity_name)
				)

			if activity.max_participants is not None and cint(activity.max_participants) > 0:
				if quantity > cint(activity.max_participants):
					frappe.throw(
						_("Activity {0} exceeds max participants").format(activity.activity_name)
					)

			unit_price = flt(activity.price_kshs)
			total_price = unit_price * quantity
			activities_total += total_price
			activities_payload.append(
				{
					"activity_id": activity.name,
					"activity_name": activity.activity_name,
					"quantity": quantity,
					"unit_price": unit_price,
					"total_price": total_price,
				}
			)

			if activity.available_spots is not None:
				activity.available_spots = cint(activity.available_spots) - quantity

		base_price = flt(trail.price_kshs) * spots
		total_price = base_price + activities_total

		booking = frappe.get_doc(
			{
				"doctype": "Trail Booking",
				"trail": trail.name,
				"user": user,
				"member": frappe.db.get_value("Member", {"user": user}, "name"),
				"booking_date": now_datetime(),
				"status": BOOKING_STATUS_PENDING,
				"spots_booked": spots,
				"base_price": base_price,
				"activities_price": activities_total,
				"total_price": total_price,
				"currency": "KES",
				"payment_status": "Pending",
				"payment_method": "MPESA",
				"confirmation_code": _generate_confirmation_code(),
				"idempotency_key": idempotency_key,
				"trail_title": trail.title,
				"trail_location": trail.location,
				"trail_scheduled_date": trail.scheduled_date,
			}
		)

		for activity_item in activities_payload:
			booking.append("selected_activities", activity_item)

		booking.status_log = append_status_log("", "Booking created")
		booking.insert(ignore_permissions=True)

		trail.available_spots = cint(trail.available_spots) - spots
		trail.flags.ignore_permissions = True
		trail.save(ignore_permissions=True)

		frappe.db.commit()
		return serialize_booking(booking)
	except Exception:
		frappe.db.rollback(save_point=save_point)
		raise



def get_user_bookings(status: str | None = None):
	user = ensure_authenticated_user()
	filters: dict[str, Any] = {"user": user}
	if status:
		filters["status"] = status

	rows = frappe.get_all(
		"Trail Booking",
		filters=filters,
		fields=["name"],
		order_by="creation desc",
	)
	bookings: list[dict[str, Any]] = []
	for row in rows:
		bookings.append(get_booking_detail(row.name))
	return bookings



def get_booking_detail(booking_id: str):
	if not booking_id:
		frappe.throw(_("Booking ID is required"))
	if not frappe.db.exists("Trail Booking", booking_id):
		frappe.throw(_("Booking not found"))

	booking = frappe.get_doc("Trail Booking", booking_id)
	_enforce_booking_owner(booking)
	return serialize_booking(booking)



def cancel_booking(booking_id: str, reason: str | None = None):
	ensure_authenticated_user()
	if not booking_id:
		frappe.throw(_("Booking ID is required"))

	save_point = f"all_trails_booking_cancel_{frappe.generate_hash(length=8)}"
	frappe.db.savepoint(save_point)
	try:
		booking = frappe.get_doc("Trail Booking", booking_id, for_update=True)
		_enforce_booking_owner(booking)

		_transition_booking_status(
			booking,
			BOOKING_STATUS_CANCELLED,
			context={"reason": "user_cancel"},
			strict=True,
		)

		trail = _load_trail_for_booking(booking.trail)
		trail.available_spots = min(
			cint(trail.max_capacity),
			cint(trail.available_spots) + cint(booking.spots_booked),
		)

		activity_rows = {row.name: row for row in trail.activities}
		for item in booking.selected_activities:
			if item.activity_id in activity_rows and activity_rows[item.activity_id].available_spots is not None:
				activity_rows[item.activity_id].available_spots = cint(activity_rows[item.activity_id].available_spots) + cint(
					item.quantity
				)

		trail.flags.ignore_permissions = True
		trail.save(ignore_permissions=True)

		booking.cancelled_on = now_datetime()
		booking.cancellation_reason = cstr(reason or "").strip() or booking.cancellation_reason
		booking.status_log = append_status_log(
			booking.status_log,
			f"Booking cancelled by user {frappe.session.user}",
		)
		booking.flags.ignore_permissions = True
		booking.save(ignore_permissions=True)

		frappe.db.commit()
		return {"success": True, "booking": serialize_booking(booking)}
	except Exception:
		frappe.db.rollback(save_point=save_point)
		raise



def initiate_booking_payment(
	booking_id: str,
	phone_number: str,
	idempotency_key: str | None = None,
):
	ensure_authenticated_user()
	if not booking_id:
		frappe.throw(_("Booking ID is required"))
	if not phone_number:
		frappe.throw(_("Phone number is required"))

	idempotency_key = cstr(idempotency_key or "").strip()
	if not idempotency_key:
		frappe.throw(_("idempotency_key is required"))

	booking = frappe.get_doc("Trail Booking", booking_id)
	_enforce_booking_owner(booking)

	if booking.status in {BOOKING_STATUS_CANCELLED, BOOKING_STATUS_COMPLETED}:
		frappe.throw(_("This booking cannot be paid in its current status"))

	if booking.payment and frappe.db.exists("All Trails Payment", booking.payment):
		existing_payment_status = frappe.db.get_value("All Trails Payment", booking.payment, "status")
		if existing_payment_status == PAYMENT_STATUS_PAID:
			payment_state = get_mpesa_payment_status(payment_id=booking.payment)
			return {
				"success": True,
				"message": _("Payment already completed"),
				"booking": get_booking_detail(booking_id),
				"payment": payment_state,
			}

	payment_response = initiate_mpesa_payment(
		reference_name=booking.name,
		phone_number=phone_number,
		amount=booking.total_price,
		journey_type="Trail Booking",
		reference_doctype="Trail Booking",
		metadata={
			"trail_id": booking.trail,
			"confirmation_code": booking.confirmation_code,
		},
		payment_id=booking.payment,
		reuse_existing=True,
		idempotency_key=idempotency_key,
	)

	payment_id = payment_response.get("payment_id")
	if payment_id and frappe.db.exists("All Trails Payment", payment_id):
		payment_doc = frappe.get_doc("All Trails Payment", payment_id)
		sync_booking_payment_state_from_payment(
			payment=payment_doc,
			status=payment_doc.status,
			context={"reason": "initiate_payment"},
		)
		frappe.db.commit()

	return {
		**payment_response,
		"booking": get_booking_detail(booking_id),
	}



def get_booking_payment_status(booking_id: str):
	ensure_authenticated_user()
	booking = frappe.get_doc("Trail Booking", booking_id)
	_enforce_booking_owner(booking)

	if not booking.payment:
		return {
			"booking": serialize_booking(booking),
			"payment": {
				"status": booking.payment_status,
				"paid": booking.payment_status == PAYMENT_STATUS_PAID,
				"failed": booking.payment_status in PAYMENT_FAILURE_STATUSES,
				"message": booking.payment_status,
			},
		}

	payment_state = get_mpesa_payment_status(payment_id=booking.payment)
	payment_doc = frappe.get_doc("All Trails Payment", booking.payment)
	sync_booking_payment_state_from_payment(
		payment=payment_doc,
		status=payment_state.get("status"),
		context={"reason": "poll_payment_status"},
	)
	frappe.db.commit()

	return {
		"booking": get_booking_detail(booking_id),
		"payment": payment_state,
	}
