import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message
from asgiref.sync import sync_to_async
import re
from django.contrib.auth.models import User
from django.utils.timezone import localtime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # Sanitize the room name to remove invalid characters
        sanitized_room_name = re.sub(r"[^a-zA-Z0-9\-\.]", "_", self.room_name)
        self.room_group_name = f'chat_{sanitized_room_name}'

        # Check if the room exists in the database
        room_exists = await sync_to_async(
            lambda: Room.objects.filter(name=self.room_name).exists()
        )()

        if not room_exists:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        author_id = text_data_json.get('author_id')

        # Retrieve the username from the author_id
        try:
            author = await sync_to_async(User.objects.get)(id=author_id)
            username = author.username
        except User.DoesNotExist:
            print("User not found.")
            return

        timestamp = localtime().isoformat()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,  # Send the username
                'timestamp': timestamp
            }
        )


        # Save the message to the database
        await sync_to_async(self.save_message)(message, author_id)


    # In your ChatConsumer
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))



    def save_message(self, message, author_id):
        try:
            room = Room.objects.get(name=self.room_name)
            author = User.objects.get(id=author_id)
            Message.objects.create(room=room, content=message, author=author)
        except (Room.DoesNotExist, User.DoesNotExist, ValueError):
            # Handle the case where the room, user does not exist, or invalid author_id
            print(f"Invalid data. Room: {self.room_name}, Author ID: {author_id}")



