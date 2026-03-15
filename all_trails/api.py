"""
ALL_TRAILS API Module

This module provides API endpoints and utilities for the ALL_TRAILS application.
"""

import json
from pathlib import Path
from urllib.parse import unquote

import frappe
from frappe import _

from all_trails.payments import (
	get_mpesa_payment_status as _get_mpesa_payment_status,
	handle_mpesa_callback as _handle_mpesa_callback,
	initiate_mpesa_payment as _initiate_mpesa_payment,
)
from all_trails.services.blog import (
	create_blog_comment as _create_blog_comment,
	create_blog_post as _create_blog_post,
	get_blog_comments as _get_blog_comments,
	get_blog_post as _get_blog_post,
	get_blog_posts as _get_blog_posts,
)
from all_trails.services.booking import (
	cancel_booking as _cancel_booking,
	create_booking as _create_booking,
	get_booking_detail as _get_booking_detail,
	get_booking_payment_status as _get_booking_payment_status,
	get_user_bookings as _get_user_bookings,
	initiate_booking_payment as _initiate_booking_payment,
)
from all_trails.services.feedback import (
	get_trail_feedback as _get_trail_feedback,
	submit_trail_feedback as _submit_trail_feedback,
)
from all_trails.services.member import register_member as _register_member
from all_trails.services.shop import (
	create_merchandise_order as _create_merchandise_order,
	get_merchandise_catalog as _get_merchandise_catalog,
	get_merchandise_categories as _get_merchandise_categories,
	get_merchandise_item_details as _get_merchandise_item_details,
	get_merchandise_order_status as _get_merchandise_order_status,
	list_merchandise_orders as _list_merchandise_orders,
	submit_merchandise_review as _submit_merchandise_review,
	validate_merchandise_coupon as _validate_merchandise_coupon,
)
from all_trails.services.trail import get_trail_detail as _get_trail_detail, get_trails as _get_trails


DEFAULT_REDIRECT_PATH = "/all-trails/"
_MANIFEST_CACHE: dict[str, object] = {"path": None, "mtime": None, "manifest": None}


def _sanitize_redirect_path(raw_redirect: str | None) -> str:
	"""Allow only local ALL_TRAILS routes to prevent open redirects."""
	if not raw_redirect:
		return DEFAULT_REDIRECT_PATH

	redirect_to = str(raw_redirect).strip()
	try:
		redirect_to = unquote(redirect_to)
	except Exception:
		# Keep original value if decoding fails.
		pass

	lowered = redirect_to.lower()
	if lowered.startswith(("http://", "https://", "//", "javascript:", "data:", "vbscript:")):
		return DEFAULT_REDIRECT_PATH

	if not redirect_to.startswith("/"):
		redirect_to = f"/{redirect_to.lstrip('/')}"

	if redirect_to.startswith("/all-trails"):
		return redirect_to

	return DEFAULT_REDIRECT_PATH


def _sanitize_icon_url(icon_value: str | None) -> str | None:
	"""Return only safe icon URLs for frontend rendering."""
	if not icon_value:
		return None

	icon = str(icon_value).strip()
	if not icon:
		return None

	lowered = icon.lower()
	if lowered.startswith(("javascript:", "data:", "vbscript:")):
		return None

	# Allow only expected URL forms.
	if icon.startswith(("/assets/", "/files/")):
		return icon
	if lowered.startswith(("https://", "http://")):
		return icon

	return None


def _get_manifest_path() -> Path | None:
	app_dir = Path(__file__).parent
	candidate_paths = (
		app_dir / "public" / "frontend" / ".vite" / "manifest.json",
		app_dir / "public" / "frontend" / "manifest.json",
	)
	for candidate in candidate_paths:
		if candidate.exists():
			return candidate
	return None


def _load_manifest() -> dict | None:
	manifest_path = _get_manifest_path()
	if not manifest_path:
		return None

	manifest_mtime = manifest_path.stat().st_mtime
	if (
		_MANIFEST_CACHE.get("path") == str(manifest_path)
		and _MANIFEST_CACHE.get("mtime") == manifest_mtime
		and isinstance(_MANIFEST_CACHE.get("manifest"), dict)
	):
		return _MANIFEST_CACHE["manifest"]  # type: ignore[return-value]

	with manifest_path.open("r", encoding="utf-8") as manifest_file:
		manifest = json.load(manifest_file)

	_MANIFEST_CACHE["path"] = str(manifest_path)
	_MANIFEST_CACHE["mtime"] = manifest_mtime
	_MANIFEST_CACHE["manifest"] = manifest
	return manifest


def _sanitize_asset_path(asset_path: str | None) -> str | None:
	if not asset_path:
		return None

	asset = str(asset_path).strip().lstrip("/")
	lowered = asset.lower()
	if lowered.startswith(("http://", "https://", "//", "javascript:", "data:", "vbscript:")):
		return None

	parts = Path(asset).parts
	if any(part == ".." for part in parts):
		return None

	return asset


@frappe.whitelist(allow_guest=True)
def get_frontend():
	"""
	Serve the ALL_TRAILS frontend application.
	
	This endpoint serves the built Vue 3 frontend application.
	It returns the index.html file with the necessary assets.
	"""
	try:
		# Read the built index.html file
		app_dir = Path(__file__).parent
		frontend_dir = app_dir / "public" / "frontend"
		index_file = frontend_dir / "index.html"
		
		if not index_file.exists():
			frappe.throw(_("Frontend not built. Please run 'bench migrate' to build the frontend."))
		
		with index_file.open("r", encoding="utf-8") as f:
			html_content = f.read()
		
		# Return the HTML content
		frappe.response['message'] = html_content
		frappe.response['type'] = 'html'
		
	except Exception as e:
		frappe.logger().error(f"Error serving frontend: {e}")
		frappe.throw(_("Error loading frontend application"))


@frappe.whitelist(allow_guest=True)
def get_frontend_assets():
	"""
	Get frontend asset hashes from Vite manifest.json
	Returns the correct script and CSS file names for dynamic loading

	Returns:
		dict: Asset file names with hashes
	"""
	try:
		manifest = _load_manifest()
		if not manifest:
			return {
				"success": False,
				"message": "Manifest not found - using fallback",
				"js_file": None,
				"css_file": None
			}

		# Extract entry point (Vite uses index.html or src/main.ts)
		js_file = None
		css_file = None

		# Try different entry point names
		entry_names = ['index.html', 'src/main.ts', 'main.ts', 'src/main.jsx', 'main.jsx']

		for entry_name in entry_names:
			if entry_name in manifest:
				entry = manifest[entry_name]
				if 'file' in entry:
					js_file = entry['file']
				if 'css' in entry and len(entry['css']) > 0:
					css_file = entry['css'][0]
				break

		js_file = _sanitize_asset_path(js_file)
		css_file = _sanitize_asset_path(css_file)

		return {
			"success": True,
			"js_file": js_file,
			"css_file": css_file,
			"base_path": "/assets/all_trails/frontend/"
		}

	except Exception as e:
		frappe.logger().error(f"Error reading frontend manifest: {str(e)}")
		return {
			"success": False,
			"message": "Failed to read frontend asset manifest",
			"js_file": None,
			"css_file": None
		}


@frappe.whitelist(allow_guest=True)
def get_social_login_providers():
	"""
	Get available social login providers for the login page.
	
	Returns:
		dict: List of social login providers with their auth URLs
	"""
	try:
		from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys
		
		providers = frappe.get_all(
			"Social Login Key",
			filters={"enable_social_login": 1},
			fields=["name", "client_id", "base_url", "provider_name", "icon"],
			order_by="name",
		)
		
		provider_logins = []
		redirect_to = _sanitize_redirect_path(frappe.form_dict.get("redirect-to"))
		
		for provider in providers:
			icon = _sanitize_icon_url(provider.icon)
				
			if provider.client_id and provider.base_url and get_oauth_keys(provider.name):
				provider_logins.append({
					"name": provider.name,
					"provider_name": provider.provider_name,
					"auth_url": get_oauth2_authorize_url(provider.name, redirect_to),
					"icon": icon,
				})
		
		return {
			"success": True,
			"providers": provider_logins
		}
	except Exception as e:
		frappe.logger().error(f"Error getting social login providers: {e}")
		return {
			"success": False,
			"providers": []
		}


@frappe.whitelist(allow_guest=True)
def register_member(
	email: str,
	password: str,
	first_name: str,
	last_name: str | None = None,
	phone: str | None = None,
):
	return _register_member(
		email=email,
		password=password,
		first_name=first_name,
		last_name=last_name,
		phone=phone,
		registration_source="Frontend Register",
	)


@frappe.whitelist(allow_guest=True)
def get_trails(
	filters: str | dict | None = None,
	page: int = 1,
	page_size: int = 10,
):
	return _get_trails(filters=filters, page=page, page_size=page_size)


@frappe.whitelist(allow_guest=True)
def get_trail_detail(trail_id: str):
	return _get_trail_detail(trail_id=trail_id)


@frappe.whitelist()
def create_booking(
	trail_id: str,
	spots_booked: int,
	selected_activities: list[dict] | str | None = None,
	idempotency_key: str | None = None,
):
	return _create_booking(
		trail_id=trail_id,
		spots_booked=spots_booked,
		selected_activities=selected_activities,
		idempotency_key=idempotency_key,
	)


@frappe.whitelist()
def get_user_bookings(status: str | None = None):
	return _get_user_bookings(status=status)


@frappe.whitelist()
def get_booking_detail(booking_id: str):
	return _get_booking_detail(booking_id=booking_id)


@frappe.whitelist()
def cancel_booking(booking_id: str, reason: str | None = None):
	return _cancel_booking(booking_id=booking_id, reason=reason)


@frappe.whitelist()
def initiate_booking_payment(
	booking_id: str,
	phone_number: str,
	idempotency_key: str | None = None,
):
	return _initiate_booking_payment(
		booking_id=booking_id,
		phone_number=phone_number,
		idempotency_key=idempotency_key,
	)


@frappe.whitelist()
def get_booking_payment_status(booking_id: str):
	return _get_booking_payment_status(booking_id=booking_id)


@frappe.whitelist(allow_guest=True)
def get_blog_posts(search: str | None = None, page: int = 1, page_size: int = 12):
	return _get_blog_posts(search=search, page=page, page_size=page_size)


@frappe.whitelist(allow_guest=True)
def get_blog_post(slug: str):
	return _get_blog_post(slug=slug)


@frappe.whitelist()
def create_blog_post(
	title: str,
	content: str,
	slug: str | None = None,
	excerpt: str | None = None,
	featured_image: str | None = None,
	published: int | str | None = 0,
):
	return _create_blog_post(
		title=title,
		content=content,
		slug=slug,
		excerpt=excerpt,
		featured_image=featured_image,
		published=published,
	)


@frappe.whitelist(allow_guest=True)
def get_blog_comments(slug: str, page: int = 1, page_size: int = 20):
	return _get_blog_comments(slug=slug, page=page, page_size=page_size)


@frappe.whitelist(allow_guest=True)
def create_blog_comment(
	slug: str,
	content: str,
	comment_by: str | None = None,
	comment_email: str | None = None,
):
	return _create_blog_comment(
		slug=slug,
		content=content,
		comment_by=comment_by,
		comment_email=comment_email,
	)


@frappe.whitelist()
def submit_trail_feedback(
	trail_id: str,
	rating: int,
	feedback_text: str,
	title: str | None = None,
	booking_id: str | None = None,
):
	return _submit_trail_feedback(
		trail_id=trail_id,
		rating=rating,
		feedback_text=feedback_text,
		title=title,
		booking_id=booking_id,
	)


@frappe.whitelist(allow_guest=True)
def get_trail_feedback(trail_id: str, page: int = 1, page_size: int = 10):
	return _get_trail_feedback(trail_id=trail_id, page=page, page_size=page_size)


@frappe.whitelist()
def initiate_mpesa_payment(
	reference_name: str | None = None,
	phone_number: str | None = None,
	amount: float | str | None = None,
	journey_type: str | None = None,
	reference_doctype: str | None = None,
	company: str | None = None,
	metadata: str | dict | None = None,
	**kwargs,
):
	return _initiate_mpesa_payment(
		reference_name=reference_name,
		phone_number=phone_number,
		amount=amount,
		journey_type=journey_type,
		reference_doctype=reference_doctype,
		company=company,
		metadata=metadata,
		**kwargs,
	)


@frappe.whitelist()
def get_mpesa_payment_status(
	payment_id: str | None = None,
	checkout_request_id: str | None = None,
	reference_name: str | None = None,
	reference_doctype: str | None = None,
	**kwargs,
):
	return _get_mpesa_payment_status(
		payment_id=payment_id,
		checkout_request_id=checkout_request_id,
		reference_name=reference_name,
		reference_doctype=reference_doctype,
		**kwargs,
	)


@frappe.whitelist(allow_guest=True)
def handle_mpesa_callback(payload: str | dict | None = None, **kwargs):
	return _handle_mpesa_callback(payload=payload, **kwargs)


@frappe.whitelist(allow_guest=True)
def get_merchandise_categories():
	return _get_merchandise_categories()


@frappe.whitelist(allow_guest=True)
def get_merchandise_catalog(
	search: str | None = None,
	category: str | None = None,
	featured_only: str | int | None = None,
	min_price: str | float | None = None,
	max_price: str | float | None = None,
	sort_by: str | None = None,
):
	return _get_merchandise_catalog(
		search=search,
		category=category,
		featured_only=featured_only,
		min_price=min_price,
		max_price=max_price,
		sort_by=sort_by,
	)


@frappe.whitelist(allow_guest=True)
def get_merchandise_item_details(item_code: str):
	return _get_merchandise_item_details(item_code=item_code)


@frappe.whitelist()
def validate_merchandise_coupon(code: str, subtotal: str | float | None = None):
	return _validate_merchandise_coupon(code=code, subtotal=subtotal)


@frappe.whitelist()
def create_merchandise_order(
	items,
	customer_name: str,
	customer_email: str,
	customer_phone: str,
	delivery_address: str,
	delivery_city: str,
	payment_method: str,
	delivery_notes: str | None = None,
	coupon_code: str | None = None,
	mpesa_phone_number: str | None = None,
):
	return _create_merchandise_order(
		items=items,
		customer_name=customer_name,
		customer_email=customer_email,
		customer_phone=customer_phone,
		delivery_address=delivery_address,
		delivery_city=delivery_city,
		payment_method=payment_method,
		delivery_notes=delivery_notes,
		coupon_code=coupon_code,
		mpesa_phone_number=mpesa_phone_number,
	)


@frappe.whitelist()
def get_merchandise_order_status(order_id: str):
	return _get_merchandise_order_status(order_id=order_id)


@frappe.whitelist()
def list_merchandise_orders(customer_email: str | None = None):
	return _list_merchandise_orders(customer_email=customer_email)


@frappe.whitelist()
def submit_merchandise_review(
	item_code: str,
	order_id: str,
	customer_name: str,
	customer_email: str,
	rating: int,
	title: str,
	review_text: str,
):
	return _submit_merchandise_review(
		item_code=item_code,
		order_id=order_id,
		customer_name=customer_name,
		customer_email=customer_email,
		rating=rating,
		title=title,
		review_text=review_text,
	)
