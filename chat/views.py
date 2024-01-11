import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from django.utils.timezone import localtime

@login_required
def index(request):
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})

@login_required
def room(request, room_name):
    if not Room.objects.filter(name=room_name).exists():
        return redirect('chat:index')
    
    messages = Message.objects.filter(room__name=room_name).order_by('timestamp')
    formatted_messages = [
        {
            'author_id': message.author.id,
            'username': message.author.username,
            'message': message.content,
            'timestamp': localtime(message.timestamp).isoformat()
        }
        for message in messages
    ]

    json_messages = json.dumps(formatted_messages)
    return render(request, 'chat/chat.html', {
        'room_name': room_name,
        'user_id': request.user.id,
        'json_messages': json_messages
    })
        

@login_required
def create_room(request):
    if request.method == "POST":
        room_name = request.POST.get('room_name')
        Room.objects.get_or_create(name=room_name)
        return redirect('chat:room', room_name=room_name)
    return render(request, 'chat/create_room.html')
