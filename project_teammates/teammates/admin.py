from django.contrib import admin

# Register your models here.
# from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Student

class CustomUserAdmin(UserAdmin):
    model = Student
    list_display = ['email', 'username','first_name','skills','university' ]

admin.site.register(Student, CustomUserAdmin)