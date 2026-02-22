frappe.ui.form.on("IoT Device", {
	refresh: function (frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Sync to ThingsBoard"), function () {
				frappe.call({
					method: "erpnext_iot_inventory.iot_inventory.thingsboard.push_device",
					args: { device_name: frm.doc.name },
					callback: function (r) {
						if (r.message) {
							frm.reload_doc();
							frappe.msgprint(__("Device synced to ThingsBoard"));
						}
					},
				});
			}, __("ThingsBoard"));

			frm.add_custom_button(__("Pull from ThingsBoard"), function () {
				frappe.call({
					method: "erpnext_iot_inventory.iot_inventory.thingsboard.pull_device",
					args: { device_name: frm.doc.name },
					callback: function (r) {
						if (r.message) {
							frm.reload_doc();
							frappe.msgprint(__("Device pulled from ThingsBoard"));
						}
					},
				});
			}, __("ThingsBoard"));
		}
	},
});
