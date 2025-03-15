from src.config import config

def parse_widget_html(data):
    if "error" in data:
        return f"<p class='color-negative'>Error: {data['error']}</p>"

    # Check if we have any monitors
    if not data.get("monitors"):
        return "<p>No monitors found</p>"

    # Build monitor list HTML
    monitor_items = []

    for monitor in data.get("monitors", []):
        status_style = "ok" if monitor.get("status") == 1 else "error"
        response_time = monitor.get("response_time", 0)
        message = monitor.get("message", "")
        monitor_id = monitor.get("id", "")

        # Generate the Uptime Kuma dashboard URL for this monitor
        dashboard_url = f"{config.UPTIME_KUMA_URL}/dashboard/{monitor_id}"

        # Show response time only for up services, ERROR for down services
        response_display = f"{response_time}ms" if status_style == "ok" else "<span class='color-negative'>ERROR</span>"

        # Create status icon based on monitor status
        if status_style == "ok":
            status_icon = """
            <div class="monitor-site-status-icon-compact" title="OK">
                <svg fill="var(--color-positive)" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm3.857-9.809a.75.75 0 0 0-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 1 0-1.06 1.061l2.5 2.5a.75.75 0 0 0 1.137-.089l4-5.5Z" clip-rule="evenodd" />
                </svg>
            </div>
            """
        else:
            status_icon = f"""
            <div class="monitor-site-status-icon-compact" title="{message if message else 'Error'}">
                <svg fill="var(--color-negative)" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495ZM10 5a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 10 5Zm0 9a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z" clip-rule="evenodd" />
                </svg>
            </div>
            """

        # Format each monitor with link to Uptime Kuma dashboard
        monitor_html = f"""
        <div class="flex items-center gap-12">
            <a class="size-title-dynamic color-highlight text-truncate block grow" href="{dashboard_url}" target="_blank" rel="noreferrer">{monitor.get('name')}</a>
            <div>{response_display}</div>
            {status_icon}
        </div>
        """
        monitor_items.append(monitor_html)

    monitors_html = "\n".join(monitor_items)

    # Use the compact widget structure
    return f"""
    <ul class="dynamic-columns list-gap-8">
        {monitors_html}
    </ul>
    """
