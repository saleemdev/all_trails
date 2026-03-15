from __future__ import annotations

from frappe.model.document import Document


class Member(Document):
	def validate(self):
		self.email = (self.email or "").strip().lower()
		self.first_name = (self.first_name or "").strip()
		self.last_name = (self.last_name or "").strip()
		self.full_name = " ".join(part for part in [self.first_name, self.last_name] if part)
		if not self.full_name:
			self.full_name = self.email
