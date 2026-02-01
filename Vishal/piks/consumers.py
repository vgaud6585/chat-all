import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import PrivateChat

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = data['sender']
        receiver = data['receiver']

        # Database mein save karein
        await self.save_message(sender, receiver, message)

        # Group mein broadcast karein
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    @database_sync_to_async
    def save_message(self, sender, receiver, message):
        return PrivateChat.objects.create(sender=sender, receiver=receiver, message=message)
    # @database_sync_to_async
    # def save_message(self, sender, receiver, message):
    #     return PrivateChat.objects.create(sender=sender, receiver=receiver, message=message)