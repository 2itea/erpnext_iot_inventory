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
	const { serial, qrcode_rc2, dev_eui, qr_png_b64, logo_b64, ce_b64 } = data;

	// Label layout matches serial_zd421.glabels template exactly:
	// Size: 57.15mm × 31.75mm
	// Logo:  left=3.68mm top=11.58mm  w=26.42mm h=8.56mm
	// CE:    left=3.86mm top=22.99mm  w=14.88mm h=5.99mm
	// QR:    left=32.05mm top=5.97mm  w=19.81mm h=19.81mm
	// Text:  "Serial:" left=27.69mm top=25.04mm  value left=37.26mm top=25.12mm
	const html = `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Étiquette ${serial}</title>
<style>
  @page {
    size: 57.15mm 31.75mm;
    margin: 0;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 57.15mm;
    height: 31.75mm;
    position: relative;
    overflow: hidden;
    font-family: Arial, Helvetica, sans-serif;
    background: white;
  }
  img { display: block; }
  .logo {
    position: absolute;
    left: 3.68mm; top: 11.58mm;
    width: 26.42mm; height: 8.56mm;
  }
  .ce {
    position: absolute;
    left: 3.86mm; top: 22.99mm;
    width: 14.88mm; height: 5.99mm;
  }
  .qr {
    position: absolute;
    left: 32.05mm; top: 5.97mm;
    width: 19.81mm; height: 19.81mm;
  }
  .serial-label {
    position: absolute;
    left: 27.69mm; top: 25.04mm;
    font-size: 5.5pt; font-weight: bold;
    line-height: 1;
  }
  .serial-value {
    position: absolute;
    left: 37.26mm; top: 25.12mm;
    font-size: 5.5pt;
    line-height: 1;
  }
</style>
</head>
<body>
  <img class="logo" src="data:image/png;base64,${logo_b64 || ""}" />
  <img class="ce"   src="data:image/png;base64,${ce_b64 || ""}" />
  <img class="qr"   src="data:image/png;base64,${qr_png_b64}" />
  <span class="serial-label">Serial:</span>
  <span class="serial-value">${serial}</span>
</body>
</html>`;

	// Use Blob URL so window.onload fires reliably after all images are decoded
	const blob = new Blob([html], { type: "text/html; charset=utf-8" });
	const blobUrl = URL.createObjectURL(blob);
	const win = window.open(blobUrl, "_blank");

	if (!win) {
		frappe.msgprint({
			title: __("Popup bloquée"),
			message: __("Autorisez les popups pour ce site, puis réessayez."),
			indicator: "orange",
		});
		URL.revokeObjectURL(blobUrl);
		return;
	}

	win.addEventListener("load", function () {
		setTimeout(function () {
			win.print();
			URL.revokeObjectURL(blobUrl);
		}, 300);
	});
}
