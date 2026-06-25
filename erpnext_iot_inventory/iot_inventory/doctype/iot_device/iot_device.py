import base64
import io
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


@frappe.whitelist()
def generate_label_data(device_name):
	"""Return QR code PNG (base64) + device metadata for client-side label printing."""
	import qrcode as qrcode_lib

	doc = frappe.get_doc("IoT Device", device_name)

	# Extract first LoRaWAN DevEUI
	dev_eui = ""
	for cred in doc.network_credentials:
		if cred.protocol_type == "LoRaWAN" and cred.dev_eui:
			dev_eui = cred.dev_eui.upper()
			break

	# Supplier serial → QRCode RC2 (insert dash after 6th char: S00177000008019 → S00177-000008019)
	supplier_serial = doc.supplier_serial_number or ""
	if len(supplier_serial) > 6 and "-" not in supplier_serial:
		qrcode_rc2 = supplier_serial[:6] + "-" + supplier_serial[6:]
	else:
		qrcode_rc2 = supplier_serial

	qr_content = "\n".join([
		f"Serial Number – 2itea: {doc.name}",
		f"QRCode – RC2: {qrcode_rc2}",
		f"DEVEUI: {dev_eui}",
		"Lot de fabrication: 00001",
	])

	qr = qrcode_lib.QRCode(
		version=1,
		error_correction=qrcode_lib.constants.ERROR_CORRECT_L,
		box_size=10,
		border=2,
	)
	qr.add_data(qr_content)
	qr.make(fit=True)
	img = qr.make_image(fill_color="black", back_color="white")

	buf = io.BytesIO()
	img.save(buf, format="PNG")
	qr_b64 = base64.b64encode(buf.getvalue()).decode()

	return {
		"serial": doc.name,
		"qrcode_rc2": qrcode_rc2,
		"dev_eui": dev_eui,
		"qr_png_b64": qr_b64,
	}
