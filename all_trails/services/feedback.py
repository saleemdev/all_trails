from __future__ import annotations

from typing import Any

import frappe
from frappe import _
from frappe.utils import cint, cstr, now_datetime

from all_trails.services.common import ensure_authenticated_user



def submit_trail_feedback(
	trail_id: str,
	rating: int,
	feedback_text: str,
	title: str | None = None,
	booking_id: str | None = None,
) -> dict[str, Any]:
	user = ensure_authenticated_user()
	if not trail_id:
		frappe.throw(_("Trail ID is required"))
	if not frappe.db.exists("Trail", trail_id):
		frappe.throw(_("Trail not found"))

	rating = cint(rating)
	if rating < 1 or rating > 5:
		frappe.throw(_("Rating must be between 1 and 5"))

	feedback_text = cstr(feedback_text).strip()
	if not feedback_text:
		frappe.throw(_("Feedback text is required"))

	if booking_id:
		if not frappe.db.exists("Trail Booking", booking_id):
			frappe.throw(_("Booking not found"))
		booking_user = frappe.db.get_value("Trail Booking", booking_id, "user")
		if booking_user != user and user != "Administrator":
			frappe.throw(_("You cannot attach feedback to this booking"), frappe.PermissionError)

	feedback = frappe.get_doc(
		{
			"doctype": "Trail Feedback",
			"trail": trail_id,
			"booking": booking_id,
			"user": user,
			"rating": rating,
			"title": cstr(title).strip() or None,
			"feedback_text": feedback_text,
			"submitted_on": now_datetime(),
			"published": 0,
			"moderation_status": "Pending",
			"ip_address": cstr(getattr(frappe.local, "request_ip", "")),
		}
	)
	feedback.insert(ignore_permissions=True)
	frappe.db.commit()

	return {
		"success": True,
		"message": _("Feedback submitted and awaiting moderation"),
		"feedback_id": feedback.name,
	}



def get_trail_feedback(trail_id: str, page: int = 1, page_size: int = 10):
	if not trail_id:
		frappe.throw(_("Trail ID is required"))

	page_no = max(cint(page), 1)
	limit = min(max(cint(page_size), 1), 100)

	rows = frappe.db.sql(
		"""
			select name, user, rating, title, feedback_text, submitted_on, creation
			from `tabTrail Feedback`
			where trail = %(trail)s
				and (published = 1 or moderation_status = 'Approved')
			order by creation desc
			limit %(limit)s offset %(offset)s
		""",
		{
			"trail": trail_id,
			"limit": limit,
			"offset": (page_no - 1) * limit,
		},
		as_dict=True,
	)
	total_row = frappe.db.sql(
		"""
			select count(*) as total
			from `tabTrail Feedback`
			where trail = %(trail)s
				and (published = 1 or moderation_status = 'Approved')
		""",
		{"trail": trail_id},
		as_dict=True,
	)
	total = cint(total_row[0].total if total_row else 0)
	user_names = {
		row.user: frappe.db.get_value("User", row.user, "full_name")
		for row in rows
		if row.user
	}

	data = [
		{
			"id": row.name,
			"user": row.user,
			"author": user_names.get(row.user) or row.user,
			"rating": cint(row.rating),
			"title": row.title,
			"feedback_text": row.feedback_text,
			"submitted_on": row.submitted_on or row.creation,
		}
		for row in rows
	]

	return {
		"data": data,
		"total": total,
		"page": page_no,
		"page_size": limit,
	}
