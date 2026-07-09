import os
import shutil

import frappe


def copy_seed_files():
	"""Copy bundled demo media (course covers, lesson PDFs) into this site's
	public files folder so records restored from fixtures don't end up with
	broken attachment links on a fresh install."""
	app_path = frappe.get_app_path("lms")
	seed_dir = os.path.join(app_path, "..", "fixtures_media")
	seed_dir = os.path.abspath(seed_dir)
	if not os.path.isdir(seed_dir):
		return

	site_files_dir = frappe.get_site_path("public", "files")
	os.makedirs(site_files_dir, exist_ok=True)

	for filename in os.listdir(seed_dir):
		src = os.path.join(seed_dir, filename)
		dest = os.path.join(site_files_dir, filename)
		if os.path.isfile(src) and not os.path.exists(dest):
			shutil.copy2(src, dest)
