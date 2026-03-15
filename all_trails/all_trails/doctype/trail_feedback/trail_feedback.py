from __future__ import annotations

import frappe
from frappe.model.document import Document


class TrailFeedback(Document):
	def validate(self):
		self.rating = int(self.rating or 0)
		if self.rating < 1 or self.rating > 5:
			frappe.throw("Rating must be between 1 and 5")

		if not (self.feedback_text or "").strip():
			frappe.throw("Feedback text is required")
