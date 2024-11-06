from flask import Flask, request, jsonify
import os
import json
import logging
import uuid
import requests
from datetime import datetime
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

    # Print and save the notification
    logging.info("Received Notification: %s", json.dumps(notification, indent=2))
    notification_filename = save_notification(notification)

    # Extract and show hasEventType
    notification_object = next((item for item in notification.get('@graph', []) if item.get('@type') == "Notification"), None)

    if notification_object:
        event_type = notification_object.get('hasEventType', {}).get('@id')
        logging.info("Event Type: %s", event_type)  # Log the hasEventType for visibility

        # Check if event type matches 'LOGISTICS_EVENT_RECEIVED'
        if event_type != "https://onerecord.iata.org/ns/api#LOGISTICS_EVENT_RECEIVED":
            return jsonify({'status': 'Not a Logistics Event, process ended.'}), 200

        # Proceed with fetching the logistics object ID if the type matches
        logistics_object_id = notification_object.get('hasLogisticsObject', {}).get('@id')
        if logistics_object_id:
            event = fetch_latest_event(logistics_object_id)
            if event:
                # Print and save the event
                logging.info("Fetched Event: %s", json.dumps(event, indent=2))
                event_filename = save_event(event)
                forward_event_to_airtable(event)
        else:
            logging.error("Logistics Object ID missing in the notification.")
    else:
        logging.warning("Notification object not found in the @graph.")

    # Respond with success status after processing and saving
    return jsonify({'status': 'notification processed', 'notification_file': notification_filename}), 200

def save_notification(notification):
    """Save the notification JSON to a file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"notifications/notification_{timestamp}_{uuid.uuid4().hex}.json"
    with open(filename, 'w') as file:
        json.dump(notification, file, indent=2)
    logging.info("Notification saved to %s", filename)
    return filename

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

def save_event(event):
    """Save the event JSON to a file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"events/event_{timestamp}_{uuid.uuid4().hex}.json"
    with open(filename, 'w') as file:
        json.dump(event, file, indent=2)
    logging.info("Event saved to %s", filename)
    return filename

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
