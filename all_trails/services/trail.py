from __future__ import annotations

from typing import Any

import frappe
from frappe import _
from frappe.utils import cint, cstr, flt

from all_trails.services.common import parse_json_input


TRAIL_LIST_FIELDS = [
	"name",
	"title",
	"slug",
	"description",
	"difficulty_level",
	"trail_type",
	"location",
	"latitude",
	"longitude",
	"county",
	"distance_km",
	"elevation_gain_m",
	"duration_hours",
	"scheduled_date",
	"start_time",
	"end_time",
	"meeting_point",
	"meeting_time",
	"meeting_notes",
	"meeting_point_maps_url",
	"terrain_summary",
	"trail_highlights",
	"altitude_start_m",
	"altitude_max_m",
	"fitness_level",
	"water_requirement_litres",
	"transport_notes",
	"packing_list",
	"safety_notes",
	"inclusions",
	"exclusions",
	"best_season",
	"max_capacity",
	"available_spots",
	"price_kshs",
	"host",
	"featured_image",
	"route_geojson",
	"status",
	"published",
	"is_long_weekend",
	"creation",
	"modified",
]



def _sanitize_public_asset(value: str | None) -> str | None:
	if not value:
		return None
	url = cstr(value).strip()
	if not url:
		return None
	low = url.lower()
	if low.startswith(("javascript:", "data:", "vbscript:")):
		return None
	if url.startswith(("/assets/", "/files/", "http://", "https://")):
		return url
	if url.startswith("/"):
		return url
	return None


def _sanitize_reference_url(value: str | None) -> str | None:
	if not value:
		return None
	url = cstr(value).strip()
	if not url:
		return None
	low = url.lower()
	if low.startswith(("javascript:", "data:", "vbscript:")):
		return None
	if low.startswith(("http://", "https://")):
		return url
	return None


def _serialize_activities(trail_name: str) -> list[dict[str, Any]]:
	activities = frappe.get_all(
		"Trail Activity",
		filters={"parent": trail_name, "parenttype": "Trail", "parentfield": "activities"},
		fields=[
			"name",
			"activity_name",
			"description",
			"price_kshs",
			"icon",
			"available",
			"requires_booking",
			"max_participants",
			"available_spots",
		],
		order_by="idx asc",
	)

	serialized: list[dict[str, Any]] = []
	for row in activities:
		serialized.append(
			{
				"id": row.name,
				"name": row.activity_name,
				"description": row.description,
				"price_kshs": flt(row.price_kshs),
				"icon": row.icon,
				"available": cint(row.available) == 1,
				"requires_booking": cint(row.requires_booking) == 1,
				"max_participants": cint(row.max_participants) if row.max_participants is not None else None,
				"available_spots": cint(row.available_spots) if row.available_spots is not None else None,
			}
		)
	return serialized


def serialize_trail(row: dict[str, Any], *, include_activities: bool = True) -> dict[str, Any]:
	trail = {
		"id": row.name,
		"name": row.name,
		"title": row.title,
		"slug": row.slug,
		"description": row.description,
		"difficulty_level": row.difficulty_level,
		"trail_type": row.trail_type,
		"location": row.location,
		"latitude": flt(row.latitude) if row.latitude is not None else None,
		"longitude": flt(row.longitude) if row.longitude is not None else None,
		"coordinates": {
			"lat": flt(row.latitude),
			"lng": flt(row.longitude),
		} if row.latitude is not None and row.longitude is not None else None,
		"county": row.county,
		"distance_km": flt(row.distance_km),
		"elevation_gain_m": cint(row.elevation_gain_m),
		"duration_hours": flt(row.duration_hours),
		"scheduled_date": row.scheduled_date,
		"start_time": row.start_time,
		"end_time": row.end_time,
		"meeting_point": row.meeting_point,
		"meeting_time": row.meeting_time,
		"meeting_notes": row.meeting_notes,
		"meeting_point_maps_url": _sanitize_reference_url(row.meeting_point_maps_url),
		"terrain_summary": row.terrain_summary,
		"trail_highlights": row.trail_highlights,
		"altitude_start_m": cint(row.altitude_start_m) if row.altitude_start_m is not None else None,
		"altitude_max_m": cint(row.altitude_max_m) if row.altitude_max_m is not None else None,
		"fitness_level": row.fitness_level,
		"water_requirement_litres": flt(row.water_requirement_litres) if row.water_requirement_litres is not None else None,
		"transport_notes": row.transport_notes,
		"packing_list": row.packing_list,
		"safety_notes": row.safety_notes,
		"inclusions": row.inclusions,
		"exclusions": row.exclusions,
		"best_season": row.best_season,
		"max_capacity": cint(row.max_capacity),
		"available_spots": cint(row.available_spots),
		"price_kshs": flt(row.price_kshs),
		"host": row.host,
		"featured_image": _sanitize_public_asset(row.featured_image),
		"route_geojson": row.route_geojson,
		"status": row.status,
		"published": cint(row.published) == 1,
		"is_long_weekend": cint(row.is_long_weekend) == 1,
		"created_at": row.creation,
		"updated_at": row.modified,
	}
	if include_activities:
		trail["extra_activities"] = _serialize_activities(row.name)
	return trail


def get_trails(filters: str | dict[str, Any] | None = None, page: int = 1, page_size: int = 10):
	page_no = max(cint(page), 1)
	limit = min(max(cint(page_size), 1), 100)
	parsed_filters = parse_json_input(filters, {}) or {}

	where = {
		"published": 1,
	}

	difficulty = cstr(parsed_filters.get("difficulty_level") or "").strip()
	if difficulty:
		where["difficulty_level"] = difficulty

	status = cstr(parsed_filters.get("status") or "").strip()
	if status:
		where["status"] = status
	else:
		where["status"] = ["!=", "Cancelled"]

	search = cstr(parsed_filters.get("search") or "").strip()

	if search:
		search_clause = " and (title like %(search)s or location like %(search)s or description like %(search)s)"
	else:
		search_clause = ""

	conditions = ["published = 1"]
	params: dict[str, Any] = {}

	if where.get("status"):
		status_filter = where["status"]
		if isinstance(status_filter, list):
			conditions.append("status != %(status_not)s")
			params["status_not"] = status_filter[1]
		else:
			conditions.append("status = %(status)s")
			params["status"] = status_filter
	if difficulty:
		conditions.append("difficulty_level = %(difficulty)s")
		params["difficulty"] = difficulty
	if parsed_filters.get("min_price") is not None:
		conditions.append("price_kshs >= %(min_price)s")
		params["min_price"] = flt(parsed_filters.get("min_price"))
	if parsed_filters.get("max_price") is not None:
		conditions.append("price_kshs <= %(max_price)s")
		params["max_price"] = flt(parsed_filters.get("max_price"))
	if parsed_filters.get("date_from"):
		conditions.append("scheduled_date >= %(date_from)s")
		params["date_from"] = parsed_filters.get("date_from")
	if parsed_filters.get("date_to"):
		conditions.append("scheduled_date <= %(date_to)s")
		params["date_to"] = parsed_filters.get("date_to")
	if search:
		params["search"] = f"%{search}%"

	where_sql = " and ".join(conditions)
	if search_clause:
		where_sql = f"{where_sql}{search_clause}"

	count_row = frappe.db.sql(
		f"""
			select count(*) as total
			from `tabTrail`
			where {where_sql}
		""",
		params,
		as_dict=True,
	)
	total = cint(count_row[0].total if count_row else 0)

	rows = frappe.db.sql(
		f"""
			select
				name, title, slug, description, difficulty_level, trail_type, location, latitude, longitude, county,
				distance_km, elevation_gain_m, duration_hours, scheduled_date,
				start_time, end_time, meeting_point, meeting_time, meeting_notes, meeting_point_maps_url,
				terrain_summary, trail_highlights, altitude_start_m, altitude_max_m,
				fitness_level, water_requirement_litres, transport_notes, packing_list,
				safety_notes, inclusions, exclusions, best_season,
				max_capacity, available_spots, price_kshs,
				host, featured_image, route_geojson, status, published,
				is_long_weekend, creation, modified
			from `tabTrail`
			where {where_sql}
			order by scheduled_date asc, creation desc
			limit %(limit)s offset %(offset)s
		""",
		{**params, "limit": limit, "offset": (page_no - 1) * limit},
		as_dict=True,
	)

	return {
		"data": [serialize_trail(row, include_activities=True) for row in rows],
		"total": total,
		"page": page_no,
		"page_size": limit,
	}


def get_trail_detail(trail_id: str) -> dict[str, Any]:
	if not trail_id:
		frappe.throw(_("Trail ID is required"))
	if not frappe.db.exists("Trail", trail_id):
		frappe.throw(_("Trail not found"))

	trail = frappe.db.get_value(
		"Trail",
		trail_id,
		TRAIL_LIST_FIELDS,
		as_dict=True,
	)
	if not trail:
		frappe.throw(_("Trail not found"))

	if cint(trail.published) != 1:
		frappe.throw(_("Trail not found"), frappe.DoesNotExistError)

	return serialize_trail(trail, include_activities=True)
