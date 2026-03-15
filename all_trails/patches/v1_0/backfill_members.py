from __future__ import annotations

import frappe
from frappe.core.doctype.user.user import STANDARD_USERS

from all_trails.services.member import assign_role_if_missing, ensure_member_record


ROLE_TRAIL_MEMBER = "Trail Member"



def execute():
	users = frappe.get_all(
		"User",
		filters={"enabled": 1},
		fields=["name", "email", "first_name", "last_name", "mobile_no"],
	)

	for user in users:
		if user.name in STANDARD_USERS:
			continue

		assign_role_if_missing(user.name, ROLE_TRAIL_MEMBER)
		ensure_member_record(
			user=user.name,
			email=user.email or user.name,
			first_name=user.first_name,
			last_name=user.last_name,
			phone=user.mobile_no,
			registration_source="Admin",
		)

	frappe.clear_cache()
