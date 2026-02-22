import re

import frappe
from frappe.model.document import Document


class IoTGateway(Document):
	def validate(self):
		self.validate_gw_eui()
		self.validate_mac_address()
		self.validate_mesh_root_key()

	def validate_gw_eui(self):
		if self.gw_eui:
			hex_16 = re.compile(r"^[0-9A-Fa-f]{16}$")
			if not hex_16.match(self.gw_eui):
				frappe.throw(
					frappe._("Gateway EUI must be exactly 16 hexadecimal characters")
				)

	def validate_mac_address(self):
		if self.mac_address:
			mac_pattern = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
			if not mac_pattern.match(self.mac_address):
				frappe.throw(
					frappe._("MAC Address must be in format XX:XX:XX:XX:XX:XX")
				)

	def validate_mesh_root_key(self):
		if self.gateway_role == "Mesh" and self.mesh_root_key:
			hex_32 = re.compile(r"^[0-9A-Fa-f]{32}$")
			key = self.get_password("mesh_root_key") or ""
			if not hex_32.match(key):
				frappe.throw(
					frappe._("Mesh Root Key must be exactly 32 hexadecimal characters")
				)
