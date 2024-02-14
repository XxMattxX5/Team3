from django.urls import path
from . import views

urlpatterns = [

    path('', views.chathome, name="chathome"),
    path('chatroom/', views.chatroom, name="chatroom"),
    path('addmessage/', views.addmessage, name="addmessage"),
    path('loadmessages/', views.loadmessages, name="loadmessages"),
    path('createroom/', views.createroom, name="createroom"),
    path('chathome2/', views.chathome2, name="chathome2"),
    path('<str:room_name>/', views.room, name="room"),


    
]