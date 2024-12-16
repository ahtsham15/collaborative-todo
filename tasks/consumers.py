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
                self.room_group_name,
                self.channel_name
            )
            self.accept()
            logger.info("WebSocket connected.")
            self.send(text_data=json.dumps({"message": "Connected to the Django channel server"}))
        except Exception as e:
            logger.error(f"Error during connection: {e}")
            self.close()

    def receive(self, text_data):

        print(text_data)
        self.send(text_data=json.dumps({"status":"Success"}))
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
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"WebSocket disconnected with code: {close_code}")
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")

    def task_update(self, event):
        # Send message to WebSocket
        print("event: ", event)
        self.send(text_data=json.dumps({
            'message': event['message']
        }))


# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
# import json
# import logging

# logger = logging.getLogger(__name__)

# class TestConsumer(WebsocketConsumer):
#     def connect(self):
#         try:
#             # Dynamically get room_name from the URL
#             self.room_name = self.scope['url_route']['kwargs']['room_name']
#             self.room_group_name = f"task_list_{self.room_name}"

#             # Add the connection to the group
#             async_to_sync(self.channel_layer.group_add)(
#                 self.room_group_name,
#                 self.channel_name
#             )
#             self.accept()
#             logger.info(f"WebSocket connected to room: {self.room_name}.")
#             self.send(text_data=json.dumps({"message": "Connected to the WebSocket group"}))
#         except KeyError:
#             logger.error("Room name not provided in the WebSocket URL.")
#             self.close()
#         except Exception as e:
#             logger.error(f"Error during connection: {e}")
#             self.close()

#     def receive(self, text_data):
#         # Just echoing back for now
#         logger.info(f"Received message: {text_data}")
#         self.send(text_data=json.dumps({"status": "Success"}))

#     def disconnect(self, close_code):
#         try:
#             # Remove the connection from the group
#             async_to_sync(self.channel_layer.group_discard)(
#                 self.room_group_name,
#                 self.channel_name
#             )
#             logger.info(f"WebSocket disconnected: {close_code}")
#         except Exception as e:
#             logger.error(f"Error during disconnect: {e}")

#     def task_update(self, event):
#         # Send task update message to WebSocket
#         print("event: ", event)
#         self.send(text_data=json.dumps({
#             'message': event['message']
#         }))


