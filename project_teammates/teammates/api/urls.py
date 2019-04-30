from django.urls import path

from .views import getStudents, submitFeedback, StudentListAPIView, CoursesListAPIView, UniversityListAPIView, RetrieveStudentsAPIView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('students/', StudentListAPIView.as_view()),
    path('courses/', CoursesListAPIView.as_view()),
    path('universities/', UniversityListAPIView.as_view()),
    # path('searchUsers/<str:course_id>', RetrieveStudentsAPIView.as_view())
    path('searchUsers/<str:course_id>', getStudents),
    path('submitFeedback', submitFeedback)
]