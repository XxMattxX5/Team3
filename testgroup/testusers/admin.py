from django.contrib import admin
from .models import Student, Teacher, Book

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Book)
