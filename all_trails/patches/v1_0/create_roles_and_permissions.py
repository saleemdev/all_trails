from __future__ import annotations

import frappe
from frappe.permissions import add_permission, update_permission_property

from all_trails.services.member import ensure_role


ROLE_TRAIL_MEMBER = "Trail Member"
ROLE_BLOGGER = "Blogger"


PERMISSION_MATRIX = {
	"Member": {
		ROLE_TRAIL_MEMBER: {"read": 1, "write": 1, "create": 1, "if_owner": 1},
	},
	"Trail": {
		ROLE_TRAIL_MEMBER: {"read": 1},
		"Guest": {"read": 1},
	},
	"Trail Booking": {
		ROLE_TRAIL_MEMBER: {"read": 1, "write": 1, "create": 1, "if_owner": 1},
	},
	"Trail Feedback": {
		ROLE_TRAIL_MEMBER: {"read": 1, "write": 1, "create": 1, "if_owner": 1},
		"Guest": {"read": 1},
	},
	"All Trails Payment": {
		ROLE_TRAIL_MEMBER: {"read": 1, "if_owner": 1},
	},
}



def _ensure_permissions(doctype: str, role: str, properties: dict[str, int]) -> None:
	if not frappe.db.exists("DocType", doctype):
		return
	add_permission(doctype, role, ptype="read")
	for ptype, value in properties.items():
		update_permission_property(
			doctype,
			role,
			0,
			ptype,
			value,
			validate=False,
		)



def execute():
	ensure_role(ROLE_TRAIL_MEMBER)
	ensure_role(ROLE_BLOGGER)

	for doctype, role_map in PERMISSION_MATRIX.items():
		for role, properties in role_map.items():
			_ensure_permissions(doctype, role, properties)

	frappe.clear_cache()
