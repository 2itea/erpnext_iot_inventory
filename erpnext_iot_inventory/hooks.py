app_name = "erpnext_iot_inventory"
app_title = "IoT Inventory"
app_publisher = "2itea"
app_description = "IoT Device Inventory Management for ERPNext"
app_email = "contact@2itea.com"
app_license = "MIT"

after_install = "erpnext_iot_inventory.setup.install.after_install"

doctype_js = {
	"Customer": "public/js/customer.js",
}

scheduler_events = {
	"daily": [
		"erpnext_iot_inventory.iot_inventory.doctype.iot_certificate.iot_certificate.check_certificate_expiry",
	],
	"hourly": [
		"erpnext_iot_inventory.iot_inventory.thingsboard.scheduled_sync",
	],
}
