from __future__ import annotations

import json
from typing import Any

import frappe
from frappe import _
from frappe.utils import cstr, getdate

from all_trails.services.common import ensure_authenticated_user

OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_CACHE_SECONDS = 60 * 60 * 6
GEOCODE_CACHE_SECONDS = 60 * 60 * 24


def _safe_float(value: Any) -> float | None:
	try:
		if value is None or value == "":
			return None
		return float(value)
	except Exception:
		return None


def _flatten_geojson_coordinates(node: Any, acc: list[tuple[float, float]]) -> None:
	"""Extract (lat, lng) points from nested GeoJSON coordinate arrays."""
	if isinstance(node, (list, tuple)):
		if len(node) >= 2 and isinstance(node[0], (int, float)) and isinstance(node[1], (int, float)):
			# GeoJSON coordinate order is [lng, lat]
			acc.append((float(node[1]), float(node[0])))
			return
		for child in node:
			_flatten_geojson_coordinates(child, acc)


def _coordinates_from_route_geojson(route_geojson: Any) -> tuple[float, float] | None:
	if not route_geojson:
		return None

	payload = route_geojson
	if isinstance(route_geojson, str):
		try:
			payload = json.loads(route_geojson)
		except Exception:
			return None

	if not isinstance(payload, dict):
		return None

	points: list[tuple[float, float]] = []

	if payload.get("type") == "FeatureCollection":
		for feature in payload.get("features") or []:
			if isinstance(feature, dict):
				_flatten_geojson_coordinates((feature.get("geometry") or {}).get("coordinates"), points)
	elif payload.get("type") == "Feature":
		_flatten_geojson_coordinates((payload.get("geometry") or {}).get("coordinates"), points)
	else:
		_flatten_geojson_coordinates(payload.get("coordinates"), points)

	if not points:
		return None

	lat = sum(lat for lat, _ in points) / len(points)
	lng = sum(lng for _, lng in points) / len(points)
	return (round(lat, 6), round(lng, 6))


def _geocode_location(location: str) -> tuple[float, float] | None:
	normalized = cstr(location or "").strip().lower()
	if not normalized:
		return None

	cache_key = f"all_trails:weather:geocode:{normalized}"
	cached = frappe.cache.get_value(cache_key)
	if cached:
		try:
			lat, lng = json.loads(cached)
			return float(lat), float(lng)
		except Exception:
			pass

	try:
		response = frappe.make_get_request(
			OPEN_METEO_GEOCODING_URL,
			params={
				"name": location,
				"count": 1,
				"language": "en",
				"format": "json",
				"country": "KE",
			},
		)
	except Exception:
		return None
	results = (response or {}).get("results") or []
	if not results:
		return None

	lat = _safe_float(results[0].get("latitude"))
	lng = _safe_float(results[0].get("longitude"))
	if lat is None or lng is None:
		return None

	coords = (round(lat, 6), round(lng, 6))
	frappe.cache.set_value(cache_key, json.dumps(coords), expires_in_sec=GEOCODE_CACHE_SECONDS)
	return coords


def _resolve_trail_coordinates(trail_doc) -> tuple[float, float] | None:
	route_coords = _coordinates_from_route_geojson(getattr(trail_doc, "route_geojson", None))
	if route_coords:
		return route_coords
	return _geocode_location(getattr(trail_doc, "location", None))


def _weather_label_from_code(weather_code: int | None) -> str:
	labels = {
		0: "Clear sky",
		1: "Mostly clear",
		2: "Partly cloudy",
		3: "Overcast",
		45: "Fog",
		48: "Depositing rime fog",
		51: "Light drizzle",
		53: "Moderate drizzle",
		55: "Dense drizzle",
		61: "Slight rain",
		63: "Moderate rain",
		65: "Heavy rain",
		71: "Slight snow",
		73: "Moderate snow",
		75: "Heavy snow",
		80: "Rain showers",
		81: "Moderate rain showers",
		82: "Violent rain showers",
		95: "Thunderstorm",
		96: "Thunderstorm with hail",
		99: "Severe thunderstorm with hail",
	}
	return labels.get(weather_code or -1, "Weather update")


def _risk_from_metrics(
	*,
	weather_code: int | None,
	precip_probability_max: float | None,
	wind_gusts_10m_max: float | None,
	uv_index_max: float | None,
) -> tuple[str, str]:
	precip = precip_probability_max or 0
	gust = wind_gusts_10m_max or 0
	uv = uv_index_max or 0

	severe_codes = {65, 75, 82, 95, 96, 99}
	if (weather_code in severe_codes) or precip >= 70 or gust >= 40:
		return ("risky", "Risky")
	if precip >= 35 or gust >= 28 or uv >= 8:
		return ("caution", "Caution")
	return ("good", "Good")


def _fetch_forecast_for_date(lat: float, lng: float, date_iso: str) -> dict[str, Any] | None:
	cache_key = f"all_trails:weather:forecast:{lat}:{lng}:{date_iso}"
	cached = frappe.cache.get_value(cache_key)
	if cached:
		try:
			return json.loads(cached)
		except Exception:
			pass

	try:
		response = frappe.make_get_request(
			OPEN_METEO_FORECAST_URL,
			params={
				"latitude": lat,
				"longitude": lng,
				"timezone": "auto",
				"start_date": date_iso,
				"end_date": date_iso,
				"daily": (
					"weather_code,temperature_2m_max,temperature_2m_min,"
					"precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,"
					"uv_index_max,sunrise,sunset"
				),
			},
		)
	except Exception:
		return None

	daily = (response or {}).get("daily") or {}
	if not daily:
		return None

	weather_code = int((daily.get("weather_code") or [None])[0]) if (daily.get("weather_code") or [None])[0] is not None else None
	temp_max = _safe_float((daily.get("temperature_2m_max") or [None])[0])
	temp_min = _safe_float((daily.get("temperature_2m_min") or [None])[0])
	precip = _safe_float((daily.get("precipitation_probability_max") or [None])[0])
	wind_speed = _safe_float((daily.get("wind_speed_10m_max") or [None])[0])
	wind_gusts = _safe_float((daily.get("wind_gusts_10m_max") or [None])[0])
	uv_index = _safe_float((daily.get("uv_index_max") or [None])[0])
	sunrise = (daily.get("sunrise") or [None])[0]
	sunset = (daily.get("sunset") or [None])[0]

	risk_key, risk_label = _risk_from_metrics(
		weather_code=weather_code,
		precip_probability_max=precip,
		wind_gusts_10m_max=wind_gusts,
		uv_index_max=uv_index,
	)

	payload = {
		"date": date_iso,
		"weather_code": weather_code,
		"summary": _weather_label_from_code(weather_code),
		"risk_level": risk_key,
		"risk_label": risk_label,
		"temperature_max_c": temp_max,
		"temperature_min_c": temp_min,
		"precipitation_probability_max": precip,
		"wind_speed_10m_max_kmh": wind_speed,
		"wind_gusts_10m_max_kmh": wind_gusts,
		"uv_index_max": uv_index,
		"sunrise": sunrise,
		"sunset": sunset,
		"coordinates": {"lat": lat, "lng": lng},
	}
	frappe.cache.set_value(cache_key, json.dumps(payload), expires_in_sec=WEATHER_CACHE_SECONDS)
	return payload


def get_trail_weather(trail_id: str) -> dict[str, Any]:
	if not trail_id:
		frappe.throw(_("Trail ID is required"))
	if not frappe.db.exists("Trail", trail_id):
		frappe.throw(_("Trail not found"))

	try:
		trail = frappe.get_doc("Trail", trail_id)
		date_iso = cstr(getdate(trail.scheduled_date))
		coords = _resolve_trail_coordinates(trail)

		if not coords:
			return {
				"available": False,
				"message": _("Weather is unavailable for this trail location"),
				"date": date_iso,
			}

		payload = _fetch_forecast_for_date(coords[0], coords[1], date_iso)
		if not payload:
			return {
				"available": False,
				"message": _("Weather forecast is currently unavailable"),
				"date": date_iso,
			}

		return {"available": True, **payload}
	except Exception:
		return {
			"available": False,
			"message": _("Weather forecast is currently unavailable"),
			"date": "",
		}


def get_booking_weather(booking_id: str) -> dict[str, Any]:
	ensure_authenticated_user()
	if not booking_id:
		frappe.throw(_("Booking ID is required"))
	if not frappe.db.exists("Trail Booking", booking_id):
		frappe.throw(_("Booking not found"))

	booking = frappe.get_doc("Trail Booking", booking_id)
	if frappe.session.user != "Administrator" and booking.user != frappe.session.user:
		frappe.throw(_("You are not allowed to access this booking"), frappe.PermissionError)

	return get_trail_weather(booking.trail)
