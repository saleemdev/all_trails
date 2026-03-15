# Copyright (c) 2026, Salim and contributors
# For license information, please see license.txt

from __future__ import annotations

import json

from frappe.model.document import Document


class AllTrailsPayment(Document):
	def validate(self):
		if self.metadata_json:
			json.loads(self.metadata_json)

