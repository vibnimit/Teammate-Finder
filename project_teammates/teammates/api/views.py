from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from teammates.models import Student, Course, University, StudentCourse
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.decorators import api_view

from .serializers import StudentSerializer, CourseSerializer, UniversitySerializer, StudentSearchSerializer
from django.core import serializers
from django.http import HttpResponse
import json

class StudentListAPIView(ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class CoursesListAPIView(ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class UniversityListAPIView(ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class RetrieveStudentsAPIView(RetrieveAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = StudentSearchSerializer

    def retrieve(self, request, *args, **kwargs):
        course_code = kwargs.get('course_code')
        print('request= ',kwargs.get('course_code'))
        # StudentCourse.objects.filter(code=course_code)
        students = Student.objects.filter(id__in=StudentCourse.objects.filter(course_id='255c4f44-a155-4eb6-9b7b-c8147d081693').values('student_id'))
        serializer = StudentSearchSerializer(students)
        return Response(serializer.data)
        # return students

@api_view()
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def getStudents(request, *args ,**kwargs):
    if request.method == "GET":
        students = Student.objects.filter(id__in=StudentCourse.objects.filter(course_id=kwargs.get('course_id')).values('student_id')).order_by('-score')
        result = serializers.serialize("json", students)

        return HttpResponse(json.dumps(result), content_type='application/json')


def updateStudentRank(request):
    students = Student.objects.all()
    # calculateScore(students)
    students.update(score=10.0)
    return HttpResponse("<h1>Success</h1>")