"""
ALL_TRAILS Path Resolver

This module provides a custom path resolver for the ALL_TRAILS frontend.
It ensures that all routes under /all-trails/* are handled by the Vue Router
by serving the same template for all paths.
"""

import frappe
from frappe.website.path_resolver import resolve_path


def resolve_all_trails_path(path):
	"""
	Custom path resolver for ALL_TRAILS frontend routes.
	
	This function catches ALL paths starting with 'all-trails' and returns
	the 'all-trails' endpoint so that the same template is served for all
	client-side routes, allowing Vue Router to handle the routing.
	
	This fixes the 404 issue when reloading on ANY route under /all-trails/*
	including:
	- /all-trails/
	- /all-trails/trails
	- /all-trails/trails/123
	- /all-trails/bookings
	- /all-trails/bookings/456
	- /all-trails/profile
	- /all-trails/blog
	- /all-trails/blog/some-slug
	- /all-trails/gallery/789
	- Any other route under /all-trails/*
	
	Args:
		path: The request path (e.g., 'all-trails', 'all-trails/trails', 'all-trails/trails/123')
	
	Returns:
		str: The endpoint 'all-trails' if path starts with 'all-trails',
		     otherwise calls Frappe's resolve_path to handle the path normally.
		     ALWAYS returns a string, never None.
	"""
	# CRITICAL: Always return a string, never None
	# Handle None or empty path
	if not path:
		try:
			result = resolve_path(path or '')
			# Ensure result is not None
			return result if result else 'index'
		except Exception:
			# If resolve_path fails, return 'index' as safe fallback
			return 'index'
	
	# Ensure path is a string
	if not isinstance(path, str):
		try:
			result = resolve_path(str(path))
			# Ensure result is not None
			return result if result else 'index'
		except Exception:
			return 'index'
	
	# Normalize path - remove leading/trailing slashes and whitespace
	normalized_path = path.strip('/').strip()
	
	# Check if path is exactly 'all-trails' or starts with 'all-trails/'
	# This catches ALL routes under /all-trails/* including nested routes
	if normalized_path == 'all-trails' or normalized_path.startswith('all-trails/'):
		# Return 'all-trails' endpoint for ALL sub-routes
		# This ensures the same template is served, allowing Vue Router to handle ALL routing
		return 'all-trails'
	
	# For all other paths, use Frappe's standard path resolution
	# This ensures paths like 'app/login' are handled correctly
	try:
		result = resolve_path(path)
		# CRITICAL: Ensure we never return None
		if result is None:
			# If resolve_path returns None (shouldn't happen, but be safe), return the path or 'index'
			return path if path else 'index'
		return result
	except Exception:
		# If resolve_path fails, return the original path as fallback (or 'index' if path is empty)
		# This should rarely happen, but prevents crashes
		return path if path else 'index'

