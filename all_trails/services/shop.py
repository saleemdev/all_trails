from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

import frappe
from frappe import _
from frappe.utils import add_days, cstr, flt, now_datetime

from all_trails.payments import initiate_mpesa_payment


DEFAULT_SHIPPING_FEE = 650.0
FREE_SHIPPING_THRESHOLD = 15000.0
BNPL_SPLIT_COUNT = 2
ORDER_PAYMENT_STATUS_PENDING = "Pending"
ORDER_PAYMENT_STATUS_PROMPT_SENT = "Prompt Sent"
ORDER_PAYMENT_STATUS_PAID = "Paid"
ORDER_PAYMENT_STATUS_PARTIALLY_PAID = "Partially Paid"
ORDER_PAYMENT_STATUS_FAILED = "Failed"
ORDER_PAYMENT_STATUS_CANCELLED = "Cancelled"

MPESA_PAYMENT_STATUS_PENDING = "Pending"
MPESA_PAYMENT_STATUS_PROMPT_SENT = "Prompt Sent"
MPESA_PAYMENT_STATUS_CALLBACK_RECEIVED = "Callback Received"
MPESA_PAYMENT_STATUS_PAID = "Paid"
MPESA_PAYMENT_STATUS_FAILED = "Failed"
MPESA_PAYMENT_STATUS_CANCELLED = "Cancelled"
MPESA_PAYMENT_STATUS_TIMEOUT = "Timeout"

COUPON_RULES: dict[str, dict[str, Any]] = {
	"SUMMIT10": {
		"valid": True,
		"code": "SUMMIT10",
		"description": "10% off technical gear orders over KES 5,000",
		"discount_type": "percentage",
		"discount_value": 10,
		"max_discount": 1800,
		"min_subtotal": 5000,
	},
	"FREESHIP": {
		"valid": True,
		"code": "FREESHIP",
		"description": "Waive standard shipping on this order",
		"discount_type": "shipping",
		"discount_value": DEFAULT_SHIPPING_FEE,
		"min_subtotal": 3500,
	},
}

SAMPLE_CATEGORIES: list[dict[str, Any]] = [
	{
		"name": "Packs",
		"slug": "packs",
		"description": "Fast-day packs and multi-day carry systems built for East African terrain.",
		"hero_copy": "Carry less dead weight and more altitude.",
		"accent": "#5b7f72",
		"image_url": "",
		"featured": 1,
		"sort_order": 1,
	},
	{
		"name": "Apparel",
		"slug": "apparel",
		"description": "Layering pieces tuned for early starts, summit wind, and post-hike coffee.",
		"hero_copy": "Warm when the ridge opens up.",
		"accent": "#925d40",
		"image_url": "",
		"featured": 1,
		"sort_order": 2,
	},
	{
		"name": "Camp Kitchen",
		"slug": "camp-kitchen",
		"description": "Drinkware and camp essentials that survive the boot of the shuttle van.",
		"hero_copy": "Ritual gear for the trailhead and the fireline.",
		"accent": "#657a88",
		"image_url": "",
		"featured": 0,
		"sort_order": 3,
	},
	{
		"name": "Accessories",
		"slug": "accessories",
		"description": "Small-format performance gear that solves the annoying parts of hiking.",
		"hero_copy": "Tiny upgrades, big comfort.",
		"accent": "#8f6a3e",
		"image_url": "",
		"featured": 0,
		"sort_order": 4,
	},
]

SAMPLE_ITEMS: list[dict[str, Any]] = [
	{
		"item_code": "SUMMIT-PACK-28",
		"slug": "summit-pack-28",
		"item_name": "Summit Pack 28L",
		"category_name": "Packs",
		"category_slug": "packs",
		"short_description": "An all-day technical pack with hydration routing and weatherproof shell.",
		"description": "Built for fast ascents and late descents with stable carry, quick-access organization, and a weatherproof shell.",
		"selling_price": 12400,
		"discount_price": 10800,
		"average_rating": 4.8,
		"review_count": 34,
		"image_url": "",
		"gallery_urls": [],
		"highlights": ["28L weatherproof shell", "Ventilated back panel", "Quick-stash trekking pole loops"],
		"materials": ["420D recycled ripstop", "YKK AquaGuard zips", "Closed-cell foam frame sheet"],
		"badges": ["Best Seller", "BNPL Ready"],
		"inventory_qty": 17,
		"available_colors": ["Mist Olive", "Basalt Black", "Clay Dune"],
		"available_sizes": ["One Size"],
		"estimated_dispatch": "Ships in 24 hours",
		"is_featured": 1,
		"is_active": 1,
		"bnpl_eligible": 1,
		"bnpl_min_amount": 9000,
	},
	{
		"item_code": "RIDGELINE-SHELL",
		"slug": "ridgeline-shell",
		"item_name": "Ridgeline Shell Jacket",
		"category_name": "Apparel",
		"category_slug": "apparel",
		"short_description": "A lightweight shell with enough structure for sudden escarpment wind.",
		"description": "A lightweight shell that cuts rain on the move and layers cleanly over technical base layers.",
		"selling_price": 14900,
		"discount_price": 13250,
		"average_rating": 4.7,
		"review_count": 21,
		"image_url": "",
		"gallery_urls": [],
		"highlights": ["10K waterproof membrane", "Helmet-compatible hood", "Two-way venting zips"],
		"materials": ["3-layer laminate", "Taped seams", "Recycled nylon face"],
		"badges": ["Limited Run"],
		"inventory_qty": 12,
		"available_colors": ["Summit Rust", "Night Pine"],
		"available_sizes": ["S", "M", "L", "XL"],
		"estimated_dispatch": "Ships in 48 hours",
		"is_featured": 1,
		"is_active": 1,
		"bnpl_eligible": 1,
		"bnpl_min_amount": 12000,
	},
	{
		"item_code": "ALPINE-FLASK-1L",
		"slug": "alpine-flask-1l",
		"item_name": "Alpine Flask 1L",
		"category_name": "Camp Kitchen",
		"category_slug": "camp-kitchen",
		"short_description": "Double-wall bottle for cold summit water or hot chai on the return leg.",
		"description": "Vacuum insulated, easy to clean, and fitted with a grippy powder coat that stays usable in cold weather.",
		"selling_price": 3600,
		"discount_price": 3200,
		"average_rating": 4.9,
		"review_count": 58,
		"image_url": "",
		"gallery_urls": [],
		"highlights": ["24-hour cold retention", "18/8 stainless build", "Leak-lock loop cap"],
		"materials": ["Stainless steel", "BPA-free lid gasket"],
		"badges": ["Gift Pick"],
		"inventory_qty": 46,
		"available_colors": ["Glacier Blue", "Trail Sand", "Forest"],
		"available_sizes": ["1L"],
		"estimated_dispatch": "Ships today",
		"is_featured": 1,
		"is_active": 1,
		"bnpl_eligible": 0,
		"bnpl_min_amount": 5000,
	},
	{
		"item_code": "RIFT-TREK-POLES",
		"slug": "rift-trek-poles",
		"item_name": "Rift Trek Poles",
		"category_name": "Accessories",
		"category_slug": "accessories",
		"short_description": "Adjustable carbon-composite trekking poles for steep and loose sections.",
		"description": "Lightweight trekking poles that pack down small and stay rigid once the route gets slippery.",
		"selling_price": 11800,
		"discount_price": 10100,
		"average_rating": 4.8,
		"review_count": 29,
		"image_url": "",
		"gallery_urls": [],
		"highlights": ["Carbon-composite shafts", "Quick-lock height adjustment", "Packed length under 40cm"],
		"materials": ["Carbon-composite", "Cork blend grip", "Tungsten carbide tip"],
		"badges": ["Guide Pick", "BNPL Ready"],
		"inventory_qty": 9,
		"available_colors": ["Carbon", "Sand"],
		"available_sizes": ["One Size"],
		"estimated_dispatch": "Ships in 48 hours",
		"is_featured": 0,
		"is_active": 1,
		"bnpl_eligible": 1,
		"bnpl_min_amount": 9000,
	},
]

SAMPLE_REVIEWS: dict[str, list[dict[str, Any]]] = {
	"SUMMIT-PACK-28": [
		{
			"id": "sample-pack-1",
			"customer_name": "Ruth M.",
			"rating": 5,
			"title": "Stable even on fast descents",
			"review_text": "It stays planted and the back ventilation makes a real difference on hotter routes.",
			"created_at": "2026-02-14T09:30:00.000Z",
			"verified_purchase": True,
			"helpful_count": 11,
		}
	],
	"RIDGELINE-SHELL": [
		{
			"id": "sample-shell-1",
			"customer_name": "Angela W.",
			"rating": 5,
			"title": "Saved a rainy Aberdare morning",
			"review_text": "Light enough to forget, solid enough once the weather turned.",
			"created_at": "2026-02-02T07:45:00.000Z",
			"verified_purchase": True,
			"helpful_count": 8,
		}
	],
}


def _doctype_ready(doctype: str) -> bool:
	return bool(frappe.db.exists("DocType", doctype))


def _parse_json(value: Any, fallback: Any):
	if value in (None, ""):
		return deepcopy(fallback)
	if isinstance(value, (dict, list)):
		return deepcopy(value)
	try:
		return json.loads(value)
	except Exception:
		return deepcopy(fallback)


def _isoformat(value: Any) -> str | None:
	if not value:
		return None
	if hasattr(value, "isoformat"):
		return value.isoformat()
	return cstr(value)


def _as_bool(value: Any) -> bool:
	if isinstance(value, bool):
		return value
	if isinstance(value, str):
		return value.strip().lower() in {"1", "true", "yes", "on"}
	return bool(value)


def _mask_phone_number(phone: str | None) -> str:
	digits = "".join(ch for ch in cstr(phone) if ch.isdigit())
	if len(digits) <= 4:
		return digits
	return f"{'*' * (len(digits) - 4)}{digits[-4:]}"


def _require_authenticated_user() -> None:
	if frappe.session.user == "Guest":
		frappe.throw(_("Authentication is required."), frappe.PermissionError)


def _get_session_email() -> str:
	if frappe.session.user == "Guest":
		return ""
	return cstr(frappe.db.get_value("User", frappe.session.user, "email") or frappe.session.user).strip()


def _has_read_access(doctype: str, doc: Any | None = None) -> bool:
	try:
		return bool(frappe.has_permission(doctype, ptype="read", doc=doc))
	except Exception:
		return False


def _assert_order_access(order_doc: Any) -> None:
	if _has_read_access("Merchandise Order", doc=order_doc):
		return

	session_email = _get_session_email().lower()
	customer_email = cstr(order_doc.customer_email).strip().lower()
	if session_email and customer_email and session_email == customer_email:
		return

	frappe.throw(_("You do not have permission to access this order."), frappe.PermissionError)


def _public_price(item: dict[str, Any]) -> float:
	discount_price = item.get("discount_price")
	return flt(discount_price if discount_price else item.get("selling_price"))


def _extract_order_timeline(order_doc: Any) -> list[dict[str, Any]]:
	timeline = _parse_json(order_doc.timeline_json, [])
	return timeline if isinstance(timeline, list) else []


def _append_timeline_event(
	timeline: list[dict[str, Any]],
	label: str,
	detail: str,
	happened_at: str | None = None,
) -> None:
	event_label = cstr(label).strip()
	event_detail = cstr(detail).strip()
	if not event_label:
		return
	for event in timeline:
		if cstr(event.get("label")).strip() == event_label and cstr(event.get("detail")).strip() == event_detail:
			return
	timeline.append(
		{
			"label": event_label,
			"detail": event_detail,
			"happened_at": happened_at or now_datetime().isoformat(),
		}
	)


def _find_latest_payment_for_order(order_name: str) -> str | None:
	if not _doctype_ready("All Trails Payment"):
		return None
	rows = frappe.get_all(
		"All Trails Payment",
		filters={"reference_doctype": "Merchandise Order", "reference_name": order_name},
		fields=["name"],
		order_by="creation desc",
		limit=1,
	)
	return rows[0]["name"] if rows else None


def _get_mpesa_payment_detail(payment_id: str | None) -> dict[str, Any] | None:
	if not payment_id:
		return None
	if not _doctype_ready("All Trails Payment"):
		return None
	if not frappe.db.exists("All Trails Payment", payment_id):
		return None

	payment = frappe.db.get_value(
		"All Trails Payment",
		payment_id,
		[
			"name",
			"status",
			"provider_status_code",
			"provider_status_message",
			"failure_reason",
			"checkout_request_id",
			"merchant_request_id",
			"mpesa_ticket",
			"receipt_number",
			"provider_transaction_id",
			"amount",
			"phone_number",
			"paid_on",
			"callback_received_on",
		],
		as_dict=True,
	)
	if not payment:
		return None

	status = cstr(payment.get("status")).strip() or MPESA_PAYMENT_STATUS_PENDING
	failed = status in {MPESA_PAYMENT_STATUS_FAILED, MPESA_PAYMENT_STATUS_CANCELLED, MPESA_PAYMENT_STATUS_TIMEOUT}
	ticket_id = cstr(payment.get("mpesa_ticket")).strip() or None
	ticket_status = None
	if ticket_id and frappe.db.exists("MPESA Ticket", ticket_id):
		ticket_status = frappe.db.get_value("MPESA Ticket", ticket_id, "ticket_status")

	message = (
		cstr(payment.get("provider_status_message")).strip()
		or cstr(payment.get("failure_reason")).strip()
		or status
	)

	return {
		"payment_id": payment.get("name"),
		"status": status,
		"paid": status == MPESA_PAYMENT_STATUS_PAID,
		"failed": failed,
		"is_terminal": status in {MPESA_PAYMENT_STATUS_PAID, MPESA_PAYMENT_STATUS_FAILED, MPESA_PAYMENT_STATUS_CANCELLED, MPESA_PAYMENT_STATUS_TIMEOUT},
		"message": message,
		"ticket_id": ticket_id,
		"ticket_status": ticket_status,
		"checkout_request_id": payment.get("checkout_request_id"),
		"merchant_request_id": payment.get("merchant_request_id"),
		"receipt_number": payment.get("receipt_number"),
		"provider_transaction_id": payment.get("provider_transaction_id"),
		"provider_status_code": payment.get("provider_status_code"),
		"provider_status_message": payment.get("provider_status_message"),
		"failure_reason": payment.get("failure_reason"),
		"amount": flt(payment.get("amount")),
		"phone_number": payment.get("phone_number"),
		"paid_on": _isoformat(payment.get("paid_on")),
		"callback_received_on": _isoformat(payment.get("callback_received_on")),
	}


def _map_order_payment_status(payment_method: str, payment_status: str | None) -> str:
	method = cstr(payment_method).strip()
	status = cstr(payment_status).strip() or MPESA_PAYMENT_STATUS_PENDING

	if method == "Cash on Delivery":
		return ORDER_PAYMENT_STATUS_PENDING
	if status == MPESA_PAYMENT_STATUS_PAID:
		return ORDER_PAYMENT_STATUS_PARTIALLY_PAID if method == "BNPL" else ORDER_PAYMENT_STATUS_PAID
	if status == MPESA_PAYMENT_STATUS_CANCELLED:
		return ORDER_PAYMENT_STATUS_CANCELLED
	if status in {MPESA_PAYMENT_STATUS_FAILED, MPESA_PAYMENT_STATUS_TIMEOUT}:
		return ORDER_PAYMENT_STATUS_FAILED
	return ORDER_PAYMENT_STATUS_PROMPT_SENT


def _build_payment_status_event(status: str, message: str) -> tuple[str, str]:
	if status in {ORDER_PAYMENT_STATUS_PAID, ORDER_PAYMENT_STATUS_PARTIALLY_PAID}:
		return ("Payment confirmed", message or "Payment confirmed successfully.")
	if status == ORDER_PAYMENT_STATUS_CANCELLED:
		return ("Payment cancelled", message or "The MPESA request was cancelled.")
	if status == ORDER_PAYMENT_STATUS_FAILED:
		return ("Payment failed", message or "The MPESA request did not complete successfully.")
	return ("Payment in progress", message or "Waiting for MPESA confirmation.")


def _sync_order_payment_from_gateway(order_doc: Any) -> dict[str, Any] | None:
	if not order_doc.mpesa_payment_id or order_doc.payment_method == "Cash on Delivery":
		return None

	payment_detail = _get_mpesa_payment_detail(order_doc.mpesa_payment_id)
	if not payment_detail:
		return None

	next_status = _map_order_payment_status(order_doc.payment_method, payment_detail.get("status"))
	updates_made = False
	timeline = _extract_order_timeline(order_doc)

	if order_doc.payment_status != next_status:
		order_doc.payment_status = next_status
		event_label, event_detail = _build_payment_status_event(next_status, cstr(payment_detail.get("message")))
		_append_timeline_event(timeline, event_label, event_detail, now_datetime().isoformat())
		updates_made = True

	if next_status in {ORDER_PAYMENT_STATUS_PAID, ORDER_PAYMENT_STATUS_PARTIALLY_PAID} and order_doc.fulfillment_status == "Draft":
		order_doc.fulfillment_status = "Confirmed"
		updates_made = True

	if updates_made:
		order_doc.timeline_json = frappe.as_json(timeline)
		order_doc.flags.ignore_permissions = True
		order_doc.save(ignore_permissions=True)
		frappe.db.commit()

	return payment_detail


def _get_category_map() -> dict[str, dict[str, Any]]:
	if not _doctype_ready("Merchandise Category"):
		return {category["name"]: deepcopy(category) for category in SAMPLE_CATEGORIES}

	category_rows = frappe.get_list(
		"Merchandise Category",
		filters={"is_active": 1},
		fields=["name", "slug", "description", "hero_copy", "accent", "image_url", "featured", "sort_order"],
		order_by="sort_order asc, modified desc",
	)
	return {row["name"]: row for row in category_rows}


def _serialize_sample_item(item: dict[str, Any]) -> dict[str, Any]:
	serialized = deepcopy(item)
	serialized["reviews"] = deepcopy(SAMPLE_REVIEWS.get(item["item_code"], []))
	return serialized


def _serialize_item_doc(doc: Any, category_map: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
	category_map = category_map or _get_category_map()
	category_name = doc.category if getattr(doc, "category", None) else None
	category = category_map.get(category_name or "", {})
	return {
		"item_code": doc.name,
		"slug": doc.slug,
		"item_name": doc.item_name,
		"category_slug": category.get("slug") or "",
		"category_name": category_name or "",
		"short_description": doc.short_description,
		"description": doc.description,
		"selling_price": flt(doc.selling_price),
		"discount_price": flt(doc.discount_price) if doc.discount_price else None,
		"average_rating": flt(doc.average_rating),
		"review_count": int(doc.review_count or 0),
		"image_url": doc.featured_image or "",
		"gallery_urls": _parse_json(doc.gallery_json, []),
		"highlights": _parse_json(doc.highlights_json, []),
		"materials": _parse_json(doc.materials_json, []),
		"badges": _parse_json(doc.badges_json, []),
		"inventory_qty": int(doc.inventory_qty or 0),
		"available_colors": _parse_json(doc.available_colors_json, []),
		"available_sizes": _parse_json(doc.available_sizes_json, []),
		"estimated_dispatch": doc.estimated_dispatch or "",
		"is_featured": bool(doc.is_featured),
		"is_active": bool(doc.is_active),
		"bnpl_eligible": bool(doc.bnpl_eligible),
		"bnpl_min_amount": flt(doc.bnpl_min_amount),
		"reviews": _get_reviews_for_item(doc.name),
	}


def _get_sample_catalog() -> list[dict[str, Any]]:
	return [_serialize_sample_item(item) for item in SAMPLE_ITEMS]


def _get_reviews_for_item(item_code: str) -> list[dict[str, Any]]:
	if not _doctype_ready("Merchandise Review"):
		return deepcopy(SAMPLE_REVIEWS.get(item_code, []))

	reviews = frappe.get_list(
		"Merchandise Review",
		filters={"item_code": item_code, "status": "Approved"},
		fields=[
			"name",
			"customer_name",
			"rating",
			"title",
			"review_text",
			"creation",
			"verified_purchase",
			"helpful_count",
		],
		order_by="creation desc",
	)
	return [
		{
			"id": review["name"],
			"customer_name": review["customer_name"],
			"rating": review["rating"],
			"title": review["title"],
			"review_text": review["review_text"],
			"created_at": _isoformat(review["creation"]),
			"verified_purchase": bool(review["verified_purchase"]),
			"helpful_count": int(review["helpful_count"] or 0),
		}
		for review in reviews
	]


def _get_real_catalog() -> list[dict[str, Any]]:
	if not _doctype_ready("Merchandise Item"):
		return _get_sample_catalog()

	item_rows = frappe.get_list(
		"Merchandise Item",
		filters={"is_active": 1},
		fields=["name"],
		order_by="position_in_category asc, modified desc",
	)
	if not item_rows:
		return _get_sample_catalog()

	category_map = _get_category_map()
	return [_serialize_item_doc(frappe.get_doc("Merchandise Item", row["name"]), category_map) for row in item_rows]


def _filter_catalog(items: list[dict[str, Any]], filters: dict[str, Any]) -> list[dict[str, Any]]:
	search = cstr(filters.get("search")).strip().lower()
	category = cstr(filters.get("category")).strip()
	featured_only = _as_bool(filters.get("featured_only"))
	min_price = flt(filters.get("min_price")) if filters.get("min_price") not in (None, "") else None
	max_price = flt(filters.get("max_price")) if filters.get("max_price") not in (None, "") else None
	sort_by = cstr(filters.get("sort_by")).strip() or "featured"

	filtered = list(items)
	if search:
		filtered = [
			item
			for item in filtered
			if search in " ".join(
				[
					item.get("item_name", ""),
					item.get("short_description", ""),
					item.get("category_name", ""),
					" ".join(item.get("highlights", [])),
				]
			).lower()
		]

	if category:
		filtered = [item for item in filtered if item.get("category_slug") == category]

	if featured_only:
		filtered = [item for item in filtered if item.get("is_featured")]

	if min_price is not None:
		filtered = [item for item in filtered if _public_price(item) >= min_price]

	if max_price is not None:
		filtered = [item for item in filtered if _public_price(item) <= max_price]

	if sort_by == "price-asc":
		filtered.sort(key=_public_price)
	elif sort_by == "price-desc":
		filtered.sort(key=_public_price, reverse=True)
	elif sort_by == "rating":
		filtered.sort(key=lambda item: flt(item.get("average_rating")), reverse=True)
	elif sort_by == "newest":
		filtered.sort(key=lambda item: item.get("item_code", ""), reverse=True)
	else:
		filtered.sort(
			key=lambda item: (
				0 if item.get("is_featured") else 1,
				-flt(item.get("average_rating")),
			)
		)

	return filtered


def _serialize_category_rows(category_map: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
	rows = list(category_map.values())
	rows.sort(key=lambda row: int(row.get("sort_order") or 0))
	return [
		{
			"name": row.get("name"),
			"slug": row.get("slug") or "",
			"description": row.get("description") or "",
			"hero_copy": row.get("hero_copy") or "",
			"accent": row.get("accent") or "",
			"image_url": row.get("image_url") or "",
			"featured": bool(row.get("featured")),
			"sort_order": int(row.get("sort_order") or 0),
		}
		for row in rows
	]


def _validate_coupon(code: str, subtotal: float) -> dict[str, Any]:
	normalized_code = cstr(code).strip().upper()
	rule = deepcopy(COUPON_RULES.get(normalized_code))
	if not rule:
		return {
			"valid": False,
			"code": normalized_code,
			"error": _("Coupon code not recognised."),
		}

	if subtotal < flt(rule.get("min_subtotal")):
		return {
			"valid": False,
			"code": normalized_code,
			"error": _("This code unlocks from KES {0}.").format(int(rule.get("min_subtotal"))),
		}

	return rule


def _calculate_discount(coupon: dict[str, Any] | None, subtotal: float, shipping_amount: float) -> float:
	if not coupon or not coupon.get("valid"):
		return 0.0

	discount_type = coupon.get("discount_type")
	discount_value = flt(coupon.get("discount_value"))

	if discount_type == "shipping":
		return min(shipping_amount, discount_value)
	if discount_type == "flat":
		return min(subtotal, discount_value)
	if discount_type == "percentage":
		calculated = subtotal * discount_value / 100.0
		max_discount = flt(coupon.get("max_discount")) or calculated
		return min(calculated, max_discount)
	return 0.0


def _coerce_items(items: Any) -> list[dict[str, Any]]:
	parsed = _parse_json(items, [])
	if not isinstance(parsed, list):
		frappe.throw(_("Order items must be a list."))
	return parsed


def _hydrate_order_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
	if not _doctype_ready("Merchandise Item"):
		frappe.throw(
			_("Merchandise DocTypes are not installed yet. Keep frontend mock mode enabled until migrations are run.")
		)

	lines: list[dict[str, Any]] = []
	for line in items:
		item_code = cstr(line.get("item_code")).strip()
		quantity = int(line.get("quantity") or 0)
		if not item_code or quantity <= 0:
			frappe.throw(_("Each order line requires an item code and a quantity above zero."))

		item = frappe.get_doc("Merchandise Item", item_code)
		unit_price = flt(item.discount_price or item.selling_price)
		lines.append(
			{
				"item_code": item.name,
				"item_name": item.item_name,
				"quantity": quantity,
				"unit_price": unit_price,
				"selected_color": cstr(line.get("selected_color")).strip() or None,
				"selected_size": cstr(line.get("selected_size")).strip() or None,
				"line_total": unit_price * quantity,
			}
		)
	return lines


def _create_bnpl_plan(order_name: str, total_amount: float) -> str:
	upfront_amount = round(total_amount / BNPL_SPLIT_COUNT, 2)
	remaining_amount = round(total_amount - upfront_amount, 2)
	next_due_date = add_days(now_datetime(), 30)
	plan = frappe.get_doc(
		{
			"doctype": "BNPL Plan",
			"merchandise_order": order_name,
			"upfront_amount": upfront_amount,
			"remaining_amount": remaining_amount,
			"installment_amount": remaining_amount,
			"status": "Awaiting Deposit",
			"schedule_json": frappe.as_json(
				[
					{
						"installment_number": 1,
						"amount": upfront_amount,
						"due_date": _isoformat(now_datetime()),
						"status": "Pending",
					},
					{
						"installment_number": 2,
						"amount": remaining_amount,
						"due_date": _isoformat(next_due_date),
						"status": "Pending",
					},
				]
			),
			"next_due_date": next_due_date,
			"installments_paid": 0,
			"installments_total": BNPL_SPLIT_COUNT,
		}
	)
	plan.insert(ignore_permissions=True)
	return plan.name


def _serialize_bnpl_plan(plan_name: str | None) -> dict[str, Any] | None:
	if not plan_name or not _doctype_ready("BNPL Plan"):
		return None
	plan = frappe.get_doc("BNPL Plan", plan_name)
	return {
		"upfront_amount": flt(plan.upfront_amount),
		"remaining_amount": flt(plan.remaining_amount),
		"installments": _parse_json(plan.schedule_json, []),
	}


def _serialize_order_doc(doc: Any, payment_detail: dict[str, Any] | None = None) -> dict[str, Any]:
	payment_detail = payment_detail or _get_mpesa_payment_detail(doc.mpesa_payment_id)
	return {
		"id": doc.name,
		"order_number": doc.name,
		"customer_name": doc.customer_name,
		"customer_email": doc.customer_email,
		"customer_phone": doc.customer_phone,
		"delivery_address": doc.delivery_address,
		"delivery_city": doc.delivery_city,
		"delivery_notes": doc.delivery_notes,
		"payment_method": doc.payment_method,
		"payment_status": doc.payment_status,
		"fulfillment_status": doc.fulfillment_status,
		"subtotal_amount": flt(doc.subtotal_amount),
		"shipping_amount": flt(doc.shipping_amount),
		"discount_amount": flt(doc.discount_amount),
		"total_amount": flt(doc.total_amount),
		"amount_due_now": flt(doc.amount_due_now),
		"amount_remaining": flt(doc.amount_remaining),
		"coupon_code": doc.coupon_code,
		"mpesa_phone_number": doc.mpesa_phone_number,
		"mpesa_payment_id": doc.mpesa_payment_id,
		"mpesa_ticket_id": payment_detail.get("ticket_id") if payment_detail else None,
		"payment_detail": payment_detail,
		"tracking_number": doc.tracking_number,
		"estimated_delivery_window": doc.estimated_delivery_window,
		"items": _parse_json(doc.items_json, []),
		"timeline": _parse_json(doc.timeline_json, []),
		"bnpl_plan": _serialize_bnpl_plan(doc.bnpl_plan),
		"created_at": _isoformat(doc.creation),
		"updated_at": _isoformat(doc.modified),
	}


@frappe.whitelist(allow_guest=True)
def get_merchandise_categories() -> list[dict[str, Any]]:
	return _serialize_category_rows(_get_category_map())


@frappe.whitelist(allow_guest=True)
def get_merchandise_catalog(
	search: str | None = None,
	category: str | None = None,
	featured_only: str | int | None = None,
	min_price: str | float | None = None,
	max_price: str | float | None = None,
	sort_by: str | None = None,
) -> dict[str, Any]:
	category_map = _get_category_map()
	items = _get_real_catalog()
	filtered = _filter_catalog(
		items,
		{
			"search": search,
			"category": category,
			"featured_only": featured_only,
			"min_price": min_price,
			"max_price": max_price,
			"sort_by": sort_by,
		},
	)
	featured = [item for item in items if item.get("is_featured")][:4]

	return {
		"data": filtered,
		"total": len(filtered),
		"categories": _serialize_category_rows(category_map),
		"featured": featured,
	}


@frappe.whitelist(allow_guest=True)
def get_merchandise_item_details(item_code: str) -> dict[str, Any]:
	normalized_code = cstr(item_code).strip()
	if not normalized_code:
		frappe.throw(_("An item code is required."))

	if not _doctype_ready("Merchandise Item"):
		for item in _get_sample_catalog():
			if item["item_code"] == normalized_code or item["slug"] == normalized_code:
				return item
		frappe.throw(_("Product not found."))

	docname = frappe.db.exists("Merchandise Item", normalized_code) or frappe.db.get_value(
		"Merchandise Item", {"slug": normalized_code}, "name"
	)
	if not docname:
		for item in _get_sample_catalog():
			if item["item_code"] == normalized_code or item["slug"] == normalized_code:
				return item
		frappe.throw(_("Product not found."))

	return _serialize_item_doc(frappe.get_doc("Merchandise Item", docname))


@frappe.whitelist()
def validate_merchandise_coupon(code: str, subtotal: str | float | None = None) -> dict[str, Any]:
	return _validate_coupon(code, flt(subtotal))


@frappe.whitelist()
def create_merchandise_order(
	items: str | list[dict[str, Any]],
	customer_name: str,
	customer_email: str,
	customer_phone: str,
	delivery_address: str,
	delivery_city: str,
	payment_method: str,
	delivery_notes: str | None = None,
	coupon_code: str | None = None,
	mpesa_phone_number: str | None = None,
) -> dict[str, Any]:
	_require_authenticated_user()
	session_email = _get_session_email()
	if not session_email:
		frappe.throw(_("A valid account email is required to place an order."))

	requested_email = cstr(customer_email).strip()
	if _has_read_access("Merchandise Order"):
		customer_email = requested_email or session_email
	else:
		customer_email = session_email

	order_lines = _hydrate_order_items(_coerce_items(items))
	subtotal_amount = sum(flt(line["line_total"]) for line in order_lines)
	shipping_amount = 0.0 if subtotal_amount >= FREE_SHIPPING_THRESHOLD else DEFAULT_SHIPPING_FEE
	coupon = _validate_coupon(coupon_code or "", subtotal_amount) if coupon_code else None
	discount_amount = _calculate_discount(coupon, subtotal_amount, shipping_amount)
	total_amount = max(0.0, subtotal_amount + shipping_amount - discount_amount)

	method = cstr(payment_method).strip() or "MPESA"
	if method not in {"MPESA", "BNPL", "Cash on Delivery"}:
		frappe.throw(_("Unsupported payment method."))

	amount_due_now = round(total_amount / BNPL_SPLIT_COUNT, 2) if method == "BNPL" else total_amount
	amount_remaining = round(total_amount - amount_due_now, 2) if method == "BNPL" else 0.0
	now = now_datetime()
	timeline = [
		{
			"label": "Order created",
			"detail": "We captured your basket and reserved stock for payment confirmation.",
			"happened_at": now.isoformat(),
		},
		{
			"label": "Payment initiated" if method != "Cash on Delivery" else "Awaiting confirmation",
			"detail": (
				"A payment request has been prepared for the selected phone number."
				if method != "Cash on Delivery"
				else "The operations team will verify this cash-on-delivery order before dispatch."
			),
			"happened_at": now.isoformat(),
		},
	]

	order = frappe.get_doc(
		{
			"doctype": "Merchandise Order",
			"customer_name": customer_name,
			"customer_email": customer_email,
			"customer_phone": customer_phone,
			"delivery_address": delivery_address,
			"delivery_city": delivery_city,
			"delivery_notes": delivery_notes,
			"items_json": frappe.as_json(order_lines),
			"payment_method": method,
			"payment_status": ORDER_PAYMENT_STATUS_PENDING if method == "Cash on Delivery" else ORDER_PAYMENT_STATUS_PROMPT_SENT,
			"fulfillment_status": "Draft",
			"subtotal_amount": subtotal_amount,
			"shipping_amount": shipping_amount,
			"discount_amount": discount_amount,
			"total_amount": total_amount,
			"amount_due_now": amount_due_now,
			"amount_remaining": amount_remaining,
			"coupon_code": coupon.get("code") if coupon and coupon.get("valid") else None,
			"mpesa_phone_number": mpesa_phone_number or customer_phone,
			"estimated_delivery_window": "2 to 4 business days",
			"timeline_json": frappe.as_json(timeline),
		}
	)
	order.insert(ignore_permissions=True)

	if method == "BNPL" and _doctype_ready("BNPL Plan"):
		order.bnpl_plan = _create_bnpl_plan(order.name, total_amount)

	if method in {"MPESA", "BNPL"}:
		try:
			payment = initiate_mpesa_payment(
				reference_name=order.name,
				reference_doctype="Merchandise Order",
				phone_number=mpesa_phone_number or customer_phone,
				amount=amount_due_now,
				journey_type="Merchandise Shop",
			)
			order.mpesa_payment_id = payment.get("payment_id")
			order.payment_status = _map_order_payment_status(method, payment.get("status"))

			payment_message = cstr(payment.get("message")).strip()
			ticket_id = cstr(payment.get("ticket_id")).strip()
			if ticket_id:
				masked_phone = _mask_phone_number(mpesa_phone_number or customer_phone)
				_append_timeline_event(
					timeline,
					"MPESA ticket created",
					f"Ticket {ticket_id} created for {masked_phone}.",
				)
			if payment.get("success"):
				_append_timeline_event(
					timeline,
					"STK push requested",
					payment_message or "The MPESA prompt has been sent to the selected phone.",
				)
			else:
				_append_timeline_event(
					timeline,
					"Payment initiation failed",
					payment_message or "The MPESA request was not accepted by the gateway.",
				)
		except Exception as exc:
			frappe.logger().warning(f"Merchandise payment initiation failed for {order.name}: {exc}")
			order.mpesa_payment_id = order.mpesa_payment_id or _find_latest_payment_for_order(order.name)
			order.payment_status = ORDER_PAYMENT_STATUS_FAILED
			_append_timeline_event(
				timeline,
				"Payment initiation failed",
				cstr(exc) or "Unable to initiate MPESA payment.",
			)

		order.timeline_json = frappe.as_json(timeline)

	order.flags.ignore_permissions = True
	order.save(ignore_permissions=True)
	frappe.db.commit()
	payment_detail = _sync_order_payment_from_gateway(order) or _get_mpesa_payment_detail(order.mpesa_payment_id)
	return _serialize_order_doc(order, payment_detail=payment_detail)


@frappe.whitelist()
def get_merchandise_order_status(order_id: str) -> dict[str, Any]:
	_require_authenticated_user()
	order_name = cstr(order_id).strip()
	if not order_name or not _doctype_ready("Merchandise Order"):
		frappe.throw(_("Order not found."))

	order = frappe.get_doc("Merchandise Order", order_name)
	_assert_order_access(order)
	payment_detail = _sync_order_payment_from_gateway(order)
	return _serialize_order_doc(order, payment_detail=payment_detail)


@frappe.whitelist()
def list_merchandise_orders(customer_email: str | None = None) -> list[dict[str, Any]]:
	_require_authenticated_user()
	if not _doctype_ready("Merchandise Order"):
		return []

	session_email = _get_session_email()
	requested_email = cstr(customer_email).strip().lower()
	can_read_all_orders = _has_read_access("Merchandise Order")

	if can_read_all_orders:
		filters = {"customer_email": requested_email} if requested_email else {}
	else:
		if not session_email:
			return []
		if requested_email and requested_email != session_email.lower():
			frappe.throw(_("You do not have permission to list orders for this email."), frappe.PermissionError)
		filters = {"customer_email": session_email}

	order_rows = frappe.get_list(
		"Merchandise Order",
		filters=filters,
		fields=["name"],
		order_by="creation desc",
	)
	if not order_rows:
		return []

	serialized_orders: list[dict[str, Any]] = []
	for row in order_rows:
		order = frappe.get_doc("Merchandise Order", row["name"])
		_assert_order_access(order)
		payment_detail = _sync_order_payment_from_gateway(order)
		serialized_orders.append(_serialize_order_doc(order, payment_detail=payment_detail))
	return serialized_orders


@frappe.whitelist()
def submit_merchandise_review(
	item_code: str,
	order_id: str,
	customer_name: str,
	customer_email: str,
	rating: int,
	title: str,
	review_text: str,
) -> dict[str, Any]:
	_require_authenticated_user()
	if not _doctype_ready("Merchandise Review"):
		frappe.throw(_("Review DocType is not installed yet."))
	if not _doctype_ready("Merchandise Order"):
		frappe.throw(_("Order records are not available."))

	order_name = cstr(order_id).strip()
	if not order_name:
		frappe.throw(_("Order not found."))
	order = frappe.get_doc("Merchandise Order", order_name)
	_assert_order_access(order)

	session_email = _get_session_email()
	if not session_email:
		frappe.throw(_("A valid account email is required to submit reviews."))

	normalized_item_code = cstr(item_code).strip()
	order_items = _parse_json(order.items_json, [])
	if not any(cstr(line.get("item_code")).strip() == normalized_item_code for line in order_items):
		frappe.throw(_("This item is not part of the selected order."), frappe.PermissionError)

	existing = frappe.get_list(
		"Merchandise Review",
		filters={
			"order_id": order.name,
			"item_code": normalized_item_code,
			"customer_email": session_email,
		},
		fields=["name"],
		limit_page_length=1,
	)
	if existing:
		frappe.throw(_("A review for this item and order already exists."))

	review = frappe.get_doc(
		{
			"doctype": "Merchandise Review",
			"item_code": normalized_item_code,
			"order_id": order.name,
			"customer_name": cstr(customer_name).strip() or cstr(order.customer_name).strip(),
			"customer_email": session_email,
			"rating": int(rating),
			"title": title,
			"review_text": review_text,
			"verified_purchase": 1,
			"status": "Pending",
			"helpful_count": 0,
		}
	)
	review.insert(ignore_permissions=True)
	frappe.db.commit()
	return {
		"success": True,
		"name": review.name,
	}
