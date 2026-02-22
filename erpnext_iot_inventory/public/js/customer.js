frappe.ui.form.on("Customer", {
	refresh: function (frm) {
		if (frm.doc.name) {
			frappe.xcall(
				"frappe.client.get_count",
				{
					doctype: "IoT Device",
					filters: { customer: frm.doc.name },
				}
			).then(function (device_count) {
				if (device_count) {
					frm.dashboard.add_indicator(
						__("IoT Devices: {0}", [device_count]),
						"blue"
					);
				}
			});

			frappe.xcall(
				"frappe.client.get_count",
				{
					doctype: "IoT Gateway",
					filters: { customer: frm.doc.name },
				}
			).then(function (gw_count) {
				if (gw_count) {
					frm.dashboard.add_indicator(
						__("IoT Gateways: {0}", [gw_count]),
						"green"
					);
				}
			});
		}
	},
});
