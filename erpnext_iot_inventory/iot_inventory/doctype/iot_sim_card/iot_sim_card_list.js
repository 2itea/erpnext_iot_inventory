frappe.listview_settings["IoT SIM Card"] = {
	get_indicator: function (doc) {
		var status_map = {
			Active: [__("Active"), "green"],
			Suspended: [__("Suspended"), "orange"],
			Deactivated: [__("Deactivated"), "red"],
			Lost: [__("Lost"), "darkgrey"],
		};
		return status_map[doc.status] || [__(doc.status), "grey"];
	},
};
