from django.urls import path

from .views import getStudents, StudentListAPIView, CoursesListAPIView, UniversityListAPIView, RetrieveStudentsAPIView


urlpatterns = [
    path('students/', StudentListAPIView.as_view()),
    path('courses/', CoursesListAPIView.as_view()),
    path('universities/', UniversityListAPIView.as_view()),
    # path('searchUsers/<str:course_id>', RetrieveStudentsAPIView.as_view())
    path('searchUsers/<str:course_id>', getStudents)
]