from flask import Flask, request, jsonify
import os
import json
import logging
import uuid
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Retrieve Airtable webhook URL and JWT token from environment variables
AIRTABLE_WEBHOOK_URL = os.getenv("AIRTABLE_WEBHOOK_URL")
JWT_TOKEN = os.getenv("JWT_TOKEN")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Ensure the directories exist
os.makedirs('notifications', exist_ok=True)
os.makedirs('events', exist_ok=True)

@app.route('/notifications', methods=['POST'])
def handle_notification():
    notification = request.json

    if not notification:
        logging.error("Invalid JSON received: %s", request.data)
        return jsonify({'error': 'Invalid JSON payload.'}), 400

    logging.info("Received notification: %s", json.dumps(notification, indent=4))
    save_to_file(notification, 'notifications', 'notification')

    notification_object = next((item for item in notification.get('@graph', []) if item.get('@type') == "Notification"), None)

    if notification_object and notification_object.get('hasEventType', {}).get('@id') == "https://onerecord.iata.org/ns/api#LOGISTICS_EVENT_RECEIVED":
        logistics_object_id = notification_object.get('hasLogisticsObject', {}).get('@id')
        
        if logistics_object_id:
            event = fetch_latest_event(logistics_object_id)
            if event:
                save_to_file(event, 'events', 'event')
                forward_event_to_airtable(event)
        else:
            logging.error("Logistics Object ID missing in the notification.")
    else:
        logging.warning("Notification type does not match 'LOGISTICS_EVENT_RECEIVED'.")

    return jsonify({'status': 'success'}), 200

def fetch_latest_event(logistics_object_id):
    url = f"{logistics_object_id}/logistics-events/"
    headers = {
        'Authorization': f'Bearer {JWT_TOKEN}',
        'Content-Type': 'application/ld+json; version=2.0.0-dev'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        events = response.json().get('@graph', [])
        sorted_events = sorted(events, key=lambda x: x.get('creationDate', {}).get('@value', ''))

        if sorted_events:
            return sorted_events[-1]
        logging.warning("No events found for logistics object.")
    else:
        logging.error("Failed to fetch events: %s", response.text)

    return None

def forward_event_to_airtable(event):
    payload = {
        'id': event.get('@id'),
        'logistics_object_id': event.get('eventFor', {}).get('@id'),
        'event_name': event.get('eventName'),
        'event_code': event.get('eventCode', {}).get('@id'),
        'event_date': event.get('eventDate', {}).get('@value'),
        'creation_date': event.get('creationDate', {}).get('@value'),
        'recording_organization': event.get('recordingOrganization', {}).get('@id')
    }

    response = requests.post(AIRTABLE_WEBHOOK_URL, json=payload)
    if response.status_code == 200:
        logging.info("Event forwarded to Airtable successfully.")
    else:
        logging.error("Failed to forward event to Airtable: %s", response.text)

def save_to_file(data, folder, prefix):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(folder, f"{prefix}_{file_id}.json")

    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)
            logging.info("Saved %s to %s", prefix, file_path)
    except IOError as e:
        logging.error("Failed to save %s: %s", prefix, str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
