frappe.ui.form.on("IoT Device", {
	refresh: function (frm) {
		if (!frm.is_new()) {
			// ── ThingsBoard buttons ───────────────────────────────────────
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

			// ── Print label button ────────────────────────────────────────
			frm.add_custom_button(__("🖨 Imprimer étiquette"), function () {
				frappe.call({
					method: "erpnext_iot_inventory.iot_inventory.doctype.iot_device.iot_device.generate_label_data",
					args: { device_name: frm.doc.name },
					freeze: true,
					freeze_message: __("Génération de l'étiquette…"),
					callback: function (r) {
						if (r.message) {
							_open_print_window(r.message);
						}
					},
				});
			});
		}
	},
});

function _open_print_window(data) {
	const { serial, qrcode_rc2, dev_eui, qr_png_b64 } = data;

	const html = `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Étiquette ${serial}</title>
<style>
  @page { size: 57.15mm 31.75mm; margin: 0; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 57.15mm;
    height: 31.75mm;
    display: flex;
    flex-direction: row;
    font-family: Arial, Helvetica, sans-serif;
    overflow: hidden;
  }
  .qr-col {
    width: 31.75mm;
    height: 31.75mm;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1mm;
  }
  .qr-col img { width: 29.75mm; height: 29.75mm; }
  .info-col {
    flex: 1;
    padding: 2mm 2mm 2mm 1mm;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 1.2mm;
  }
  .brand   { font-size: 5.5pt; color: #888; text-transform: uppercase; letter-spacing: 0.5pt; }
  .serial  { font-size: 9pt; font-weight: bold; }
  .rc2     { font-size: 6pt; color: #444; }
  .lbl     { font-size: 5pt; color: #888; margin-top: 0.8mm; }
  .deveui  { font-size: 5.5pt; font-family: monospace; letter-spacing: 0.2pt; }
</style>
</head>
<body>
  <div class="qr-col">
    <img src="data:image/png;base64,${qr_png_b64}" />
  </div>
  <div class="info-col">
    <div class="brand">2itea</div>
    <div class="serial">${serial}</div>
    <div class="rc2">${qrcode_rc2 || ""}</div>
    <div class="lbl">DevEUI</div>
    <div class="deveui">${dev_eui || "—"}</div>
  </div>
</body>
</html>`;

	const win = window.open("", "_blank", "width=350,height=250");
	if (!win) {
		frappe.msgprint({
			title: __("Popup bloquée"),
			message: __("Autorisez les popups pour ce site, puis réessayez."),
			indicator: "orange",
		});
		return;
	}
	win.document.write(html);
	win.document.close();
	win.focus();
	// Wait for image to render before triggering print dialog
	win.onload = function () { win.print(); };
	setTimeout(function () { win.print(); }, 600);
}
