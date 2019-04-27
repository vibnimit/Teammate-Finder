from django.contrib import admin

# Register your models here.
# from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Student, University, Course, StudentCourse, Rating, Comment, LookingForTeammates

class UniversityAdmin():
    model = University
    list_display = ['id', 'name']

class CustomUserAdmin(UserAdmin):
    model = Student
    list_display = ['email', 'username','first_name','skills','university' ]


admin.site.register(Student, CustomUserAdmin)
admin.site.register(University)
admin.site.register(Course)
admin.site.register(StudentCourse)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(LookingForTeammates)