from __future__ import annotations

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class TrailBookingActivity(Document):
	def validate(self):
		self.activity_name = (self.activity_name or "").strip()
		if not self.activity_name:
			frappe.throw("Activity name is required")

		self.quantity = int(self.quantity or 0)
		if self.quantity <= 0:
			frappe.throw("Activity quantity must be greater than zero")

		self.unit_price = flt(self.unit_price)
		self.total_price = flt(self.total_price) or flt(self.unit_price) * self.quantity
		if self.unit_price < 0 or self.total_price < 0:
			frappe.throw("Activity prices cannot be negative")
