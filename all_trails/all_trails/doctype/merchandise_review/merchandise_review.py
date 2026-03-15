from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class MerchandiseReview(Document):
	def validate(self):
		rating = flt(self.rating)
		if rating < 1 or rating > 5:
			frappe.throw(_("Rating must be between 1 and 5."))

	def after_insert(self):
		self._refresh_item_stats()

	def on_update(self):
		self._refresh_item_stats()

	def _refresh_item_stats(self):
		if not self.item_code or not frappe.db.exists("Merchandise Item", self.item_code):
			return

		reviews = frappe.get_all(
			"Merchandise Review",
			filters={"item_code": self.item_code, "status": "Approved"},
			fields=["rating"],
		)
		if not reviews:
			frappe.db.set_value(
				"Merchandise Item",
				self.item_code,
				{
					"average_rating": 0,
					"review_count": 0,
				},
				update_modified=False,
			)
			return

		total = sum(flt(review["rating"]) for review in reviews)
		frappe.db.set_value(
			"Merchandise Item",
			self.item_code,
			{
				"average_rating": round(total / len(reviews), 2),
				"review_count": len(reviews),
			},
			update_modified=False,
		)
