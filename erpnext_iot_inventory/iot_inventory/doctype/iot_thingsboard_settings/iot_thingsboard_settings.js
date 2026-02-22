frappe.ui.form.on("IoT ThingsBoard Settings", {
	refresh: function (frm) {
		frm.add_custom_button(__("Test Connection"), function () {
			frappe.call({
				method: "erpnext_iot_inventory.iot_inventory.thingsboard.test_connection",
				callback: function (r) {
					if (r.message && r.message.success) {
						frappe.msgprint(__("Connection successful!"));
					} else {
						frappe.msgprint(
							__("Connection failed: {0}", [
								r.message ? r.message.error : "Unknown error",
							])
						);
					}
				},
			});
		});
	},

	sync_all_button: function (frm) {
		frappe.call({
			method: "erpnext_iot_inventory.iot_inventory.thingsboard.sync_all_devices",
			callback: function (r) {
				if (r.message) {
					frappe.msgprint(
						__("Sync completed: {0} devices synced", [r.message.count])
					);
				}
			},
		});
	},
});
