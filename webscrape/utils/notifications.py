# utils/notifications.py
import requests

def send_notification(data):
    url = "http://node-backend-url/notifications"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Notification sent successfully")
    else:
        print("Failed to send notification")
