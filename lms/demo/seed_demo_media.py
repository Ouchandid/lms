import json
import os
import shutil

import frappe


def copy_seed_files():
	"""Copy bundled demo media (course covers, lesson PDFs, site logo) into
	this site's public files folder, and ensure the matching File doctype
	records exist, so records restored from fixtures don't end up with
	broken attachment links on a fresh install.

	This intentionally does not rely on fixture-importing the File doctype
	itself: a plain fixture import re-writes the file's bytes through
	File.save_file(), and on a site where a file of that name already
	exists (e.g. a second migrate run), Frappe treats it as new content and
	renames it with a random suffix — leaving doctype fields (e.g. Website
	Settings.banner_image) pointing at a filename that no longer has a
	File record. Creating the File record directly with
	copy_from_existing_file sidesteps that rewrite and is idempotent.
	"""
	app_path = frappe.get_app_path("lms")
	seed_dir = os.path.abspath(os.path.join(app_path, "..", "fixtures_media"))
	if not os.path.isdir(seed_dir):
		return

	site_files_dir = frappe.get_site_path("public", "files")
	os.makedirs(site_files_dir, exist_ok=True)

	for filename in os.listdir(seed_dir):
		src = os.path.join(seed_dir, filename)
		dest = os.path.join(site_files_dir, filename)
		if os.path.isfile(src) and not os.path.exists(dest):
			shutil.copy2(src, dest)

	_ensure_file_records()


def _ensure_file(file_url, attached_to_doctype, attached_to_name, attached_to_field=None):
	if not file_url or not file_url.startswith("/files/"):
		return

	# Match on the exact file_url rather than just (doctype, name): several
	# fields/blocks can legitimately point at different files on the same
	# parent (Website Settings banner_image vs favicon; a lesson with two
	# PDFs). Matching — and deleting — by (doctype, name) alone meant
	# reconciling one field found a *different* field's record, saw a
	# file_url mismatch, and deleted it out from under it.
	if frappe.db.exists(
		"File",
		{
			"attached_to_doctype": attached_to_doctype,
			"attached_to_name": attached_to_name,
			"file_url": file_url,
		},
	):
		return

	filename = file_url.split("/files/")[-1]
	local_path = os.path.join(frappe.get_site_path("public", "files"), filename)
	if not os.path.exists(local_path):
		return

	file_doc = frappe.new_doc("File")
	file_doc.update(
		{
			"file_name": filename,
			"file_url": file_url,
			"attached_to_doctype": attached_to_doctype,
			"attached_to_name": attached_to_name,
			"attached_to_field": attached_to_field,
			"is_private": 0,
			"folder": "Home",
		}
	)
	file_doc.flags.copy_from_existing_file = True
	file_doc.insert(ignore_permissions=True)


def _ensure_file_records():
	ws = frappe.get_single("Website Settings")
	for field in ["banner_image", "app_logo", "footer_logo", "favicon"]:
		_ensure_file(ws.get(field), "Website Settings", "Website Settings", field)

	for course in frappe.get_all("LMS Course", fields=["name", "image"]):
		_ensure_file(course.image, "LMS Course", course.name)

	for lesson in frappe.get_all("Course Lesson", fields=["name", "content"]):
		if not lesson.content:
			continue
		try:
			data = json.loads(lesson.content)
		except Exception:
			continue
		for block in data.get("blocks", []):
			btype = block.get("type")
			bdata = block.get("data", {})
			if btype == "upload" and bdata.get("file_url"):
				_ensure_file(bdata["file_url"], "Course Lesson", lesson.name)
			if btype == "image" and bdata.get("file", {}).get("url"):
				_ensure_file(bdata["file"]["url"], "Course Lesson", lesson.name)

	frappe.db.commit()
