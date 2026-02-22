import re

import frappe
from frappe.model.document import Document


class IoTDevice(Document):
	def validate(self):
		self.validate_mac_address()

	def validate_mac_address(self):
		if self.mac_address:
			mac_pattern = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
			if not mac_pattern.match(self.mac_address):
				frappe.throw(
					frappe._("MAC Address must be in format XX:XX:XX:XX:XX:XX")
				)
