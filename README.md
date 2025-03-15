# Uptime Kuma Glance Extension
_An extension widget API for the [Glance](https://github.com/glanceapp/glance) dashboard._

![Widget screenshot](https://github.com/user-attachments/assets/21cbbf7b-bc1b-4643-bcd1-c1db1fe55248)

A widget that displays your [Uptime Kuma](https://github.com/louislam/uptime-kuma) services on a specific status page within Glance. Shows all monitors with their current status and response time.

## Setup
### Docker Compose
Add the following to your existing glance docker compose
```yml
services:
  glance:
    image: glanceapp/glance
    # ...

  uptime-kuma-extension:
    image: ghcr.io/not-first/uptime-kuma-glance-extension
    ports:
      - '8676:8676'
    restart: unless-stopped
    env_file: .env
```
#### Environment Variables
This widget must be set up by providing an environment variable, which can be added to your existing glance .env file:
```env
UPTIME_KUMA_URL=http://uptime-kuma.example.com
```

### Glance Config
Next, add the extension widget into your glance page by creating an environment variable storing the IP and port for the API, and adding this to your `glance.yml`.
```yml
- type: extension
  title: Uptime Status
  url: http://${UPTIME_KUMA_EXTENSION_URL}/{status-page-slug}
  cache: 5m
  allow-potentially-dangerous-html: true
```
The endpoint for your status page is accessible on the path `/{status-page-slug}`, where `{status-page-slug}` is the slug of your Uptime Kuma status page.

For example, if your status page's URL is `http://uptime-kuma.example.com/status/mypage`, the slug would be `mypage`.

---
