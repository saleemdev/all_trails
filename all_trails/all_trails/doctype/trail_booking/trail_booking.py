from __future__ import annotations

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class TrailBooking(Document):
	def validate(self):
		if self.spots_booked is None or int(self.spots_booked) <= 0:
			frappe.throw("Spots booked must be greater than zero")
		self.spots_booked = int(self.spots_booked)

		self.base_price = flt(self.base_price)
		self.activities_price = flt(self.activities_price)
		self.total_price = flt(self.total_price)

		if self.total_price < 0:
			frappe.throw("Total price cannot be negative")
		if self.base_price < 0:
			frappe.throw("Base price cannot be negative")
		if self.activities_price < 0:
			frappe.throw("Activities price cannot be negative")

		if not self.confirmation_code:
			self.confirmation_code = frappe.generate_hash(length=12).upper()
