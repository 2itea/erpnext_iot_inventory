frappe.listview_settings["IoT Device"] = {
	get_indicator: function (doc) {
		var status_map = {
			"In Stock": [__("In Stock"), "blue"],
			Provisioned: [__("Provisioned"), "orange"],
			Deployed: [__("Deployed"), "green"],
			Maintenance: [__("Maintenance"), "yellow"],
			Decommissioned: [__("Decommissioned"), "darkgrey"],
			Faulty: [__("Faulty"), "red"],
		};
		return status_map[doc.status] || [__(doc.status), "grey"];
	},
};
