from django.urls import path

from .views import getStudents, getStudentInfo, get_or_setCourses, submitFeedback, StudentListAPIView, CoursesListAPIView, UniversityListAPIView, RetrieveStudentsAPIView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('students/', StudentListAPIView.as_view()),
    path('courses/', get_or_setCourses),
    path('courses/<str:student_id>', get_or_setCourses),
    path('universities/', UniversityListAPIView.as_view()),
    # path('searchUsers/<str:course_id>', RetrieveStudentsAPIView.as_view())
    path('searchUsers/<str:course_id>', getStudents),
    path('submitFeedback', submitFeedback),
    path('get_student_info/<str:student_id>', getStudentInfo)

]