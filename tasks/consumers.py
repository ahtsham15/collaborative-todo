from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import logging

logger = logging.getLogger(__name__)


class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"

        try:
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
            self.accept()
            logger.info("WebSocket connected.")
            self.send(
                text_data=json.dumps(
                    {"message": "Connected to the Django channel server"}
                )
            )
        except Exception as e:
            logger.error(f"Error during connection: {e}")
            self.close()

    def receive(self, text_data):

        print(text_data)
        self.send(text_data=json.dumps({"status": "Success"}))
        # pass
        # try:
        # Parse the incoming JSON data
        #     data = json.loads(text_data)
        #     logger.info(f"Message received: {data}")
        #     # Echo back the data for now
        #     self.send(text_data=json.dumps({"message": f"Received: {data}"}))
        # except json.JSONDecodeError as e:
        #     logger.warning(f"Invalid JSON format: {e}")
        #     self.send(text_data=json.dumps({"error": "Invalid JSON format"}))
        # except Exception as e:
        #     logger.error(f"Error in receive: {e}")
        #     self.close()

    def disconnect(self, close_code):
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name
            )
            logger.info(f"WebSocket disconnected with code: {close_code}")
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")

    def task_update(self, event):
        # Send message to WebSocket
        print("event: ", event)
        self.send(text_data=json.dumps({"message": event["message"]}))
