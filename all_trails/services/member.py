from __future__ import annotations

from typing import Any

import frappe
from frappe import _
from frappe.core.doctype.user.user import STANDARD_USERS
from frappe.utils import cstr, now_datetime, validate_email_address

from all_trails.services.common import ROLE_TRAIL_MEMBER


def _normalize_phone(phone: str | None) -> str | None:
	phone = cstr(phone).strip()
	return phone or None


def _can_use_mobile(mobile_no: str | None, user_name: str | None) -> bool:
	if not mobile_no:
		return True
	existing_user = frappe.db.get_value("User", {"mobile_no": mobile_no}, "name")
	if not existing_user:
		return True
	return existing_user == user_name


def ensure_role(role_name: str) -> None:
	if not role_name:
		return
	if frappe.db.exists("Role", role_name):
		return
	frappe.get_doc({"doctype": "Role", "role_name": role_name}).insert(ignore_permissions=True)


def assign_role_if_missing(user: str, role_name: str) -> None:
	if not user or user in STANDARD_USERS:
		return
	if not role_name:
		return
	if frappe.db.exists("Has Role", {"parent": user, "role": role_name}):
		return
	user_doc = frappe.get_doc("User", user)
	user_doc.append_roles(role_name)
	user_doc.flags.ignore_permissions = True
	user_doc.save(ignore_permissions=True)


def ensure_member_record(
	*,
	user: str,
	email: str,
	first_name: str | None,
	last_name: str | None,
	phone: str | None,
	registration_source: str,
) -> str:
	email = cstr(email).strip().lower()
	member_name = frappe.db.get_value("Member", {"email": email}, "name")
	if not member_name and user:
		member_name = frappe.db.get_value("Member", {"user": user}, "name")

	values = {
		"first_name": cstr(first_name).strip(),
		"last_name": cstr(last_name).strip(),
		"email": email,
		"user": user,
		"phone": cstr(phone).strip() or None,
		"registration_source": registration_source,
		"last_synced": now_datetime(),
	}

	if member_name:
		member = frappe.get_doc("Member", member_name)
		member.update(values)
		member.flags.ignore_permissions = True
		member.save(ignore_permissions=True)
		return member.name

	member = frappe.get_doc(
		{
			"doctype": "Member",
			**values,
		}
	)
	member.insert(ignore_permissions=True)
	return member.name


def register_member(
	email: str,
	password: str,
	first_name: str,
	last_name: str | None = None,
	phone: str | None = None,
	registration_source: str = "Frontend Register",
) -> dict[str, Any]:
	email = cstr(email).strip().lower()
	if not email:
		frappe.throw(_("Email is required"))
	if not password:
		frappe.throw(_("Password is required"))
	if not first_name:
		frappe.throw(_("First name is required"))

	validate_email_address(email, throw=True)

	user_exists = frappe.db.exists("User", email)
	normalized_phone = _normalize_phone(phone)
	if user_exists:
		user = frappe.get_doc("User", email)
		if user.name in STANDARD_USERS:
			frappe.throw(_("Invalid user account for registration"))

		user.first_name = cstr(first_name).strip()
		user.last_name = cstr(last_name).strip()
		if _can_use_mobile(normalized_phone, user.name):
			user.mobile_no = normalized_phone or user.mobile_no
		user.enabled = 1
		user.send_welcome_email = 0
		user.new_password = password
		user.flags.no_welcome_mail = True
		user.flags.ignore_permissions = True
		user.save(ignore_permissions=True)
	else:
		user = frappe.get_doc(
			{
				"doctype": "User",
				"email": email,
				"first_name": cstr(first_name).strip(),
				"last_name": cstr(last_name).strip(),
				"mobile_no": normalized_phone if _can_use_mobile(normalized_phone, None) else None,
				"send_welcome_email": 0,
				"new_password": password,
				"user_type": "Website User",
				"enabled": 1,
			}
		)
		user.flags.no_welcome_mail = True
		user.insert(ignore_permissions=True)

	ensure_role(ROLE_TRAIL_MEMBER)
	assign_role_if_missing(user.name, ROLE_TRAIL_MEMBER)

	member_name = ensure_member_record(
		user=user.name,
		email=email,
		first_name=user.first_name,
		last_name=user.last_name,
		phone=normalized_phone or user.mobile_no,
		registration_source=registration_source,
	)

	frappe.db.commit()
	return {
		"success": True,
		"user": user.name,
		"member": member_name,
		"message": _("Registration completed successfully"),
	}


def on_user_after_insert(doc, _method=None):
	"""Ensure default role/member linkage for users created via /signup or Desk."""
	if not doc or doc.name in STANDARD_USERS:
		return

	try:
		ensure_role(ROLE_TRAIL_MEMBER)
		assign_role_if_missing(doc.name, ROLE_TRAIL_MEMBER)
		ensure_member_record(
			user=doc.name,
			email=doc.email or doc.name,
			first_name=doc.first_name,
			last_name=doc.last_name,
			phone=doc.mobile_no,
			registration_source="Frappe Signup",
		)
	except Exception:
		frappe.log_error(
			title="All Trails User Post-Insert Sync Failed",
			message=frappe.get_traceback(),
		)
