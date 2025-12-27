import os
import subprocess
import shutil
import re
import sys
import frappe

def before_build():
	"""Build frontend assets before Frappe build process"""
	try:
		call_frontend_build_script()
	except Exception as e:
		frappe.log_error(f"Frontend build failed: {str(e)}", "ALL_TRAILS Build Error")
		print(f"Warning: Frontend build failed: {str(e)}")

def after_build():
	"""Post-build cleanup and verification"""
	try:
		verify_build_assets()
	except Exception as e:
		frappe.log_error(f"Build verification failed: {str(e)}", "ALL_TRAILS Build Verification")
		print(f"Warning: Build verification failed: {str(e)}")

def call_frontend_build_script():
	"""Call the frontend/build.py script to build and update assets"""
	# Get the app path - frappe.get_app_path returns the app directory
	# which is the all_trails subdirectory, so we need to go up one level
	try:
		app_path = frappe.get_app_path("all_trails")
		# Go up one level to get the actual app root
		app_path = os.path.dirname(app_path)
	except:
		# Fallback: use the parent directory of this file
		app_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

	build_script = os.path.join(app_path, "frontend", "build.py")

	if not os.path.exists(build_script):
		print(f"Frontend build script not found at {build_script}")
		print(f"App path: {app_path}")
		print(f"Available files: {os.listdir(app_path) if os.path.exists(app_path) else 'N/A'}")
		return

	print("=" * 60)
	print("Executing frontend build script...")
	print("=" * 60)

	try:
		# Execute the build.py script using the current Python interpreter
		result = subprocess.run(
			[sys.executable, build_script],
			capture_output=True,
			text=True,
			check=False
		)

		# Print the output
		if result.stdout:
			print(result.stdout)
		if result.stderr:
			print(result.stderr)

		# Check if build was successful
		if result.returncode != 0:
			raise Exception(f"Frontend build script failed with return code {result.returncode}")

		print("=" * 60)
		print("Frontend build script completed successfully")
		print("=" * 60)

	except Exception as e:
		raise Exception(f"Failed to execute frontend build script: {e}")

def verify_build_assets():
	"""Verify that build assets exist and are properly referenced"""
	app_path = frappe.get_app_path("all_trails")

	# Check if assets directory exists
	assets_dir = os.path.join(app_path, "public", "frontend", "assets")
	if not os.path.exists(assets_dir):
		raise Exception("Assets directory not found after build")

	# Check if HTML file exists
	html_file = os.path.join(app_path, "www", "all-trails.html")
	if not os.path.exists(html_file):
		raise Exception("HTML file not found in www directory")

	# Verify asset references in HTML
	with open(html_file, 'r') as f:
		html_content = f.read()

	# Extract asset references
	js_matches = re.findall(r'src="[^"]*assets/([^"]*\.js)"', html_content)
	css_matches = re.findall(r'href="[^"]*assets/([^"]*\.css)"', html_content)

	# Check if referenced assets exist
	for js_file in js_matches:
		js_path = os.path.join(assets_dir, js_file)
		if not os.path.exists(js_path):
			raise Exception(f"Referenced JS file not found: {js_file}")

	for css_file in css_matches:
		css_path = os.path.join(assets_dir, css_file)
		if not os.path.exists(css_path):
			raise Exception(f"Referenced CSS file not found: {css_file}")

	print("Build verification completed successfully")

def run_frontend_build():
	"""
	Run frontend build after migration.
	This ensures the frontend assets are always up-to-date after database migrations.
	Errors are logged but don't fail the migration.

	This function is called as a Frappe after_migrate hook and directly invokes
	the existing call_frontend_build_script() function.
	"""
	try:
		frappe.logger().info("Starting ALL_TRAILS frontend build after migration...")

		# Call the existing frontend build script function
		# This function handles all the build logic and error reporting
		call_frontend_build_script()

		frappe.logger().info("ALL_TRAILS frontend build completed successfully after migration")

	except Exception as e:
		# Log the error but don't fail the migration
		frappe.log_error(
			f"Frontend build failed after migration: {str(e)}",
			"ALL_TRAILS Post-Migration Build Error"
		)

