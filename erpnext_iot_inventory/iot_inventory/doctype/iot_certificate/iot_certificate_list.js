frappe.listview_settings["IoT Certificate"] = {
	get_indicator: function (doc) {
		var status_map = {
			Active: [__("Active"), "green"],
			Expired: [__("Expired"), "red"],
			Revoked: [__("Revoked"), "darkgrey"],
		};
		return status_map[doc.status] || [__(doc.status), "grey"];
	},
};
