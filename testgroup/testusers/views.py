from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Teacher, Student, Book, CreateUserForm
from django.http import JsonResponse
from django.core import serializers
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from django.contrib.auth.forms import UserCreationForm
#Did this work? Yes it did
# Create your views here.

def home(request):
    return HttpResponse("<h1>Home</h1>")

def student(request):
    return HttpResponse("<h1>Student</h1>")

def teacher(request):
    if request.method == 'POST':
        #name = request.POST.get("name")
       # teachers = Teacher.objects.filter(name__contains=name).values()
       # print(teachers)
        ##teachers = list(teachers)
        #teachers = JsonResponse(teachers, safe=False)
        #return HttpResponse(teachers, content_type="application/json")



        if request.POST.get('opt') == "teacher" and request.POST.get("name") != "":
            name = request.POST.get("name")
            teachers = Teacher.objects.filter(name__contains=name).values()
            teachers = list(teachers)
            teachers = JsonResponse(teachers, safe=False)
            return HttpResponse(teachers, content_type="application/json")
        
        if request.POST.get('opt') == "student" and request.POST.get("name") != "":
           name = request.POST.get("name")
           print(name)
           students = Student.objects.filter(name__contains=name).values()
           students = list(students)
           students = JsonResponse(students, safe=False)
           return HttpResponse(students, content_type="application/json")

        if request.POST.get('opt') == "book" and request.POST.get("name") != "":
            name = request.POST.get("name")
            books = Book.objects.filter(name__contains=name).values()
            books = list(books)
            books = JsonResponse(books, safe=False)
            return HttpResponse(books, content_type="application/json")
        
        if request.POST.get('name') == "":
           print()
           return HttpResponse('empty')

    return render(request, 'testusers/choice.html')


def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                us = User.objects.get(username=user)
                if request.POST.get("roles") == "user":
                    group = Group.objects.get(name='User')
                    group.user_set.add(us)
                if request.POST.get("roles") == "eventorganizer":
                    group = Group.objects.get(name='Event Organizer')
                    group.user_set.add(us)

                messages.success(request, "Accounted was created for " + user)
                return redirect("login")
                

        context = {
            'form': form
        }

        return render(request,"testusers/register.html", context)

def loginpage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            print(username)
            print(password)
            user = authenticate(request, username=username, password=password)

            if user is not None:
                print("here")
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, "Username OR password is incorrect")
                return render(request, 'testusers/login.html')

        return render(request, 'testusers/login.html')

def logoutuser(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect("login")

@login_required(login_url='login')
def home(request):
    
    
    return render(request, "testusers/home.html")

@login_required(login_url='login')
def userpage(request):
    if request.user.groups.filter(name="User").exists():
        return render(request, "testusers/user.html")
    else:
        return redirect("home")
