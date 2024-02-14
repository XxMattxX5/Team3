from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message, Room
from channels.db import database_sync_to_async
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
from datetime import date, datetime

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        messages, senders, dates = await database_sync_to_async(self.get_messages)()

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'tester_message',
                'message': messages,
                'senders': senders,
                'dates': dates,
            }
        )

    async def tester_message(self, event):
        message = event['message']
        senders = event['senders']
        dates = event['dates']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': senders,
            'date': dates
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        room = text_data_json['room']
        user = await self.get_user(user)
        room = await self.get_room(room)
        await self.addmessage(message, user, room)

        messages, senders, dates = await database_sync_to_async(self.get_messages)()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'tester_message',
                'message': messages,
                'senders': senders,
                'dates': dates,
            }
        )

    
    def get_messages(self):
        room_name = self.scope['url_route']['kwargs']['room_name']
        room = Room.objects.get(name=room_name)
        message = Message.objects.filter(room=room).values()
        message = list(message)
        
        messages = []
        senders = []
        dates = []
    
        for i in range(len(message)):
           messages.append(message[i]['value'])
           senders.append(User.objects.filter(id=message[i]['user_id']).values_list('username')[0][0])
           dates.append(message[i]['date'].strftime('%b. %d, %Y, %I:%M %p'))

        return messages, senders, dates
    
    @database_sync_to_async
    def get_user(self, id):
        user = User.objects.get(id=id)
        return user
    
    @database_sync_to_async
    def get_room(self, name):
        room = Room.objects.get(name=name)
        return room
    
    @database_sync_to_async
    def addmessage(self, message, user, room):
        m = Message(value=message, user=user, room=room)
        m.save()