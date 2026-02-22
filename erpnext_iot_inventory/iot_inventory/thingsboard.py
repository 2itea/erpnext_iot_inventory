import json

import frappe
import requests
from frappe import _


class ThingsBoardClient:
	"""Client for ThingsBoard REST API."""

	def __init__(self):
		settings = frappe.get_single("IoT ThingsBoard Settings")
		self.base_url = (settings.instance_url or "").rstrip("/")
		self.username = settings.username
		self.password = settings.get_password("password")
		self.token = None

	def authenticate(self):
		"""Authenticate and obtain JWT token."""
		url = f"{self.base_url}/api/auth/login"
		response = requests.post(
			url,
			json={"username": self.username, "password": self.password},
			timeout=30,
		)
		response.raise_for_status()
		self.token = response.json().get("token")
		return self.token

	def _headers(self):
		if not self.token:
			self.authenticate()
		return {
			"Content-Type": "application/json",
			"X-Authorization": f"Bearer {self.token}",
		}

	def create_device(self, name, device_type=None):
		"""Create a device on ThingsBoard and return its ID and credentials."""
		if not device_type:
			settings = frappe.get_single("IoT ThingsBoard Settings")
			device_type = settings.default_device_type or "default"

		url = f"{self.base_url}/api/device"
		payload = {"name": name, "type": device_type}
		response = requests.post(
			url, headers=self._headers(), json=payload, timeout=30
		)
		response.raise_for_status()
		device_data = response.json()
		device_id = device_data["id"]["id"]

		credentials = self.get_credentials(device_id)

		return {
			"device_id": device_id,
			"access_token": credentials.get("credentialsId", ""),
		}

	def get_device(self, device_id):
		"""Get device details from ThingsBoard."""
		url = f"{self.base_url}/api/device/{device_id}"
		response = requests.get(url, headers=self._headers(), timeout=30)
		response.raise_for_status()
		return response.json()

	def delete_device(self, device_id):
		"""Delete a device from ThingsBoard."""
		url = f"{self.base_url}/api/device/{device_id}"
		response = requests.delete(url, headers=self._headers(), timeout=30)
		response.raise_for_status()

	def update_attributes(self, device_id, attrs):
		"""Push server-scope attributes to a device."""
		url = f"{self.base_url}/api/plugins/telemetry/DEVICE/{device_id}/attributes/SERVER_SCOPE"
		response = requests.post(
			url, headers=self._headers(), json=attrs, timeout=30
		)
		response.raise_for_status()

	def get_credentials(self, device_id):
		"""Get device credentials (access token) from ThingsBoard."""
		url = f"{self.base_url}/api/device/{device_id}/credentials"
		response = requests.get(url, headers=self._headers(), timeout=30)
		response.raise_for_status()
		return response.json()


@frappe.whitelist()
def test_connection():
	"""Test the connection to ThingsBoard."""
	try:
		client = ThingsBoardClient()
		client.authenticate()
		return {"success": True}
	except Exception as e:
		return {"success": False, "error": str(e)}


@frappe.whitelist()
def push_device(device_name):
	"""Create or update a device on ThingsBoard."""
	doc = frappe.get_doc("IoT Device", device_name)
	client = ThingsBoardClient()

	if doc.tb_device_id:
		# Update existing device attributes
		attrs = {
			"serial_number": doc.serial_number,
			"status": doc.status,
			"device_profile": doc.device_profile,
		}
		if doc.location_name:
			attrs["location"] = doc.location_name
		if doc.gps_latitude and doc.gps_longitude:
			attrs["latitude"] = doc.gps_latitude
			attrs["longitude"] = doc.gps_longitude

		client.update_attributes(doc.tb_device_id, attrs)
	else:
		# Create new device
		result = client.create_device(doc.serial_number)
		doc.tb_device_id = result["device_id"]
		doc.tb_access_token = result["access_token"]
		doc.save(ignore_permissions=True)

		# Push initial attributes
		attrs = {
			"serial_number": doc.serial_number,
			"status": doc.status,
			"device_profile": doc.device_profile,
		}
		client.update_attributes(doc.tb_device_id, attrs)

	return True


@frappe.whitelist()
def pull_device(device_name):
	"""Pull device info from ThingsBoard."""
	doc = frappe.get_doc("IoT Device", device_name)

	if not doc.tb_device_id:
		frappe.throw(_("No ThingsBoard Device ID set for this device"))

	client = ThingsBoardClient()
	tb_device = client.get_device(doc.tb_device_id)

	# Update access token
	credentials = client.get_credentials(doc.tb_device_id)
	doc.tb_access_token = credentials.get("credentialsId", "")
	doc.save(ignore_permissions=True)

	return True


@frappe.whitelist()
def sync_all_devices():
	"""Sync all devices that have no ThingsBoard ID yet."""
	devices = frappe.get_all(
		"IoT Device",
		filters={"tb_device_id": ["in", ["", None]]},
		pluck="name",
	)

	count = 0
	for device_name in devices:
		try:
			push_device(device_name)
			count += 1
		except Exception:
			frappe.log_error(
				f"ThingsBoard sync failed for {device_name}",
				"ThingsBoard Sync Error",
			)

	if count:
		frappe.db.commit()

	return {"count": count}


def scheduled_sync():
	"""Hourly scheduled task: auto-sync if enabled."""
	settings = frappe.get_single("IoT ThingsBoard Settings")
	if not settings.auto_sync:
		return
	if not settings.instance_url:
		return

	sync_all_devices()
