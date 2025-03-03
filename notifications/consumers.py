import json
from channels.generic.websocket import AsyncWebsocketConsumer


class dashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['patient_id']
        self.room_group_name = 'medicine-notificaton-%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    #async def receive(self, text_data):
    #    text_data_json = json.loads(text_data)
    #    message = text_data_json['message']
#
    #    # Send message to room group
    #    await self.channel_layer.group_send(
    #        self.room_group_name,
    #        {
    #            'type': 'chat_message',
    #            'message': message
    #        }
    #    )

    # Receive message from room group
    async def send_medicine_notification(self, event):
        message = event['message']
        medicine=event['medicine']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'medicine':medicine
        }))
