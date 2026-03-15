from __future__ import annotations

import frappe
from frappe.model.document import Document
from frappe.utils import cstr


class Trail(Document):
	def validate(self):
		self.title = (self.title or "").strip()
		self.slug = (self.slug or "").strip() or frappe.scrub(self.title)
		self.slug = cstr(self.slug).replace("_", "-")

		if self.max_capacity is None:
			self.max_capacity = 0
		if self.available_spots is None:
			self.available_spots = 0

		self.max_capacity = int(self.max_capacity)
		self.available_spots = int(self.available_spots)

		if self.max_capacity < 0:
			frappe.throw("Max capacity cannot be negative")
		if self.available_spots < 0:
			frappe.throw("Available spots cannot be negative")
		if self.available_spots > self.max_capacity:
			frappe.throw("Available spots cannot exceed max capacity")
