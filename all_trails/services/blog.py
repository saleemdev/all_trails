from __future__ import annotations

import math
from typing import Any

import frappe
from frappe import _
from frappe.utils import cint, cstr
from frappe.utils.data import strip_html
from frappe.utils.html_utils import sanitize_html

from all_trails.services.common import (
	ROLE_BLOGGER,
	ROLE_TRAIL_MEMBER,
	enforce_ip_session_rate_limit,
	ensure_authenticated_user,
	require_roles,
	slugify,
)


DEFAULT_BLOG_CATEGORY = "Trail Stories"



def _safe_excerpt(content: str, *, fallback: str | None = None, max_len: int = 240) -> str:
	base = cstr(fallback or "").strip()
	if not base:
		base = strip_html(cstr(content or ""))
	base = " ".join(base.split())
	if len(base) <= max_len:
		return base
	return f"{base[: max_len - 1].rstrip()}…"



def _compute_read_time_minutes(content: str) -> int:
	words = len(strip_html(cstr(content or "")).split())
	if words <= 0:
		return 1
	return max(1, math.ceil(words / 220))



def _route_for_slug(slug: str) -> str:
	slug = slugify(slug)
	if not slug:
		frappe.throw(_("A valid slug is required"))
	if slug.startswith("all-trails"):
		frappe.throw(_("Slug conflicts with reserved app routes"))
	return f"blog/{slug}"



def _get_web_page_by_slug(slug: str, *, only_published: bool = True):
	route = _route_for_slug(slug)
	filters: dict[str, Any] = {"route": route}
	if only_published:
		filters["published"] = 1
	name = frappe.db.get_value("Web Page", filters, "name")
	if not name:
		frappe.throw(_("Blog post not found"), frappe.DoesNotExistError)
	return frappe.get_doc("Web Page", name)



def _serialize_post(web_page) -> dict[str, Any]:
	content = cstr(web_page.main_section_html or web_page.main_section or web_page.main_section_md or "")
	slug = web_page.route.split("blog/")[-1] if web_page.route and "blog/" in web_page.route else web_page.route
	author_name = frappe.db.get_value("User", web_page.owner, "full_name") or web_page.owner

	return {
		"id": web_page.name,
		"name": web_page.name,
		"title": web_page.title,
		"slug": slug,
		"route": web_page.route,
		"excerpt": _safe_excerpt(content, fallback=web_page.meta_description),
		"content": content,
		"featured_image": web_page.meta_image,
		"author": author_name,
		"author_email": web_page.owner,
		"category": DEFAULT_BLOG_CATEGORY,
		"tags": [],
		"published_date": web_page.creation,
		"read_time": _compute_read_time_minutes(content),
		"status": "Published" if cint(web_page.published) == 1 else "Draft",
		"created_at": web_page.creation,
		"updated_at": web_page.modified,
	}



def get_blog_posts(search: str | None = None, page: int = 1, page_size: int = 12):
	page_no = max(cint(page), 1)
	limit = min(max(cint(page_size), 1), 100)

	filters = {"published": 1}
	rows = frappe.get_all(
		"Web Page",
		filters=filters,
		fields=[
			"name",
			"title",
			"route",
			"owner",
			"meta_description",
			"meta_image",
			"main_section_html",
			"main_section",
			"main_section_md",
			"creation",
			"modified",
			"published",
		],
		order_by="creation desc",
	)

	search_term = cstr(search or "").strip().lower()
	blog_rows = [row for row in rows if row.route and row.route.startswith("blog/")]
	if search_term:
		blog_rows = [
			row
			for row in blog_rows
			if search_term in cstr(row.title).lower()
			or search_term in cstr(row.meta_description).lower()
			or search_term in strip_html(cstr(row.main_section_html or row.main_section or row.main_section_md or "")).lower()
		]

	total = len(blog_rows)
	start = (page_no - 1) * limit
	selected = blog_rows[start : start + limit]

	data = [_serialize_post(frappe._dict(row)) for row in selected]
	return {
		"data": data,
		"total": total,
		"page": page_no,
		"page_size": limit,
	}



def get_blog_post(slug: str):
	web_page = _get_web_page_by_slug(slug, only_published=True)
	return _serialize_post(web_page)



def create_blog_post(
	title: str,
	content: str,
	slug: str | None = None,
	excerpt: str | None = None,
	featured_image: str | None = None,
	published: int | str | None = 0,
):
	ensure_authenticated_user()
	require_roles([ROLE_TRAIL_MEMBER, ROLE_BLOGGER], require_all=True)

	title = cstr(title).strip()
	if not title:
		frappe.throw(_("Title is required"))

	clean_content = sanitize_html(cstr(content or ""), always_sanitize=True)
	if not strip_html(clean_content).strip():
		frappe.throw(_("Content is required"))

	effective_slug = slugify(slug or title)
	route = _route_for_slug(effective_slug)
	if frappe.db.exists("Web Page", {"route": route}):
		frappe.throw(_("A blog post with this slug already exists"))

	if route.startswith("all-trails/"):
		frappe.throw(_("Route conflicts with application routes"))

	doc = frappe.get_doc(
		{
			"doctype": "Web Page",
			"title": title,
			"route": route,
			"published": cint(published),
			"content_type": "HTML",
			"main_section_html": clean_content,
			"meta_description": _safe_excerpt(clean_content, fallback=excerpt, max_len=160),
			"meta_image": cstr(featured_image).strip() or None,
			"enable_comments": 0,
			"show_title": 0,
		}
	)
	doc.flags.ignore_permissions = True
	doc.insert(ignore_permissions=True)
	frappe.db.commit()
	return _serialize_post(doc)



def get_blog_comments(slug: str, page: int = 1, page_size: int = 20):
	web_page = _get_web_page_by_slug(slug, only_published=True)
	page_no = max(cint(page), 1)
	limit = min(max(cint(page_size), 1), 100)

	filters = {
		"reference_doctype": "Web Page",
		"reference_name": web_page.name,
		"comment_type": "Comment",
		"published": 1,
	}
	rows = frappe.get_all(
		"Comment",
		filters=filters,
		fields=["name", "comment_by", "comment_email", "content", "creation"],
		order_by="creation asc",
		start=(page_no - 1) * limit,
		limit=limit,
	)
	total = frappe.db.count("Comment", filters=filters)

	data = [
		{
			"id": row.name,
			"author": row.comment_by,
			"email": row.comment_email,
			"content": sanitize_html(cstr(row.content or ""), always_sanitize=True),
			"created_at": row.creation,
		}
		for row in rows
	]

	return {
		"data": data,
		"total": total,
		"page": page_no,
		"page_size": limit,
	}



def create_blog_comment(
	slug: str,
	content: str,
	comment_by: str | None = None,
	comment_email: str | None = None,
):
	enforce_ip_session_rate_limit("blog_comment", limit=8, window_seconds=60)
	web_page = _get_web_page_by_slug(slug, only_published=True)

	clean_content = sanitize_html(cstr(content or ""), always_sanitize=True)
	if not strip_html(clean_content).strip():
		frappe.throw(_("Comment content is required"))

	if frappe.session.user != "Guest":
		user = frappe.get_doc("User", frappe.session.user)
		resolved_name = user.full_name or user.first_name or user.name
		resolved_email = user.email or user.name
	else:
		resolved_name = cstr(comment_by).strip() or _("Guest")
		resolved_email = cstr(comment_email).strip() or None

	comment = frappe.get_doc(
		{
			"doctype": "Comment",
			"comment_type": "Comment",
			"reference_doctype": "Web Page",
			"reference_name": web_page.name,
			"comment_by": resolved_name,
			"comment_email": resolved_email,
			"content": clean_content,
			"published": 0,
			"ip_address": cstr(getattr(frappe.local, "request_ip", "")),
		}
	)
	comment.insert(ignore_permissions=True)
	frappe.db.commit()

	return {
		"success": True,
		"message": _("Comment submitted and pending moderation"),
		"comment_id": comment.name,
		"published": 0,
	}
