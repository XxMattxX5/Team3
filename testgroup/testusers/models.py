from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

# Create your models here.


class Teacher(models.Model):
    name = models.CharField(max_length=300)
    role = models.CharField(max_length=10, default="teacher", editable= False)

class Student(models.Model):
    name = models.CharField(max_length=300)
    role = models.CharField(max_length=10, default="student", editable= False)
    teachers = models.ManyToManyField(Teacher, related_name='teachers', blank='true')

class Book(models.Model):
    name = models.CharField(max_length=300)
    isbn = models.CharField(max_length=300)
    teachers = models.ManyToManyField(Teacher, related_name='books')

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', "password2"
        ]