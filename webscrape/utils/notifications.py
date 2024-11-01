# utils.py
import requests
import logging

logger = logging.getLogger(__name__)

def send_notification(data):
    webhook_url = "https://3470pw9n-5000.inc1.devtunnels.ms/notification"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(webhook_url, json=data, headers=headers)
        response.raise_for_status()
        logger.info("Notification sent successfully")
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")

