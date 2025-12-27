"""
ALL_TRAILS Frontend Page

This module provides a Frappe page that serves the Vue 3 frontend application.
The page loads the built frontend assets from the public directory.
"""

import frappe
from frappe import _
from frappe.website.page.page import Page


class AllTrailsPageController(Page):
	"""
	Custom page controller for the ALL_TRAILS frontend.

	This controller serves the Vue 3 frontend application by loading
	the built assets from the public directory.
	"""

	def get_context(self, context):
		"""
		Get context for the ALL_TRAILS frontend page.

		This function is called by Frappe when rendering the page and provides
		the necessary context for the frontend to load.
		"""
		context.no_cache = 1
		context.show_sidebar = False
		context.show_search = False
		context.full_width = True
		return context

