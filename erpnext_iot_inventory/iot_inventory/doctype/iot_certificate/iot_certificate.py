from datetime import date

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, getdate, today


class IoTCertificate(Document):
	def validate(self):
		self.update_days_until_expiry()

	def update_days_until_expiry(self):
		if self.valid_until:
			self.days_until_expiry = date_diff(self.valid_until, today())
			if self.days_until_expiry < 0 and self.status == "Active":
				self.status = "Expired"


def check_certificate_expiry():
	"""Daily scheduled task: update expiry status for all active certificates."""
	certificates = frappe.get_all(
		"IoT Certificate",
		filters={"status": "Active", "valid_until": ["<", today()]},
		pluck="name",
	)
	for cert_name in certificates:
		cert = frappe.get_doc("IoT Certificate", cert_name)
		cert.status = "Expired"
		cert.days_until_expiry = date_diff(cert.valid_until, today())
		cert.save(ignore_permissions=True)

	if certificates:
		frappe.db.commit()
