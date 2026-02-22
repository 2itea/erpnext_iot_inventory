import frappe
from frappe import _


def after_install():
	create_iot_manager_role()
	create_default_profiles()


def create_iot_manager_role():
	"""Create the IoT Manager role if it doesn't exist."""
	if not frappe.db.exists("Role", "IoT Manager"):
		role = frappe.new_doc("Role")
		role.role_name = "IoT Manager"
		role.desk_access = 1
		role.insert(ignore_permissions=True)
		frappe.db.commit()


def create_default_profiles():
	"""Create default device profiles."""
	profiles = [
		{
			"profile_name": "Generic LoRaWAN Sensor",
			"device_category": "Sensor",
			"supported_protocols": "LoRaWAN",
		},
		{
			"profile_name": "RAK7268v2 Gateway",
			"manufacturer": "RAKwireless",
			"model": "RAK7268v2",
			"device_category": "Gateway",
			"supported_protocols": "LoRaWAN",
			"power_source": "PoE",
			"ip_rating": "IP65",
		},
	]

	for profile_data in profiles:
		if not frappe.db.exists("IoT Device Profile", profile_data["profile_name"]):
			doc = frappe.new_doc("IoT Device Profile")
			doc.update(profile_data)
			doc.insert(ignore_permissions=True)

	frappe.db.commit()
