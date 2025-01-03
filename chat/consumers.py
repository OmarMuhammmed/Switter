import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Get room_name from the URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()


    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_username = text_data_json['sender']

        sender = await database_sync_to_async(User.objects.get)(username=sender_username)
        
       
        try:
            conversation = await database_sync_to_async(Conversation.objects.get)(id=self.room_name)
        except Conversation.DoesNotExist:
            conversation = await database_sync_to_async(Conversation.objects.create)(id=self.room_name)
            await database_sync_to_async(conversation.participants.add)(sender)
        
        await database_sync_to_async(Message.objects.create)(
            conversation=conversation,
            sender=sender,
            content=message
        )

       
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))
