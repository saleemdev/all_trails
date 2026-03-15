from __future__ import annotations

import json

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class BNPLPlan(Document):
	def validate(self):
		if self.schedule_json:
			json.loads(self.schedule_json)

		if flt(self.remaining_amount) < 0 or flt(self.upfront_amount) < 0:
			frappe.throw(_("BNPL amounts cannot be negative."))
