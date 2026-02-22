from frappe import _


def get_data():
	return {
		"fieldname": "iot_device",
		"transactions": [
			{
				"label": _("References"),
				"items": ["Customer", "Project", "Subscription", "Contract", "Asset"],
			},
		],
	}
