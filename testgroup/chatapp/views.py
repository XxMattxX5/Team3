from django.shortcuts import render, HttpResponse, redirect
from .models import Room, Message
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import calendar

# Create your views here.
def chathome(request):
    return render(request, "chatapp/chathome.html")

@login_required(login_url="chathome")
def chatroom(request):
    if request.method == "POST":
        name = request.POST.get('roomname')
        rooms = Room.objects.get(name=name) 
        context = {
            "room": rooms,
            "messages": Message.objects.filter(room=rooms.id)
        }
        return render(request, "chatapp/chatroom.html", context)
    
    return render(request, "chatapp/chathome.html")

@login_required(login_url="chathome")
def addmessage(request):
    if request.method == "POST":
        user = request.POST.get("userid")
        room = request.POST.get("roomid")
        room = Room.objects.get(id=room)
        user = User.objects.get(id=user)

        newmessage = request.POST.get("newmessage")

        m = Message(value=newmessage, user=user, room=room)
        m.save()
        message = Message.objects.filter(room=room.id).values()
        message = list(message)
        formatedDate = ""
        for i in range(len(message)):
            message[i]['user_id'] = User.objects.get(id=message[i]['user_id']).username
            formatedDate += calendar.month_name[(message[i]['date'].month)][0:3] + "."
            formatedDate += f" {message[i]['date'].day},"
            formatedDate += f" {message[i]['date'].year},"
            if message[i]['date'].hour > 12:
                formatedDate += f" {message[i]['date'].hour - 12}:"
            else:  
                formatedDate += f" {message[i]['date'].hour}:"
            
            if message[i]['date'].minute > 9:
                formatedDate += f"{message[i]['date'].minute}"
            else:
                formatedDate += f"0{message[i]['date'].minute}"

            if message[i]['date'].hour > 12:
                 formatedDate += " p.m."
            else:
                formatedDate += " a.m."
            message[i]['date'] = formatedDate
            formatedDate = ""
        message = JsonResponse(message, safe=False)
        
        return HttpResponse(message, content_type="application/json")

    else:
        return render(request, "chatapp/chathome.html")
    
def loadmessages(request):
    if request.method == "POST":
        
        room = request.POST.get("roomid")
        room = Room.objects.get(id=room)

        message = Message.objects.filter(room=room.id).values()
        message = list(message)
        formatedDate = ""
        for i in range(len(message)):
            message[i]['user_id'] = User.objects.get(id=message[i]['user_id']).username
            formatedDate += calendar.month_name[(message[i]['date'].month)][0:3] + "."
            formatedDate += f" {message[i]['date'].day},"
            formatedDate += f" {message[i]['date'].year},"
            if message[i]['date'].hour > 12:
                formatedDate += f" {message[i]['date'].hour - 12}:"
            else:  
                formatedDate += f" {message[i]['date'].hour}:"
            
            if message[i]['date'].minute > 9:
                formatedDate += f"{message[i]['date'].minute}"
            else:
                formatedDate += f"0{message[i]['date'].minute}"

            if message[i]['date'].hour > 12:
                 formatedDate += " p.m."
            else:
                formatedDate += " a.m."
            message[i]['date'] = formatedDate
            formatedDate = ""
        message = JsonResponse(message, safe=False)
        
        return HttpResponse(message, content_type="application/json")
    
def createroom(request):
    if request.method == "POST":
        roomname = request.POST.get("newroomname")
        newroom = Room(name=roomname)
        newroom.save()
        return redirect("chatroom")
    else:
        return render(request, "chatapp/createroom.html")
    


def chathome2(request):
    return HttpResponse("Hello")

def room(request, room_name):
    context = {
        'room_name': room_name
    }
    return render(request, 'chatapp/room.html', context)