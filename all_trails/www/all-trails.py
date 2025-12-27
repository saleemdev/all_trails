"""
ALL_TRAILS Frontend Route Handler

This module handles the /all-trails route and serves the Vue 3 frontend application.
"""

import frappe
from frappe import _

def get_context(context):
	"""
	Get context for the all-trails page.
	
	This function is called by Frappe when rendering the all-trails.html template.
	It provides the necessary context variables for the template.
	"""
	context.no_cache = 1
	context.show_sidebar = False
	
	return context

