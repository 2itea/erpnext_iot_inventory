# ERPNext IoT Inventory

IoT Device Inventory Management for ERPNext / Frappe.

Manage your IoT fleet (sensors, gateways, SIM cards, certificates) directly in ERPNext with optional ThingsBoard integration.

## Features

- **IoT Device Profile** - Define device types with specs (manufacturer, model, protocol, IP rating)
- **IoT Device** - Track individual sensors/actuators with serial numbers, LoRaWAN/Sigfox credentials, and lifecycle status
- **IoT Gateway** - Manage gateways with EUI, MQTT config, SIM cards, and mesh networking
- **IoT SIM Card** - Track SIM cards with ICCID, carrier, data plan, and costs
- **IoT Firmware** - Version firmware per device profile with SHA256 checksums
- **IoT Certificate** - Manage TLS/mTLS certificates with automatic expiry tracking
- **IoT ThingsBoard Settings** - Sync devices to/from ThingsBoard via REST API
- **Customer Dashboard** - See IoT Device and Gateway counts on each Customer

## ERPNext Integration

Devices and gateways link to native ERPNext DocTypes:
- **Customer** - Client assignment
- **Subscription** / **Contract** - Service agreements
- **Asset** - Fixed asset tracking
- **Project** - Project association
- **Item** - Device profiles link to purchasable items
- **Supplier** - SIM card operators

## Installation

```bash
bench get-app https://github.com/2itea/erpnext_iot_inventory
bench --site your-site install-app erpnext_iot_inventory
bench migrate
```

## Setup

1. The **IoT Manager** role is created automatically on install
2. Two default device profiles are created (Generic LoRaWAN Sensor, RAK7268v2 Gateway)
3. Configure **IoT ThingsBoard Settings** if you use ThingsBoard

## Roles

| Role | Access |
|------|--------|
| System Manager | Full CRUD + import/export on all DocTypes |
| IoT Manager | Full CRUD + import/export on all DocTypes |
| Sales User | Read-only on IoT Device and IoT Gateway |

## License

MIT
