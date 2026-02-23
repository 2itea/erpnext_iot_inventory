from frappe import _


def get_data():
	return {
		"fieldname": "serial_number",
		"internal_links": {
			"Customer": ["customer"],
			"Project": ["project"],
			"Subscription": ["subscription"],
			"Contract": ["contract"],
			"Asset": ["asset"],
		},
		"transactions": [
			{
				"label": _("References"),
				"items": ["Customer", "Project", "Subscription", "Contract", "Asset"],
			},
		],
	}
