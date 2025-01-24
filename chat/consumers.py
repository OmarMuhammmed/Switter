import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Get room_name from the URL and extract room_id (numeric part)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_id = int(self.room_name.split('_')[-1])  # Extract numeric part
        self.room_group_name = f"chat_{self.room_id}"

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

        # Fetch sender object from the database
        sender = await database_sync_to_async(User.objects.get)(username=sender_username)
        
        # Fetch or create the conversation object using room_id
        try:
            conversation = await database_sync_to_async(Conversation.objects.get)(id=self.room_id)
        except Conversation.DoesNotExist:
            conversation = await database_sync_to_async(Conversation.objects.create)()
            await database_sync_to_async(conversation.participants.add)(sender)
        
      
        # Save the message to the database
        await database_sync_to_async(Message.objects.create)(
            conversation=conversation,
            sender=sender,
            content=message
        )
        

        # Send the message to the group
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
