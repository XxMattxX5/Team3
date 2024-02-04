from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('student/', views.student, name="student"),
    path('teacher/', views.teacher, name="teacher"),
    path('register/', views.register, name="register"),
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutuser, name="logout"),
    path('home/', views.home, name="home"),
    path('user/', views.userpage, name='user')
]
