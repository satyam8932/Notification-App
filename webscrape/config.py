# config.py
import os
from redis import Redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
QUEUE_NAME = os.getenv("QUEUE_NAME", "car_alerts")
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

# Set up Redis connection
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)
