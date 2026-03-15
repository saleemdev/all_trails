from __future__ import annotations

import json
from collections.abc import Iterable
from typing import Any

import frappe
from frappe import _
from frappe.utils import cstr

ROLE_TRAIL_MEMBER = "Trail Member"
ROLE_BLOGGER = "Blogger"


def ensure_authenticated_user() -> str:
	if frappe.session.user == "Guest":
		frappe.throw(_("Authentication required"), frappe.PermissionError)
	return frappe.session.user


def parse_json_input(value: Any, default: Any):
	if value is None:
		return default
	if isinstance(value, (dict, list)):
		return value
	if isinstance(value, str) and value.strip():
		try:
			return json.loads(value)
		except Exception:
			return default
	return default


def slugify(value: str) -> str:
	raw = cstr(value or "").strip().lower()
	raw = raw.replace("_", "-")
	return "-".join(part for part in raw.split("-") if part)


def user_has_role(user: str, role: str) -> bool:
	if user == "Administrator":
		return True
	if not user or not role:
		return False
	return bool(frappe.db.exists("Has Role", {"parent": user, "role": role}))


def require_roles(roles: Iterable[str], *, require_all: bool = False) -> None:
	user = ensure_authenticated_user()
	roles = [role for role in roles if role]
	if not roles:
		return

	if require_all:
		missing = [role for role in roles if not user_has_role(user, role)]
		if missing:
			frappe.throw(
				_("Missing required role(s): {0}").format(", ".join(missing)),
				frappe.PermissionError,
			)
		return

	if any(user_has_role(user, role) for role in roles):
		return

	frappe.throw(
		_("You do not have the required role to perform this action"),
		frappe.PermissionError,
	)


def get_request_ip() -> str:
	return cstr(getattr(frappe.local, "request_ip", "") or "")


def enforce_ip_session_rate_limit(scope: str, *, limit: int, window_seconds: int) -> None:
	"""Simple abuse throttling by IP and session id."""
	ip = get_request_ip() or "unknown"
	sid = cstr(getattr(frappe.session, "sid", "") or "guest")

	keys = [
		f"all_trails:rl:{scope}:ip:{ip}",
		f"all_trails:rl:{scope}:sid:{sid}",
	]

	for key in keys:
		current = int(frappe.cache.get_value(key) or 0) + 1
		frappe.cache.set_value(key, current, expires_in_sec=window_seconds)
		if current > limit:
			frappe.throw(
				_("Too many requests. Please try again later."),
				frappe.RateLimitExceededError,
			)


def log_illegal_transition(entity: str, name: str, from_state: str, to_state: str, context: dict[str, Any]):
	frappe.log_error(
		title=f"All Trails Illegal {entity} Transition",
		message=frappe.as_json(
			{
				"entity": entity,
				"name": name,
				"from": from_state,
				"to": to_state,
				"context": context,
			}
		),
	)


def append_status_log(existing_log: str | None, message: str) -> str:
	entry = f"[{frappe.utils.now()}] {message}"
	if not existing_log:
		return entry
	return f"{existing_log}\n{entry}"[-12000:]
