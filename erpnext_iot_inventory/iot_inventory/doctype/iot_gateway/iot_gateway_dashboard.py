from frappe import _


def get_data():
	return {
		"fieldname": "iot_gateway",
		"transactions": [
			{
				"label": _("References"),
				"items": ["Customer", "Project", "Subscription", "Contract"],
			},
		],
	}
