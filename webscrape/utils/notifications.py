# utils.py
import requests

def send_notification(data):
    webhook_url = "http://your-backend-url.com/notifications"  # Replace with actual backend URL
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(webhook_url, json=data, headers=headers)
    if response.status_code == 200:
        print("Notification sent successfully")
    else:
        print(f"Failed to send notification: {response.status_code}")
