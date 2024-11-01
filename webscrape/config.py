# config.py
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
QUEUE_NAME = os.getenv("QUEUE_NAME", "car_alerts")
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")
