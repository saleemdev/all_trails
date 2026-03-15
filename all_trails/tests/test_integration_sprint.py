from __future__ import annotations

from contextlib import contextmanager

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import cint

from all_trails.services.blog import create_blog_comment, get_blog_comments
from all_trails.services.booking import (
	cancel_booking,
	create_booking,
	get_booking_detail,
	initiate_booking_payment,
)
from all_trails.services.member import register_member


class TestIntegrationSprint(FrappeTestCase):
	def setUp(self):
		self.system_user = "Administrator"
		frappe.set_user(self.system_user)
		self._required_doctypes_available = all(
			frappe.db.exists("DocType", dt)
			for dt in ["Trail", "Trail Booking", "All Trails Payment", "Web Page", "Comment"]
		)

	def tearDown(self):
		frappe.set_user(self.system_user)

	def _unique_email(self, prefix: str) -> str:
		return f"{prefix}.{frappe.generate_hash(length=8)}@example.com"

	def _create_user(self, prefix: str) -> str:
		email = self._unique_email(prefix)
		frappe.get_doc(
			{
				"doctype": "User",
				"email": email,
				"first_name": prefix.title(),
				"last_name": "User",
				"send_welcome_email": 0,
				"new_password": "StrongPassw0rd!",
				"enabled": 1,
				"user_type": "Website User",
			}
		).insert(ignore_permissions=True)
		return email

	def _create_trail(self, max_capacity: int = 5, available_spots: int = 5) -> str:
		trail = frappe.get_doc(
			{
				"doctype": "Trail",
				"title": f"Trail {frappe.generate_hash(length=6)}",
				"slug": f"trail-{frappe.generate_hash(length=6)}",
				"description": "Test trail",
				"difficulty_level": "Moderate",
				"location": "Nairobi",
				"scheduled_date": "2030-01-01",
				"start_time": "08:00:00",
				"end_time": "14:00:00",
				"max_capacity": max_capacity,
				"available_spots": available_spots,
				"price_kshs": 2500,
				"status": "Active",
				"published": 1,
			}
		)
		trail.insert(ignore_permissions=True)
		return trail.name

	@contextmanager
	def _mock_mpesa_gateway(self):
		import all_trails.payments as payments

		original_initiate = payments.mpesa_handler.initiate_payment
		original_callback_url = payments._ensure_mpesa_callback_url
		original_company = payments._resolve_company
		original_shortcode = payments._resolve_business_short_code

		counter = {"value": 0}

		def fake_initiate_payment(**_kwargs):
			counter["value"] += 1
			suffix = frappe.generate_hash(length=6)
			return {
				"ResponseCode": "0",
				"ResponseDescription": "Request accepted",
				"CustomerMessage": "Prompt sent",
				"CheckoutRequestID": f"ws_CO_{counter['value']}_{suffix}",
				"MerchantRequestID": f"mr_{counter['value']}_{suffix}",
			}

		def fake_callback_url(_short_code):
			return "https://example.test/api/method/all_trails.api.handle_mpesa_callback"

		def fake_company(company):
			if company and frappe.db.exists("Company", company):
				return company
			companies = frappe.get_all("Company", pluck="name", limit=1)
			if not companies:
				self.skipTest("No Company configured in test site")
			return companies[0]

		payments.mpesa_handler.initiate_payment = fake_initiate_payment
		payments._ensure_mpesa_callback_url = fake_callback_url
		payments._resolve_company = fake_company
		payments._resolve_business_short_code = lambda _company: "123456"

		try:
			yield counter
		finally:
			payments.mpesa_handler.initiate_payment = original_initiate
			payments._ensure_mpesa_callback_url = original_callback_url
			payments._resolve_company = original_company
			payments._resolve_business_short_code = original_shortcode

	def test_register_member_new_and_existing_user_paths(self):
		email = self._unique_email("register")
		email_queue_before = frappe.db.count("Email Queue") if frappe.db.exists("DocType", "Email Queue") else 0

		result_new = register_member(
			email=email,
			password="StrongPassw0rd!",
			first_name="Trail",
			last_name="Member",
			phone="0712345678",
		)
		self.assertTrue(result_new["success"])
		self.assertTrue(frappe.db.exists("User", email))
		self.assertTrue(frappe.db.exists("Member", {"email": email}))
		self.assertTrue(frappe.db.exists("Has Role", {"parent": email, "role": "Trail Member"}))
		self.assertEqual(frappe.db.get_value("User", email, "send_welcome_email"), 0)

		result_existing = register_member(
			email=email,
			password="UpdatedPassw0rd!",
			first_name="Updated",
			last_name="Name",
			phone="254712000000",
		)
		self.assertTrue(result_existing["success"])
		self.assertEqual(frappe.db.get_value("User", email, "first_name"), "Updated")
		self.assertEqual(frappe.db.get_value("Member", {"email": email}, "first_name"), "Updated")

		if frappe.db.exists("DocType", "Email Queue"):
			email_queue_after = frappe.db.count("Email Queue")
			self.assertEqual(email_queue_before, email_queue_after)

	def test_booking_capacity_and_ownership_enforcement(self):
		if not self._required_doctypes_available:
			self.skipTest("Required doctypes unavailable")

		user_one = self._create_user("owner")
		user_two = self._create_user("other")
		trail_id = self._create_trail(max_capacity=1, available_spots=1)

		frappe.set_user(user_one)
		booking = create_booking(
			trail_id=trail_id,
			spots_booked=1,
			selected_activities=[],
			idempotency_key=f"idem-{frappe.generate_hash(length=10)}",
		)
		self.assertEqual(booking["spots_booked"], 1)
		self.assertEqual(frappe.db.get_value("Trail", trail_id, "available_spots"), 0)

		with self.assertRaises(frappe.ValidationError):
			create_booking(
				trail_id=trail_id,
				spots_booked=1,
				selected_activities=[],
				idempotency_key=f"idem-{frappe.generate_hash(length=10)}",
			)

		frappe.set_user(user_two)
		with self.assertRaises(frappe.PermissionError):
			get_booking_detail(booking["id"])

	def test_booking_idempotency_prevents_duplicate_capacity_decrement(self):
		if not self._required_doctypes_available:
			self.skipTest("Required doctypes unavailable")

		user = self._create_user("idempotent")
		trail_id = self._create_trail(max_capacity=5, available_spots=5)
		idempotency_key = f"idem-{frappe.generate_hash(length=10)}"

		frappe.set_user(user)
		first = create_booking(
			trail_id=trail_id,
			spots_booked=2,
			selected_activities=[],
			idempotency_key=idempotency_key,
		)
		second = create_booking(
			trail_id=trail_id,
			spots_booked=2,
			selected_activities=[],
			idempotency_key=idempotency_key,
		)

		self.assertEqual(first["id"], second["id"])
		self.assertEqual(frappe.db.get_value("Trail", trail_id, "available_spots"), 3)

	def test_payment_retry_reuses_payment_and_ignores_stale_callback(self):
		if not self._required_doctypes_available:
			self.skipTest("Required doctypes unavailable")
		if not frappe.db.exists("DocType", "MPESA Ticket"):
			self.skipTest("MPESA Ticket doctype unavailable")

		user = self._create_user("payer")
		trail_id = self._create_trail(max_capacity=3, available_spots=3)

		frappe.set_user(user)
		booking = create_booking(
			trail_id=trail_id,
			spots_booked=1,
			selected_activities=[],
			idempotency_key=f"idem-{frappe.generate_hash(length=10)}",
		)

		with self._mock_mpesa_gateway():
			first_attempt = initiate_booking_payment(
				booking_id=booking["id"],
				phone_number="0712345678",
				idempotency_key=f"pay-{frappe.generate_hash(length=10)}",
			)
			from all_trails.payments import handle_mpesa_callback

			# Fail first attempt so user can retry.
			failure_payload = {
				"Body": {
					"stkCallback": {
						"MerchantRequestID": first_attempt["merchant_request_id"],
						"CheckoutRequestID": first_attempt["checkout_request_id"],
						"ResultCode": 1032,
						"ResultDesc": "Request cancelled by user",
					}
				}
			}
			handle_mpesa_callback(payload=failure_payload)

			second_attempt = initiate_booking_payment(
				booking_id=booking["id"],
				phone_number="0712345678",
				idempotency_key=f"pay-{frappe.generate_hash(length=10)}",
			)

			self.assertEqual(first_attempt["payment_id"], second_attempt["payment_id"])
			self.assertEqual(first_attempt["ticket_id"], second_attempt["ticket_id"])

			payment = frappe.get_doc("All Trails Payment", first_attempt["payment_id"])
			self.assertEqual(cint(payment.current_attempt_no), 2)
			self.assertEqual(len(payment.attempts), 2)

			stale_payload = {
				"Body": {
					"stkCallback": {
						"MerchantRequestID": payment.attempts[0].merchant_request_id,
						"CheckoutRequestID": payment.attempts[0].checkout_request_id,
						"ResultCode": 0,
						"ResultDesc": "Success",
						"CallbackMetadata": {"Item": [{"Name": "MpesaReceiptNumber", "Value": "RCPT-OLD"}]},
					}
				}
			}
			handle_mpesa_callback(payload=stale_payload)
			payment.reload()
			self.assertNotEqual(payment.status, "Paid")
			self.assertEqual(cint(payment.stale_callback_count), 1)

			active_payload = {
				"Body": {
					"stkCallback": {
						"MerchantRequestID": payment.attempts[1].merchant_request_id,
						"CheckoutRequestID": payment.attempts[1].checkout_request_id,
						"ResultCode": 0,
						"ResultDesc": "Success",
						"CallbackMetadata": {"Item": [{"Name": "MpesaReceiptNumber", "Value": "RCPT-NEW"}]},
					}
				}
			}
			handle_mpesa_callback(payload=active_payload)
			payment.reload()
			self.assertEqual(payment.status, "Paid")
			self.assertTrue(payment.payment_entry)
			payment_entry = frappe.get_doc("Payment Entry", payment.payment_entry)
			self.assertEqual(cint(payment_entry.docstatus), 1)
			self.assertEqual(payment_entry.payment_type, "Receive")
			self.assertEqual(payment_entry.party_type, "Customer")
			self.assertEqual(payment_entry.reference_no, "RCPT-NEW")

			payment_entry_count_before = frappe.db.count(
				"Payment Entry",
				filters={
					"company": payment.company,
					"payment_type": "Receive",
					"party_type": "Customer",
					"party": payment_entry.party,
					"reference_no": payment_entry.reference_no,
					"docstatus": ["!=", 2],
				},
			)
			handle_mpesa_callback(payload=active_payload)
			payment.reload()
			self.assertEqual(payment.payment_entry, payment_entry.name)
			payment_entry_count_after = frappe.db.count(
				"Payment Entry",
				filters={
					"company": payment.company,
					"payment_type": "Receive",
					"party_type": "Customer",
					"party": payment_entry.party,
					"reference_no": payment_entry.reference_no,
					"docstatus": ["!=", 2],
				},
			)
			self.assertEqual(payment_entry_count_before, payment_entry_count_after)

		booking_doc = frappe.get_doc("Trail Booking", booking["id"])
		self.assertEqual(booking_doc.status, "Confirmed")
		self.assertIn(booking_doc.payment_status, ["Paid", "Completed"])

	def test_booking_state_machine_guard(self):
		if not self._required_doctypes_available:
			self.skipTest("Required doctypes unavailable")

		user = self._create_user("guard")
		trail_id = self._create_trail(max_capacity=2, available_spots=2)

		frappe.set_user(user)
		booking = create_booking(
			trail_id=trail_id,
			spots_booked=1,
			selected_activities=[],
			idempotency_key=f"idem-{frappe.generate_hash(length=10)}",
		)

		booking_doc = frappe.get_doc("Trail Booking", booking["id"])
		booking_doc.status = "Completed"
		booking_doc.save(ignore_permissions=True)

		with self.assertRaises(frappe.ValidationError):
			cancel_booking(booking_id=booking["id"], reason="Should not allow")

	def test_blog_guest_comment_moderation(self):
		if not frappe.db.exists("DocType", "Web Page"):
			self.skipTest("Web Page doctype unavailable")

		slug = f"guest-comment-{frappe.generate_hash(length=6)}"
		web_page = frappe.get_doc(
			{
				"doctype": "Web Page",
				"title": f"Blog {slug}",
				"route": f"blog/{slug}",
				"published": 1,
				"content_type": "HTML",
				"main_section_html": "<p>Post content</p>",
			}
		)
		web_page.insert(ignore_permissions=True)

		frappe.set_user("Guest")
		response = create_blog_comment(
			slug=slug,
			content="<script>alert(1)</script><p>Looks good</p>",
			comment_by="Guest User",
			comment_email="guest@example.com",
		)
		self.assertTrue(response["success"])
		comment = frappe.get_doc("Comment", response["comment_id"])
		self.assertEqual(cint(comment.published), 0)
		self.assertNotIn("<script", (comment.content or "").lower())

		public_comments = get_blog_comments(slug=slug, page=1, page_size=10)
		self.assertEqual(public_comments["total"], 0)
