from __future__ import annotations

import frappe
from frappe.model.document import Document


class MerchandiseCategory(Document):
	def validate(self):
		if not self.slug and self.category_name:
			self.slug = frappe.scrub(self.category_name).replace("_", "-")
