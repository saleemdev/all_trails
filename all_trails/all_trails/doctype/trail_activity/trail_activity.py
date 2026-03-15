from __future__ import annotations

import frappe
from frappe.model.document import Document


class TrailActivity(Document):
	def validate(self):
		self.activity_name = (self.activity_name or "").strip()
		if not self.activity_name:
			frappe.throw("Activity name is required")
		if self.max_participants is not None and int(self.max_participants) < 0:
			frappe.throw("Max participants cannot be negative")
		if self.available_spots is not None and int(self.available_spots) < 0:
			frappe.throw("Available spots cannot be negative")
