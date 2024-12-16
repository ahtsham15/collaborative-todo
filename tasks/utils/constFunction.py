from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_task_update_message(channel_name, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        channel_name,
        {
            "type": "task_update",
            "message": message
        }
    )