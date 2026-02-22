import re

import frappe
from frappe.model.document import Document


class IoTNetworkCredential(Document):
	def validate(self):
		if self.protocol_type == "LoRaWAN":
			self.validate_lorawan()

	def validate_lorawan(self):
		hex_16 = re.compile(r"^[0-9A-Fa-f]{16}$")
		hex_32 = re.compile(r"^[0-9A-Fa-f]{32}$")

		if self.dev_eui and not hex_16.match(self.dev_eui):
			frappe.throw(frappe._("DevEUI must be exactly 16 hexadecimal characters"))

		if self.app_eui and not hex_16.match(self.app_eui):
			frappe.throw(frappe._("AppEUI must be exactly 16 hexadecimal characters"))

		if self.app_key and not hex_32.match(self.get_password("app_key") or ""):
			frappe.throw(frappe._("AppKey must be exactly 32 hexadecimal characters"))

		if self.nwk_key and not hex_32.match(self.get_password("nwk_key") or ""):
			frappe.throw(frappe._("NwkKey must be exactly 32 hexadecimal characters"))
