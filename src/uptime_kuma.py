import requests
import logging
from datetime import datetime
from src.config import config

logger = logging.getLogger("uptime-kuma-api")

def get_status_page(slug):
    """Get status page information from Uptime Kuma API"""
    try:
        response = requests.get(f"{config.UPTIME_KUMA_URL}/api/status-page/{slug}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching status page: {e}")
        return {"error": str(e)}

def get_heartbeat_data(slug):
    """Get heartbeat data from Uptime Kuma API"""
    try:
        response = requests.get(f"{config.UPTIME_KUMA_URL}/api/status-page/heartbeat/{slug}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching heartbeat data: {e}")
        return {"error": str(e)}

def process_monitor_data(status_page, heartbeat_data):
    """Process and combine status page and heartbeat data, only keeping fields used in widget"""
    if "error" in status_page or "error" in heartbeat_data:
        return {"error": status_page.get("error") or heartbeat_data.get("error")}

    monitors = []

    # Process each monitor group
    for group in status_page.get("publicGroupList", []):
        for monitor in group.get("monitorList", []):
            monitor_id = str(monitor.get("id"))

            # Get heartbeat data for this monitor
            heartbeat_list = heartbeat_data.get("heartbeatList", {}).get(monitor_id, [])

            # Get the most recent heartbeat
            latest_heartbeat = heartbeat_list[0] if heartbeat_list else None

            # Only keep data needed for widget display
            monitor_info = {
                "id": monitor_id,
                "name": monitor.get("name"),
                "status": latest_heartbeat.get("status") if latest_heartbeat else 0,
                "response_time": latest_heartbeat.get("ping") if latest_heartbeat else 0,
                "message": latest_heartbeat.get("msg") if latest_heartbeat else ""
            }

            monitors.append(monitor_info)

    # Sort monitors: down first, then by name
    monitors.sort(key=lambda m: (m["status"] == 1, m["name"]))

    return {
        "title": status_page.get("config", {}).get("title", "Status"),
        "monitors": monitors,
        "has_failing": any(m["status"] != 1 for m in monitors)
    }
