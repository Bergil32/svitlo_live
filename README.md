# 🟡 Svitlo.live
ЧИТАТИ УКРАЇНСЬКОЮ
An integration for **Home Assistant** that displays the current electricity supply status for your region and queue, based on data from [svitlo.live](https://svitlo.live).

This is the **new version (v2.0.0)**, which now fully relies on the **official API** instead of HTML parsing.  
The integration has been completely rebuilt — faster, more secure, and much lighter on the server.

---

## ⚙️ Main Features

- ✅ Displays the **current power status** (`On / Off`),  
- ✅ Detects the **next power-on** and **power-off** times,  
- ✅ Shows the time of the **last schedule update**,  
- ✅ Includes **built-in localization** (UA / EN),  
- ✅ Supports **all regions of Ukraine** and queue/group types (1.1–6.2, 1–6, 1–12),  
- ✅ Allows **multiple entries** (regions/queues) in a single Home Assistant instance,  
- ✅ All entries share **one common API request** to reduce network load,  
- ✅ Provides sensors and binary sensors ideal for automations and dashboards.

---

## 🔄 How It Works

### 🧩 Integration Architecture
The integration consists of two layers:

1. **`SvitloApiHub` (api_hub.py)**  
   A shared API hub for all entries.  
   - Makes **one HTTP request** to the proxy server (Cloudflare Worker) with the API key.  
   - Stores the response in a cache for 15 minutes.  
   - Prevents duplicate requests even when Home Assistant restarts.

2. **`SvitloCoordinator` (coordinator.py)**  
   A dedicated coordinator for each region/queue.  
   - Retrieves data from the shared hub (`api_hub`) without additional network requests.  
   - Processes half-hour slots and builds power states (`on/off`).  
   - Schedules **precise entity state changes at the exact time of power switch** — without calling the API again.

### 🕒 Timezone Handling
- The API returns the schedule in **local Ukrainian time (Europe/Kyiv)**.  
- The integration converts this to UTC for Home Assistant,  
  ensuring all times are displayed correctly regardless of your HA timezone.

---

## 🔐 API Key Protection

The integration **does not expose the API key** anywhere.

Access to `https://svitlo.live/api/asistant.php` is handled via a secure **Cloudflare Worker** proxy that:
- stores the `x-api-key` privately in its environment,
- accepts keyless requests from Home Assistant,
- forwards the request to `svitlo.live` and returns the JSON response.

This allows users to install the integration safely through HACS without exposing any private credentials.

---

## 🧠 Data Refresh Logic

- Home Assistant fetches new data **every 15 minutes**.
- The API response is **cached for 15 minutes** to minimize load.
- Between updates, the integration **auto-switches states** exactly at the scheduled times (half-hour marks).  
  For example: if power is scheduled to go off at 17:30, the “Electricity” sensor will change state **precisely at 17:30**, without any additional API calls.

---

## 🧩 Created Entities

| Type | Name | Description |
|------|------|-------------|
| 🟢 **Binary Sensor** | `Electricity status` | True/False power indicator |
| 📘 **Sensor** | `Electricity` | Text status: “Grid ON / OFF” |
| ⏰ **Sensor** | `Next grid connection` | Next power-on time (if currently off) |
| ⚠️ **Sensor** | `Next outage` | Next power-off time (if currently on) |
| 🔄 **Sensor** | `Schedule updated` | Last successful API refresh |
| 📅 **Calendar** | `calendar.svitlo_<region>_<queue>` |  “💡 Electricity available” events (Kyiv local time) |

---

## 🌍 Supported Regions

All regions of Ukraine (except temporarily unavailable ones, e.g., Kherson).  
For Vinnytsia — format “Queue N”; for Chernivtsi and Donetsk — “Group N”; others — “Queue N.M”.

---

## 🧰 Installation via HACS

1. Open HACS → **Integrations → Custom repositories**.  
2. Add this repository:
   ```
   https://github.com/chaichuk/svitlo_live
   ```
   (type: *Integration*).  
3. Install `Svitlo.live` and restart Home Assistant.  
4. Go to `Settings → Devices & Services → + Add Integration → Svitlo.live`  
   and select your region and queue.

---

## ⚡ Usage Example

### Automation: Notify when power goes off
```yaml
alias: Alert before blackout
trigger:
  - platform: state
    entity_id: binary_sensor.svitlo_kiivska_oblast_3_2_electricity_status
    to: 'off'
action:
  - service: notify.mobile_app
    data:
      title: "⚡ Power outage"
      message: "Electricity has been turned off in queue 3.2"
```

---

## 🧾 Changes in Version 2.0.0

| Category | Description |
|-----------|-------------|
| 🧠 **New architecture** | Centralized API requests through a shared `api_hub` |
| ⚡ **Precise synchronization** | Entity states update at exact scheduled times without extra API calls |
| ⏱ **Fixed refresh interval** | One API call every 15 minutes shared across all entries |
| 🌍 **Localization** | Full Ukrainian and English translation support |

---

## 💡 Author

- GitHub: [@chaichuk](https://github.com/chaichuk)  
- Telegram: [@serhii_chaichuk](https://t.me/serhii_chaichuk)

---

## 🪪 License

MIT License © 2025  
Open-source, with no API keys or personal data exposed.
