from __future__ import annotations

import json

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class MerchandiseOrder(Document):
	def validate(self):
		for fieldname in ["items_json", "timeline_json"]:
			if getattr(self, fieldname, None):
				json.loads(getattr(self, fieldname))

		if flt(self.amount_due_now) < 0 or flt(self.amount_remaining) < 0:
			frappe.throw(_("Order balances cannot be negative."))

		if self.payment_method not in {"MPESA", "BNPL", "Cash on Delivery"}:
			frappe.throw(_("Unsupported payment method."))
