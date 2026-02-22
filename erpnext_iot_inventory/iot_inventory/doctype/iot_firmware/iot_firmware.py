import hashlib

import frappe
from frappe.model.document import Document


class IoTFirmware(Document):
	def before_save(self):
		if self.firmware_file:
			self.compute_checksum()

	def compute_checksum(self):
		try:
			file_path = frappe.get_site_path("public", self.firmware_file.lstrip("/"))
			with open(file_path, "rb") as f:
				self.checksum_sha256 = hashlib.sha256(f.read()).hexdigest()
		except FileNotFoundError:
			pass
