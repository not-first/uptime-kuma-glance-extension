import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from src.config import config
from src.uptime_kuma import get_status_page, get_heartbeat_data, process_monitor_data
from src.widget import parse_widget_html

logging.basicConfig(format="%(levelname)s:    %(message)s", level=logging.INFO)
logger = logging.getLogger("uptime-kuma-api")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Uptime Kuma API is running!"}

@app.get("/{slug}")
async def get_status(slug: str, request: Request):
    logger.info(f"Request received for status page: {slug}")

    if not config.UPTIME_KUMA_URL:
        error_msg = "UPTIME_KUMA_URL not configured"
        logger.error(error_msg)
        return HTMLResponse(
            content=f"<p class='color-negative'>Error: {error_msg}</p>",
            headers={"Widget-Title": "Uptime Status", "Widget-Content-Type": "html"}
        )

    # Fetch data directly from Uptime Kuma API
    status_page = get_status_page(slug)
    if "error" in status_page:
        return HTMLResponse(
            content=f"<p class='color-negative'>Error: {status_page['error']}</p>",
            headers={"Widget-Title": "Uptime Status", "Widget-Content-Type": "html"}
        )

    heartbeat_data = get_heartbeat_data(slug)
    if "error" in heartbeat_data:
        return HTMLResponse(
            content=f"<p class='color-negative'>Error: {heartbeat_data['error']}</p>",
            headers={"Widget-Title": "Uptime Status", "Widget-Content-Type": "html"}
        )

    # Process the data
    data = process_monitor_data(status_page, heartbeat_data)

    if "error" in data:
        return HTMLResponse(
            content=f"<p class='color-negative'>Error: {data['error']}</p>",
            headers={"Widget-Title": "Uptime Status", "Widget-Content-Type": "html"}
        )

    widget_title = data.get("title", "Uptime Status")

    return HTMLResponse(
        content=parse_widget_html(data),
        headers={"Widget-Title": widget_title, "Widget-Content-Type": "html"}
    )