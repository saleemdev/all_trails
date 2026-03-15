from __future__ import annotations

import json
from contextlib import contextmanager
from typing import Any

import frappe
from frappe import _
from frappe.utils import cint, cstr, flt, get_url, getdate, now_datetime, today

from mpesa_tx.api import mpesa_handler

from all_trails.services.common import log_illegal_transition


PAYMENT_STATUS_PENDING = "Pending"
PAYMENT_STATUS_PROMPT_SENT = "Prompt Sent"
PAYMENT_STATUS_CALLBACK_RECEIVED = "Callback Received"
PAYMENT_STATUS_PAID = "Paid"
PAYMENT_STATUS_FAILED = "Failed"
PAYMENT_STATUS_CANCELLED = "Cancelled"
PAYMENT_STATUS_TIMEOUT = "Timeout"

TERMINAL_PAYMENT_STATUSES = {
	PAYMENT_STATUS_PAID,
	PAYMENT_STATUS_FAILED,
	PAYMENT_STATUS_CANCELLED,
	PAYMENT_STATUS_TIMEOUT,
}

PAYMENT_ALLOWED_TRANSITIONS = {
	PAYMENT_STATUS_PENDING: {
		PAYMENT_STATUS_PROMPT_SENT,
		PAYMENT_STATUS_CALLBACK_RECEIVED,
		PAYMENT_STATUS_PAID,
		PAYMENT_STATUS_FAILED,
		PAYMENT_STATUS_CANCELLED,
		PAYMENT_STATUS_TIMEOUT,
	},
	PAYMENT_STATUS_PROMPT_SENT: {
		PAYMENT_STATUS_CALLBACK_RECEIVED,
		PAYMENT_STATUS_PAID,
		PAYMENT_STATUS_FAILED,
		PAYMENT_STATUS_CANCELLED,
		PAYMENT_STATUS_TIMEOUT,
	},
	PAYMENT_STATUS_CALLBACK_RECEIVED: {
		PAYMENT_STATUS_PAID,
		PAYMENT_STATUS_FAILED,
		PAYMENT_STATUS_CANCELLED,
		PAYMENT_STATUS_TIMEOUT,
	},
	PAYMENT_STATUS_FAILED: {PAYMENT_STATUS_PENDING, PAYMENT_STATUS_PROMPT_SENT},
	PAYMENT_STATUS_CANCELLED: {PAYMENT_STATUS_PENDING, PAYMENT_STATUS_PROMPT_SENT},
	PAYMENT_STATUS_TIMEOUT: {PAYMENT_STATUS_PENDING, PAYMENT_STATUS_PROMPT_SENT},
	PAYMENT_STATUS_PAID: set(),
}

TICKET_STATUS_REQUESTED = "Requested"
TICKET_STATUS_COMPLETED = "Completed"
TICKET_STATUS_FAILED = "Failed"



def initiate_mpesa_payment(
	reference_name: str | None = None,
	phone_number: str | None = None,
	amount: float | str | None = None,
	journey_type: str | None = None,
	reference_doctype: str | None = None,
	company: str | None = None,
	metadata: str | dict[str, Any] | None = None,
	payment_id: str | None = None,
	reuse_existing: bool | str | int = False,
	idempotency_key: str | None = None,
	**kwargs,
) -> dict[str, Any]:
	request = _build_payment_request(
		reference_name=reference_name,
		phone_number=phone_number,
		amount=amount,
		journey_type=journey_type,
		reference_doctype=reference_doctype,
		company=company,
		metadata=metadata,
		kwargs=kwargs,
	)

	payment = _resolve_or_create_payment(
		request,
		payment_id=payment_id,
		reuse_existing=bool(cint(reuse_existing)),
	)
	_authorize_payment_write(payment)

	ticket = _get_or_create_mpesa_ticket(payment, request)
	callback_url = _ensure_mpesa_callback_url(ticket.business_short_code)

	idempotency_key = cstr(idempotency_key or kwargs.get("idempotency_key") or "").strip() or None
	if idempotency_key:
		existing_attempt = _find_attempt_by_idempotency(payment, idempotency_key)
		if existing_attempt and payment.status in {
			PAYMENT_STATUS_PENDING,
			PAYMENT_STATUS_PROMPT_SENT,
			PAYMENT_STATUS_CALLBACK_RECEIVED,
			PAYMENT_STATUS_PAID,
		}:
			return _build_initiation_response(
				payment=payment,
				ticket_name=ticket.name,
				phone_number=payment.phone_number,
				callback_url=callback_url,
				success=payment.status in {PAYMENT_STATUS_PROMPT_SENT, PAYMENT_STATUS_PAID},
				message=payment.provider_status_message
				or payment.failure_reason
				or _("Using existing payment attempt"),
				deduplicated=True,
			)

	# Prevent duplicate prompt creation while a payment attempt is in-flight.
	if payment.status in {
		PAYMENT_STATUS_PENDING,
		PAYMENT_STATUS_PROMPT_SENT,
		PAYMENT_STATUS_CALLBACK_RECEIVED,
	} and payment.checkout_request_id:
		return _build_initiation_response(
			payment=payment,
			ticket_name=ticket.name,
			phone_number=payment.phone_number,
			callback_url=callback_url,
			success=payment.status in {PAYMENT_STATUS_PROMPT_SENT, PAYMENT_STATUS_PAID},
			message=payment.provider_status_message or _("Payment attempt already in progress"),
			deduplicated=True,
		)

	attempt = _append_attempt(payment, idempotency_key=idempotency_key)

	if not _transition_payment_status(
		payment,
		PAYMENT_STATUS_PENDING,
		context={"reason": "initiation_attempt", "attempt_no": attempt.attempt_no},
		strict=True,
	):
		frappe.throw(_("Unable to start payment attempt"))

	_save_payment(payment)

	try:
		response = mpesa_handler.initiate_payment(
			phone=request["phone_number"],
			amount=request["amount"],
			account_reference=ticket.name,
			business_short_code=ticket.business_short_code,
			company=request["company"],
		)
	except Exception as exc:
		_apply_initiation_exception(payment, attempt, ticket.name, str(exc))
		raise

	if not isinstance(response, dict):
		response = {"ResponseDescription": str(response or ""), "ResponseCode": "1"}

	return _apply_initiation_response(
		payment=payment,
		attempt=attempt,
		ticket_name=ticket.name,
		phone_number=request["phone_number"],
		response=response,
		callback_url=callback_url,
	)



def get_mpesa_payment_status(
	payment_id: str | None = None,
	checkout_request_id: str | None = None,
	reference_name: str | None = None,
	reference_doctype: str | None = None,
	**_,
) -> dict[str, Any]:
	payment_name = _resolve_payment_name(
		payment_id=payment_id,
		checkout_request_id=checkout_request_id,
		reference_name=reference_name,
		reference_doctype=reference_doctype,
	)
	if not payment_name:
		frappe.throw(_("Payment not found"))

	payment = frappe.get_doc("All Trails Payment", payment_name)
	_authorize_payment_read(payment)
	return _serialize_payment(payment)



def handle_mpesa_callback(payload: str | dict[str, Any] | None = None, **kwargs) -> dict[str, Any]:
	request_payload = _get_callback_payload(payload=payload, kwargs=kwargs)
	normalized = _normalize_callback_payload(request_payload)
	payment = _find_payment_for_callback(normalized)

	if not payment:
		frappe.log_error(
			title="All Trails MPESA Callback Unmatched",
			message=frappe.as_json(request_payload),
		)
		return _accept_callback()

	payment = frappe.get_doc("All Trails Payment", payment.name, for_update=True)
	attempt, stale = _resolve_callback_attempt(payment, normalized)
	payload_name = _create_mpesa_payload(payment, normalized, request_payload)

	if stale:
		_record_stale_callback(payment, attempt, normalized, request_payload, payload_name)
		frappe.db.commit()
		return _accept_callback()

	if attempt:
		attempt.raw_callback_payload = frappe.as_json(request_payload)
		attempt.callback_received_on = now_datetime()

	updates: dict[str, Any] = {
		"provider_status_code": normalized.get("result_code"),
		"provider_status_message": normalized.get("status_message"),
		"raw_callback_payload": frappe.as_json(request_payload),
		"callback_received_on": now_datetime(),
	}
	if payload_name:
		updates["mpesa_payload"] = payload_name

	if normalized.get("checkout_request_id"):
		updates["checkout_request_id"] = normalized.get("checkout_request_id")
		if attempt and not attempt.checkout_request_id:
			attempt.checkout_request_id = normalized.get("checkout_request_id")
	if normalized.get("merchant_request_id"):
		updates["merchant_request_id"] = normalized.get("merchant_request_id")
		if attempt and not attempt.merchant_request_id:
			attempt.merchant_request_id = normalized.get("merchant_request_id")

	payment.update(updates)
	_transition_payment_status(
		payment,
		PAYMENT_STATUS_CALLBACK_RECEIVED,
		context={"reason": "callback_received"},
		strict=False,
	)

	if normalized.get("is_success"):
		if attempt:
			attempt.status_after_callback = PAYMENT_STATUS_PAID
		payment.receipt_number = normalized.get("receipt_number")
		payment.provider_transaction_id = normalized.get("provider_transaction_id")
		payment.failure_reason = None
		payment.paid_on = now_datetime()
		if _transition_payment_status(
			payment,
			PAYMENT_STATUS_PAID,
			context={"reason": "callback_success"},
			strict=False,
		):
			_set_ticket_status(payment.mpesa_ticket, TICKET_STATUS_COMPLETED)
		_ensure_payment_entry_posted(payment)
	else:
		failure_status = _map_failure_status(normalized.get("result_code"))
		if attempt:
			attempt.status_after_callback = failure_status
		payment.failure_reason = normalized.get("status_message")
		if normalized.get("provider_transaction_id"):
			payment.provider_transaction_id = normalized.get("provider_transaction_id")
		if _transition_payment_status(
			payment,
			failure_status,
			context={"reason": "callback_failure", "result_code": normalized.get("result_code")},
			strict=False,
		):
			_set_ticket_status(payment.mpesa_ticket, TICKET_STATUS_FAILED)

	_save_payment(payment)
	_sync_reference_booking(payment, context={"reason": "callback"})
	frappe.db.commit()
	return _accept_callback()



def _build_payment_request(
	reference_name: str | None,
	phone_number: str | None,
	amount: float | str | None,
	journey_type: str | None,
	reference_doctype: str | None,
	company: str | None,
	metadata: str | dict[str, Any] | None,
	kwargs: dict[str, Any],
) -> dict[str, Any]:
	resolved_reference_name = (reference_name or kwargs.get("reference_name") or "").strip()
	if not resolved_reference_name:
		frappe.throw(_("A reference name is required to initiate payment"))

	resolved_phone = _normalize_phone_number(phone_number or kwargs.get("phone_number"))
	if not resolved_phone:
		frappe.throw(_("A valid MPESA phone number is required"))

	resolved_amount = flt(amount or kwargs.get("amount"))
	if resolved_amount <= 0:
		frappe.throw(_("Payment amount must be greater than zero"))

	resolved_company = _resolve_company(company or kwargs.get("company"))
	business_short_code = _resolve_business_short_code(resolved_company)
	metadata_dict = _coerce_dict(metadata or kwargs.get("metadata"))

	return {
		"reference_name": resolved_reference_name,
		"reference_doctype": (reference_doctype or kwargs.get("reference_doctype") or "").strip(),
		"journey_type": (journey_type or kwargs.get("journey_type") or "Generic").strip(),
		"phone_number": resolved_phone,
		"amount": resolved_amount,
		"company": resolved_company,
		"business_short_code": business_short_code,
		"currency": (kwargs.get("currency") or "KES").strip() or "KES",
		"metadata": metadata_dict,
		"client_id": (kwargs.get("client_id") or frappe.session.user or resolved_reference_name).strip(),
	}



def _resolve_or_create_payment(
	request: dict[str, Any],
	*,
	payment_id: str | None,
	reuse_existing: bool,
):
	if payment_id:
		if not frappe.db.exists("All Trails Payment", payment_id):
			frappe.throw(_("Payment not found"))
		payment = frappe.get_doc("All Trails Payment", payment_id, for_update=True)
		if request["reference_name"] and payment.reference_name != request["reference_name"]:
			frappe.throw(_("Payment reference mismatch"))
		if request["reference_doctype"] and payment.reference_doctype != request["reference_doctype"]:
			frappe.throw(_("Payment reference doctype mismatch"))
		payment.phone_number = request["phone_number"]
		payment.amount = request["amount"]
		payment.metadata_json = frappe.as_json(request["metadata"]) if request["metadata"] else payment.metadata_json
		return payment

	if reuse_existing:
		existing_rows = frappe.get_all(
			"All Trails Payment",
			filters={
				"reference_name": request["reference_name"],
				"reference_doctype": request["reference_doctype"],
			},
			fields=["name"],
			order_by="creation desc",
			limit=1,
		)
		existing_name = existing_rows[0].name if existing_rows else None
		if existing_name:
			payment = frappe.get_doc("All Trails Payment", existing_name, for_update=True)
			payment.phone_number = request["phone_number"]
			payment.amount = request["amount"]
			payment.metadata_json = (
				frappe.as_json(request["metadata"]) if request["metadata"] else payment.metadata_json
			)
			return payment

	return _create_payment_doc(request)



def _create_payment_doc(request: dict[str, Any]):
	payment = frappe.get_doc(
		{
			"doctype": "All Trails Payment",
			"provider": "MPESA",
			"status": PAYMENT_STATUS_PENDING,
			"payment_journey": request["journey_type"],
			"reference_doctype": request["reference_doctype"],
			"reference_name": request["reference_name"],
			"user": None if frappe.session.user == "Guest" else frappe.session.user,
			"phone_number": request["phone_number"],
			"amount": request["amount"],
			"currency": request["currency"],
			"company": request["company"],
			"business_short_code": request["business_short_code"],
			"metadata_json": frappe.as_json(request["metadata"]) if request["metadata"] else None,
			"current_attempt_no": 0,
			"stale_callback_count": 0,
		}
	)
	payment.insert(ignore_permissions=True)
	return payment



def _get_or_create_mpesa_ticket(payment, request: dict[str, Any]):
	if payment.mpesa_ticket and frappe.db.exists("MPESA Ticket", payment.mpesa_ticket):
		ticket = frappe.get_doc("MPESA Ticket", payment.mpesa_ticket)
		ticket.msisdn = request["phone_number"]
		ticket.amount = request["amount"]
		ticket.ticket_status = TICKET_STATUS_REQUESTED
		ticket.flags.ignore_permissions = True
		ticket.save(ignore_permissions=True)
		return ticket

	company_abbr = frappe.db.get_value("Company", request["company"], "abbr")
	ticket_name = _generate_unique_ticket_name(request["company"])
	ticket = frappe.get_doc(
		{
			"doctype": "MPESA Ticket",
			"name": ticket_name,
			"client_id": request["client_id"],
			"msisdn": request["phone_number"],
			"amount": request["amount"],
			"company": request["company"],
			"company_abbr": company_abbr,
			"ticket_status": TICKET_STATUS_REQUESTED,
			"business_short_code": request["business_short_code"],
		}
	)
	ticket.insert(ignore_permissions=True)
	payment.mpesa_ticket = ticket.name
	return ticket



def _append_attempt(payment, *, idempotency_key: str | None):
	attempt_no = cint(payment.current_attempt_no) + 1
	attempt = payment.append(
		"attempts",
		{
			"attempt_no": attempt_no,
			"initiated_at": now_datetime(),
			"idempotency_key": idempotency_key,
			"status_after_callback": PAYMENT_STATUS_PENDING,
		},
	)
	payment.current_attempt_no = attempt_no
	payment.active_attempt_key = idempotency_key
	payment.last_attempted_on = now_datetime()
	return attempt



def _find_attempt_by_idempotency(payment, idempotency_key: str):
	for attempt in payment.get("attempts") or []:
		if cstr(attempt.idempotency_key).strip() == idempotency_key:
			return attempt
	return None



def _get_attempt_by_no(payment, attempt_no: int):
	for attempt in payment.get("attempts") or []:
		if cint(attempt.attempt_no) == cint(attempt_no):
			return attempt
	return None



def _apply_initiation_exception(payment, attempt, ticket_name: str, error_message: str) -> None:
	attempt.status_after_callback = PAYMENT_STATUS_FAILED
	attempt.raw_initiation_response = frappe.as_json({"error": error_message})
	payment.failure_reason = error_message
	payment.provider_status_message = error_message
	payment.raw_initiation_response = attempt.raw_initiation_response
	_transition_payment_status(
		payment,
		PAYMENT_STATUS_FAILED,
		context={"reason": "initiation_exception", "error": error_message},
		strict=False,
	)
	_set_ticket_status(ticket_name, TICKET_STATUS_FAILED)
	_save_payment(payment)
	_sync_reference_booking(payment, context={"reason": "initiation_exception"})
	frappe.db.commit()



def _apply_initiation_response(
	*,
	payment,
	attempt,
	ticket_name: str,
	phone_number: str,
	response: dict[str, Any],
	callback_url: str,
) -> dict[str, Any]:
	response_code = str(response.get("ResponseCode") or "")
	response_message = (
		response.get("CustomerMessage")
		or response.get("ResponseDescription")
		or _("Payment request sent")
	)
	success = response_code == "0"
	status = PAYMENT_STATUS_PROMPT_SENT if success else PAYMENT_STATUS_FAILED

	attempt.checkout_request_id = response.get("CheckoutRequestID")
	attempt.merchant_request_id = response.get("MerchantRequestID")
	attempt.raw_initiation_response = frappe.as_json(response)
	attempt.status_after_callback = status

	payment.provider_status_code = response_code or None
	payment.provider_status_message = response_message
	payment.raw_initiation_response = attempt.raw_initiation_response
	payment.checkout_request_id = attempt.checkout_request_id
	payment.merchant_request_id = attempt.merchant_request_id
	payment.failure_reason = None if success else response_message

	if _transition_payment_status(
		payment,
		status,
		context={"reason": "initiation_response", "response_code": response_code},
		strict=False,
	):
		if not success:
			_set_ticket_status(ticket_name, TICKET_STATUS_FAILED)
	else:
		if not success:
			_set_ticket_status(ticket_name, TICKET_STATUS_FAILED)

	_save_payment(payment)
	_sync_reference_booking(payment, context={"reason": "initiation_response"})
	frappe.db.commit()

	return _build_initiation_response(
		payment=payment,
		ticket_name=ticket_name,
		phone_number=phone_number,
		callback_url=callback_url,
		success=success,
		message=response_message,
		deduplicated=False,
	)



def _build_initiation_response(
	*,
	payment,
	ticket_name: str,
	phone_number: str,
	callback_url: str,
	success: bool,
	message: str,
	deduplicated: bool,
) -> dict[str, Any]:
	return {
		"success": success,
		"payment_id": payment.name,
		"status": payment.status,
		"message": message,
		"provider_status_code": payment.provider_status_code,
		"provider_status_message": payment.provider_status_message,
		"failure_reason": payment.failure_reason,
		"checkout_request_id": payment.checkout_request_id,
		"merchant_request_id": payment.merchant_request_id,
		"ticket_id": ticket_name,
		"ticket_status": _get_ticket_status(ticket_name),
		"amount": payment.amount,
		"phone_number": phone_number,
		"callback_url": callback_url,
		"attempt_no": cint(payment.current_attempt_no),
		"deduplicated": deduplicated,
	}



def _transition_payment_status(
	payment,
	new_status: str,
	*,
	context: dict[str, Any],
	strict: bool,
) -> bool:
	current = cstr(payment.status or PAYMENT_STATUS_PENDING)
	if new_status == current:
		return True

	allowed = PAYMENT_ALLOWED_TRANSITIONS.get(current, set())
	if new_status not in allowed:
		log_illegal_transition("Payment", payment.name, current, new_status, context)
		if strict:
			frappe.throw(
				_("Illegal payment status transition from {0} to {1}").format(current, new_status),
				frappe.ValidationError,
			)
		return False

	payment.status = new_status
	return True



def _resolve_payment_name(
	payment_id: str | None = None,
	checkout_request_id: str | None = None,
	reference_name: str | None = None,
	reference_doctype: str | None = None,
) -> str | None:
	if payment_id and frappe.db.exists("All Trails Payment", payment_id):
		return payment_id
	if checkout_request_id:
		name = frappe.db.get_value("All Trails Payment", {"checkout_request_id": checkout_request_id}, "name")
		if name:
			return name
		attempt_parent = frappe.db.get_value(
			"All Trails Payment Attempt",
			{"checkout_request_id": checkout_request_id},
			"parent",
		)
		if attempt_parent:
			return attempt_parent
	if reference_name:
		filters: dict[str, Any] = {"reference_name": reference_name}
		if reference_doctype:
			filters["reference_doctype"] = reference_doctype
		payments = frappe.db.get_all(
			"All Trails Payment",
			filters=filters,
			fields=["name"],
			order_by="creation desc",
			limit=1,
			as_list=True,
		)
		return payments[0][0] if payments else None
	return None



def _authorize_payment_read(payment) -> None:
	if frappe.session.user == "Administrator":
		return
	if frappe.has_permission("All Trails Payment", ptype="read", doc=payment):
		return
	if payment.user and payment.user == frappe.session.user:
		return
	frappe.throw(_("You do not have permission to access this payment"), frappe.PermissionError)



def _authorize_payment_write(payment) -> None:
	if frappe.session.user == "Administrator":
		return
	if payment.user and payment.user == frappe.session.user:
		return
	if frappe.has_permission("All Trails Payment", ptype="write", doc=payment):
		return
	frappe.throw(_("You do not have permission to modify this payment"), frappe.PermissionError)



def _serialize_payment(payment) -> dict[str, Any]:
	status = payment.status or PAYMENT_STATUS_PENDING
	ticket_status = _get_ticket_status(payment.mpesa_ticket)

	attempt_history = [
		{
			"attempt_no": cint(attempt.attempt_no),
			"initiated_at": attempt.initiated_at,
			"checkout_request_id": attempt.checkout_request_id,
			"merchant_request_id": attempt.merchant_request_id,
			"status_after_callback": attempt.status_after_callback,
			"callback_received_on": attempt.callback_received_on,
		}
		for attempt in (payment.get("attempts") or [])
	]

	return {
		"payment_id": payment.name,
		"status": status,
		"paid": status == PAYMENT_STATUS_PAID,
		"failed": status in {PAYMENT_STATUS_FAILED, PAYMENT_STATUS_CANCELLED, PAYMENT_STATUS_TIMEOUT},
		"is_terminal": status in TERMINAL_PAYMENT_STATUSES,
		"message": payment.provider_status_message or payment.failure_reason or status,
		"checkout_request_id": payment.checkout_request_id,
		"merchant_request_id": payment.merchant_request_id,
		"ticket_id": payment.mpesa_ticket,
		"ticket_status": ticket_status,
		"receipt_number": payment.receipt_number,
		"provider_transaction_id": payment.provider_transaction_id,
		"provider_status_code": payment.provider_status_code,
		"provider_status_message": payment.provider_status_message,
		"failure_reason": payment.failure_reason,
		"amount": payment.amount,
		"phone_number": payment.phone_number,
		"reference_name": payment.reference_name,
		"reference_doctype": payment.reference_doctype,
		"payment_journey": payment.payment_journey,
		"paid_on": payment.paid_on,
		"callback_received_on": payment.callback_received_on,
		"attempt_no": cint(payment.current_attempt_no),
		"stale_callback_count": cint(payment.stale_callback_count),
		"payment_entry": payment.payment_entry,
		"attempt_history": attempt_history,
	}



def _get_callback_payload(payload: str | dict[str, Any] | None, kwargs: dict[str, Any]) -> dict[str, Any]:
	if isinstance(payload, dict):
		return payload
	if isinstance(payload, str) and payload.strip():
		try:
			return json.loads(payload)
		except json.JSONDecodeError:
			pass
	if kwargs:
		return kwargs
	try:
		raw_body = frappe.request.get_data(as_text=True)
	except Exception:
		raw_body = ""
	if raw_body:
		try:
			return json.loads(raw_body)
		except json.JSONDecodeError:
			pass
	return {}



def _normalize_callback_payload(payload: dict[str, Any]) -> dict[str, Any]:
	stk_callback = payload.get("Body", {}).get("stkCallback") or payload.get("stkCallback")
	if stk_callback:
		metadata = _callback_items_to_dict(stk_callback.get("CallbackMetadata", {}).get("Item") or [])
		result_code = _normalize_result_code(stk_callback.get("ResultCode"))
		receipt_number = metadata.get("MpesaReceiptNumber")
		return {
			"checkout_request_id": stk_callback.get("CheckoutRequestID"),
			"merchant_request_id": stk_callback.get("MerchantRequestID"),
			"result_code": result_code,
			"status_message": stk_callback.get("ResultDesc") or "",
			"amount": flt(metadata.get("Amount") or 0),
			"receipt_number": receipt_number,
			"provider_transaction_id": receipt_number,
			"phone_number": _normalize_phone_number(metadata.get("PhoneNumber")),
			"transaction_date": metadata.get("TransactionDate"),
			"ticket_id": payload.get("AccountReference") or payload.get("account_number"),
			"is_success": result_code == "0",
		}

	transaction_reference = (
		payload.get("transaction_reference")
		or payload.get("TransID")
		or payload.get("MpesaReceiptNumber")
		or payload.get("ReceiptNo")
	)
	result_code = payload.get("result_code")
	if result_code in (None, ""):
		result_code = payload.get("ResultCode")
	result_code = _normalize_result_code(result_code)
	if not result_code and transaction_reference:
		result_code = "0"

	return {
		"checkout_request_id": payload.get("CheckoutRequestID"),
		"merchant_request_id": payload.get("MerchantRequestID"),
		"result_code": result_code,
		"status_message": payload.get("ResultDesc") or payload.get("result_desc") or "",
		"amount": flt(payload.get("amount") or payload.get("TransAmount") or 0),
		"receipt_number": payload.get("MpesaReceiptNumber") or payload.get("ReceiptNo") or transaction_reference,
		"provider_transaction_id": transaction_reference,
		"phone_number": _normalize_phone_number(
			payload.get("phone") or payload.get("MSISDN") or payload.get("PhoneNumber")
		),
		"transaction_date": payload.get("transaction_date") or payload.get("TransTime"),
		"ticket_id": payload.get("account_number") or payload.get("BillRefNumber") or payload.get("AccountReference"),
		"is_success": result_code == "0",
	}



def _find_payment_for_callback(normalized: dict[str, Any]):
	checkout_request_id = normalized.get("checkout_request_id")
	merchant_request_id = normalized.get("merchant_request_id")
	ticket_id = normalized.get("ticket_id")

	if checkout_request_id:
		attempt_parent = frappe.db.get_value(
			"All Trails Payment Attempt",
			{"checkout_request_id": checkout_request_id},
			"parent",
		)
		if attempt_parent and frappe.db.exists("All Trails Payment", attempt_parent):
			return frappe.get_doc("All Trails Payment", attempt_parent)

		name = frappe.db.get_value(
			"All Trails Payment",
			{"checkout_request_id": checkout_request_id},
			"name",
		)
		if name:
			return frappe.get_doc("All Trails Payment", name)

	if merchant_request_id:
		attempt_parent = frappe.db.get_value(
			"All Trails Payment Attempt",
			{"merchant_request_id": merchant_request_id},
			"parent",
		)
		if attempt_parent and frappe.db.exists("All Trails Payment", attempt_parent):
			return frappe.get_doc("All Trails Payment", attempt_parent)

		name = frappe.db.get_value(
			"All Trails Payment",
			{"merchant_request_id": merchant_request_id},
			"name",
		)
		if name:
			return frappe.get_doc("All Trails Payment", name)

	if ticket_id:
		name = frappe.db.get_value("All Trails Payment", {"mpesa_ticket": ticket_id}, "name")
		if name:
			return frappe.get_doc("All Trails Payment", name)

	return None



def _resolve_callback_attempt(payment, normalized: dict[str, Any]):
	checkout_request_id = normalized.get("checkout_request_id")
	merchant_request_id = normalized.get("merchant_request_id")
	current_attempt_no = cint(payment.current_attempt_no)
	attempt = None

	if checkout_request_id or merchant_request_id:
		for row in payment.get("attempts") or []:
			if checkout_request_id and cstr(row.checkout_request_id) == cstr(checkout_request_id):
				attempt = row
				break
			if merchant_request_id and cstr(row.merchant_request_id) == cstr(merchant_request_id):
				attempt = row
				break

	if attempt:
		if current_attempt_no and cint(attempt.attempt_no) != current_attempt_no:
			return attempt, True
		return attempt, False

	if current_attempt_no <= 0:
		return None, False

	if checkout_request_id or merchant_request_id:
		return None, True

	current_attempt = _get_attempt_by_no(payment, current_attempt_no)
	return current_attempt, False



def _record_stale_callback(
	payment,
	attempt,
	normalized: dict[str, Any],
	request_payload: dict[str, Any],
	payload_name: str | None,
):
	payment.stale_callback_count = cint(payment.stale_callback_count) + 1
	if payload_name:
		payment.mpesa_payload = payload_name
	payment.raw_callback_payload = frappe.as_json(request_payload)
	payment.callback_received_on = now_datetime()
	if attempt:
		attempt.status_after_callback = "Ignored Stale"
		attempt.callback_received_on = now_datetime()
		attempt.raw_callback_payload = frappe.as_json(request_payload)

	frappe.log_error(
		title="All Trails Stale MPESA Callback Ignored",
		message=frappe.as_json(
			{
				"payment": payment.name,
				"current_attempt_no": cint(payment.current_attempt_no),
				"attempt_no": cint(attempt.attempt_no) if attempt else None,
				"checkout_request_id": normalized.get("checkout_request_id"),
				"merchant_request_id": normalized.get("merchant_request_id"),
			}
		),
	)
	_save_payment(payment)



def _create_mpesa_payload(payment, normalized: dict[str, Any], payload: dict[str, Any]) -> str | None:
	if not payment.mpesa_ticket:
		return None

	transaction_reference = (
		normalized.get("provider_transaction_id")
		or normalized.get("receipt_number")
		or normalized.get("checkout_request_id")
		or normalized.get("merchant_request_id")
	)
	if not transaction_reference:
		return None

	existing_name = frappe.db.get_value(
		"MPESA Payload",
		{"transaction_reference": transaction_reference},
		"name",
	)
	if existing_name:
		return existing_name

	# Some deployments install MPESA Payload hooks that query Patient on save.
	# Skip payload creation if Patient table is unavailable to keep callbacks non-blocking.
	if not frappe.db.table_exists("Patient"):
		return None

	mpesa_payload = frappe.get_doc(
		{
			"doctype": "MPESA Payload",
			"phone": normalized.get("phone_number"),
			"amount": normalized.get("amount") or payment.amount,
			"transaction_reference": transaction_reference,
			"account_number": payment.mpesa_ticket,
			"json_dump": frappe.as_json(payload),
			"is_processed": 0,
			"company": payment.company,
		}
	)
	try:
		mpesa_payload.insert(ignore_permissions=True)
	except Exception:
		frappe.log_error(
			title="All Trails MPESA Payload Insert Failed",
			message=frappe.as_json(
				{
					"payment": payment.name,
					"ticket": payment.mpesa_ticket,
					"transaction_reference": transaction_reference,
					"traceback": frappe.get_traceback(),
				}
			),
		)
		return None
	return mpesa_payload.name



def _map_failure_status(result_code: str | None) -> str:
	code = str(result_code or "")
	if code == "1032":
		return PAYMENT_STATUS_CANCELLED
	if code == "1037":
		return PAYMENT_STATUS_TIMEOUT
	return PAYMENT_STATUS_FAILED



def _ensure_payment_entry_posted(payment) -> str:
	if not frappe.db.exists("DocType", "Payment Entry"):
		frappe.throw(_("Payment Entry doctype is required for accounting posting"))

	with _payment_entry_user():
		existing_name = cstr(getattr(payment, "payment_entry", "") or "").strip()
		if existing_name and frappe.db.exists("Payment Entry", existing_name):
			existing_doc = frappe.get_doc("Payment Entry", existing_name)
			if cint(existing_doc.docstatus) == 0:
				existing_doc.flags.ignore_permissions = True
				existing_doc.submit()
			if cint(existing_doc.docstatus) == 1:
				return existing_doc.name

		customer = _ensure_customer_for_payment(payment)
		reference_no = _build_payment_reference_no(payment)
		existing_name = frappe.db.get_value(
			"Payment Entry",
			{
				"payment_type": "Receive",
				"company": payment.company,
				"party_type": "Customer",
				"party": customer,
				"reference_no": reference_no,
				"docstatus": ["!=", 2],
			},
			"name",
		)
		if existing_name:
			existing_doc = frappe.get_doc("Payment Entry", existing_name)
			if cint(existing_doc.docstatus) == 0:
				existing_doc.flags.ignore_permissions = True
				existing_doc.submit()
			payment.payment_entry = existing_doc.name
			return existing_doc.name

		paid_from = _resolve_customer_receivable_account(customer, payment.company)
		mode_of_payment, paid_to = _resolve_payment_destination(payment.company)
		posting_date = getdate(payment.paid_on) if payment.paid_on else getdate(today())

		pe = frappe.new_doc("Payment Entry")
		pe.payment_type = "Receive"
		pe.company = payment.company
		pe.posting_date = posting_date
		pe.party_type = "Customer"
		pe.party = customer
		pe.paid_from = paid_from
		pe.paid_to = paid_to
		pe.paid_amount = flt(payment.amount)
		pe.received_amount = flt(payment.amount)
		pe.source_exchange_rate = 1
		pe.target_exchange_rate = 1
		pe.reference_no = reference_no
		pe.reference_date = posting_date
		if mode_of_payment:
			pe.mode_of_payment = mode_of_payment
		pe.remarks = (
			f"All Trails MPESA payment {payment.name} for {payment.reference_doctype} {payment.reference_name}"
		)

		pe.flags.ignore_permissions = True
		pe.insert(ignore_permissions=True)
		if cint(pe.docstatus) == 0:
			pe.flags.ignore_permissions = True
			pe.submit()

		payment.payment_entry = pe.name
		return pe.name


@contextmanager
def _payment_entry_user():
	current_user = cstr(frappe.session.user or "Guest")
	if current_user == "Administrator":
		yield
		return

	if frappe.has_permission("Payment Entry", ptype="create", user=current_user):
		yield
		return

	frappe.set_user("Administrator")
	try:
		yield
	finally:
		frappe.set_user(current_user)



def _ensure_customer_for_payment(payment) -> str:
	user_id = cstr(payment.user or "").strip()
	user_doc = frappe.get_doc("User", user_id) if user_id and frappe.db.exists("User", user_id) else None

	email = cstr((user_doc.email if user_doc else user_id) or "").strip().lower()
	if not email:
		email = cstr(user_id or payment.reference_name or payment.name).strip().lower()

	existing_name = frappe.db.get_value("Customer", {"email_id": email}, "name") if email else None
	if existing_name:
		return existing_name

	display_name = ""
	if user_doc:
		display_name = cstr(user_doc.full_name or user_doc.first_name or user_doc.name).strip()
	if not display_name:
		display_name = cstr(payment.reference_name or payment.name).strip()

	customer = frappe.new_doc("Customer")
	customer.customer_name = display_name
	customer.customer_type = "Individual"
	customer.customer_group = _resolve_default_customer_group()
	customer.territory = _resolve_default_customer_territory()
	if email:
		customer.email_id = email
	if payment.phone_number:
		customer.mobile_no = payment.phone_number

	customer.flags.ignore_permissions = True
	customer.insert(ignore_permissions=True)
	return customer.name



def _resolve_default_customer_group() -> str:
	group = cstr(frappe.db.get_single_value("Selling Settings", "customer_group") or "").strip()
	if group and frappe.db.exists("Customer Group", group):
		return group

	row = frappe.db.get_value("Customer Group", {"is_group": 0}, "name")
	if row:
		return cstr(row)

	frappe.throw(_("Please configure at least one leaf Customer Group for Payment Entry posting"))



def _resolve_default_customer_territory() -> str:
	territory = cstr(frappe.db.get_single_value("Selling Settings", "territory") or "").strip()
	if territory and frappe.db.exists("Territory", territory):
		return territory

	row = frappe.db.get_value("Territory", {"is_group": 0}, "name")
	if row:
		return cstr(row)

	frappe.throw(_("Please configure at least one leaf Territory for Payment Entry posting"))



def _resolve_customer_receivable_account(customer: str, company: str) -> str:
	from erpnext.accounts.party import get_party_account

	account = cstr(get_party_account("Customer", customer, company) or "").strip()
	if account:
		return account

	account = cstr(frappe.db.get_value("Company", company, "default_receivable_account") or "").strip()
	if account:
		return account

	frappe.throw(_("Default receivable account is required to post Payment Entry"))



def _resolve_payment_destination(company: str) -> tuple[str | None, str]:
	mode_candidates = ("MPESA", "M-Pesa", "M Pesa", "Cash")
	for mode_name in mode_candidates:
		if not frappe.db.exists("Mode of Payment", mode_name):
			continue
		account = frappe.db.get_value(
			"Mode of Payment Account",
			{"parent": mode_name, "company": company},
			"default_account",
		)
		if account:
			return mode_name, cstr(account)

	account = cstr(frappe.db.get_value("Company", company, "default_bank_account") or "").strip()
	if account:
		return None, account

	account = cstr(frappe.db.get_value("Company", company, "default_cash_account") or "").strip()
	if account:
		return None, account

	row = frappe.db.sql(
		"""
			select name
			from `tabAccount`
			where company = %(company)s
				and is_group = 0
				and account_type in ('Bank', 'Cash')
			order by account_type = 'Bank' desc, creation asc
			limit 1
		""",
		{"company": company},
		as_dict=True,
	)
	if row:
		return None, cstr(row[0].name)

	frappe.throw(_("No bank/cash account found for company {0} to post Payment Entry").format(company))



def _build_payment_reference_no(payment) -> str:
	return cstr(
		payment.receipt_number
		or payment.provider_transaction_id
		or payment.checkout_request_id
		or payment.name
	).strip()



def _accept_callback() -> dict[str, Any]:
	frappe.local.response.update({"ResultCode": 0, "ResultDesc": "Accepted"})
	return {"ResultCode": 0, "ResultDesc": "Accepted"}



def _callback_items_to_dict(items: list[dict[str, Any]]) -> dict[str, Any]:
	result: dict[str, Any] = {}
	for item in items:
		key = item.get("Name")
		if key:
			result[key] = item.get("Value")
	return result



def _normalize_result_code(value: Any) -> str:
	if value is None:
		return ""
	return str(value).strip()



def _coerce_dict(value: str | dict[str, Any] | None) -> dict[str, Any]:
	if isinstance(value, dict):
		return value
	if isinstance(value, str) and value.strip():
		try:
			parsed = json.loads(value)
			return parsed if isinstance(parsed, dict) else {}
		except json.JSONDecodeError:
			return {}
	return {}



def _normalize_phone_number(phone_number: Any) -> str:
	raw_value = "".join(ch for ch in str(phone_number or "") if ch.isdigit())
	if not raw_value:
		return ""
	if raw_value.startswith("0") and len(raw_value) == 10:
		return f"254{raw_value[1:]}"
	if raw_value.startswith("254") and len(raw_value) == 12:
		return raw_value
	if raw_value.startswith("7") and len(raw_value) == 9:
		return f"254{raw_value}"
	return ""



def _resolve_company(company: str | None) -> str:
	resolved = (company or frappe.defaults.get_user_default("Company") or "").strip()
	if not resolved:
		resolved = frappe.db.get_single_value("Global Defaults", "default_company") or ""
	if not resolved:
		companies = frappe.get_all("Company", pluck="name", limit=1)
		resolved = companies[0] if companies else ""
	if not resolved or not frappe.db.exists("Company", resolved):
		frappe.throw(_("A default company is required before initiating MPESA payments"))
	return resolved



def _resolve_business_short_code(company: str) -> str:
	business_short_code = frappe.db.get_value(
		"Mpesa Settings",
		{"custom_company": company},
		"business_shortcode",
	)
	if not business_short_code:
		frappe.throw(
			_("Mpesa Settings with a business short code are required for company {0}").format(company)
		)
	return str(business_short_code)



def _generate_unique_ticket_name(company: str) -> str:
	for _ in range(5):
		ticket_name = mpesa_handler.generate_mpesa_ticket_id(company)
		if not frappe.db.exists("MPESA Ticket", ticket_name):
			return ticket_name
	frappe.throw(_("Unable to generate a unique MPESA ticket reference"))



def _ensure_mpesa_callback_url(business_short_code: str) -> str:
	settings_name = frappe.db.get_value(
		"Mpesa Settings",
		{"business_shortcode": business_short_code},
		"name",
	)
	if not settings_name:
		frappe.throw(_("Mpesa Settings not found for short code {0}").format(business_short_code))

	callback_url = f"{get_url().rstrip('/')}/api/method/all_trails.api.handle_mpesa_callback"
	current_callback = frappe.db.get_value("Mpesa Settings", settings_name, "custom_confirmation_url")
	if current_callback != callback_url:
		frappe.db.set_value(
			"Mpesa Settings",
			settings_name,
			"custom_confirmation_url",
			callback_url,
			update_modified=False,
		)
	return callback_url



def _set_ticket_status(ticket_name: str | None, status: str) -> None:
	if ticket_name and frappe.db.exists("MPESA Ticket", ticket_name):
		frappe.db.set_value("MPESA Ticket", ticket_name, "ticket_status", status, update_modified=False)



def _get_ticket_status(ticket_name: str | None) -> str | None:
	if not ticket_name:
		return None
	if not frappe.db.exists("MPESA Ticket", ticket_name):
		return None
	return frappe.db.get_value("MPESA Ticket", ticket_name, "ticket_status")



def _save_payment(payment) -> None:
	payment.flags.ignore_permissions = True
	payment.save(ignore_permissions=True)



def _sync_reference_booking(payment, *, context: dict[str, Any]):
	if payment.reference_doctype != "Trail Booking" or not payment.reference_name:
		return

	try:
		from all_trails.services.booking import sync_booking_payment_state_from_payment

		sync_booking_payment_state_from_payment(payment=payment, status=payment.status, context=context)
	except Exception:
		frappe.log_error(
			title="All Trails Payment to Booking Sync Failed",
			message=frappe.get_traceback(),
		)
