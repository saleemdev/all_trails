from __future__ import annotations

import json

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class MerchandiseItem(Document):
	def validate(self):
		if not self.slug and self.item_name:
			self.slug = frappe.scrub(self.item_name).replace("_", "-")

		if flt(self.discount_price) and flt(self.discount_price) > flt(self.selling_price):
			frappe.throw(_("Discount price cannot exceed the selling price."))

		if self.bnpl_eligible and flt(self.bnpl_min_amount) > flt(self.selling_price):
			frappe.throw(_("BNPL minimum amount cannot exceed the selling price."))

		for fieldname in [
			"gallery_json",
			"highlights_json",
			"materials_json",
			"badges_json",
			"available_colors_json",
			"available_sizes_json",
		]:
			if getattr(self, fieldname, None):
				json.loads(getattr(self, fieldname))
