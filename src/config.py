import os

class Config:
    UPTIME_KUMA_URL = os.getenv("UPTIME_KUMA_URL", "").rstrip('/')

config = Config()
