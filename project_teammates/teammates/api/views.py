from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from teammates.models import Student, Course, University, StudentCourse, Rating, Comment
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.decorators import api_view

from .serializers import StudentSerializer, CourseSerializer, UniversitySerializer, StudentSearchSerializer
from django.core import serializers
from django.http import HttpResponse
import json
from rest_auth.app_settings import LoginSerializer
from rest_auth.views import LoginView
from rest_auth.registration.views import RegisterView
from rest_auth.models import TokenModel
from django.conf import settings
from rest_framework import status
from django.middleware.csrf import get_token
from rest_framework.generics import CreateAPIView
from rest_auth.registration.app_settings import RegisterSerializer, register_permission_classes
from allauth.account import app_settings as allauth_settings
from rest_auth.app_settings import (TokenSerializer,
                                    JWTSerializer)
from project_teammates.settings import REST_AUTH_SERIALIZERS
from django.utils.translation import ugettext_lazy as _
# from teammates.CustomTokenSerializer import MyTokenSerializer




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
    stud_data = {}
    for student in students:
        ratings = Rating.objects.filter(rating_receiver=student.id).values_list("rating", flat=True)
        comments = Comment.objects.filter(rating_receiver=student.id).values_list("comment", flat=True)
        stud_data[student.id] = {
            "comments": comments,
            "ratings": ratings
        }

    score_dict = function_by_Jagriti(stud_data)
    for student in students:
        student.score=score_dict.get(student.id)
        student.save()
    return HttpResponse("<h1>Success</h1>")


def function_by_Jagriti(dic):
    scores = {}
    for student in dic.keys():
        scores[student] = 4.0

    return scores



class CustomLogin(LoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel


    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': self.user,
                'token': self.token,
                'vibhu':'varshney'
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})
        serialize_data = serializer.data
        serialize_data['session'] = self.request.session.session_key
        serialize_data['csrf'] = get_token(self.request)
        # serialize_data['session'] = self.request
        # print('data:::  ',serialize_data)
        response = Response(serialize_data, status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_jwt.settings import api_settings as jwt_settings
            if jwt_settings.JWT_AUTH_COOKIE:
                from datetime import datetime
                expiration = (datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
                                    self.token,
                                    expires=expiration,
                                    httponly=True)

        print("ress",response)
        return response


class CustomRegisterView(RegisterView):
    serializer_class = RegisterSerializer
    permission_classes = register_permission_classes()
    token_model = TokenModel


    def get_response_data(self, user):
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": _("Verification e-mail sent.")}

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': user,
                'token': self.token
            }
            print("JWT", data)
            return JWTSerializer(data).data
        else:
            # print("Token", TokenSerializer(user.auth_token).data)
            register_data = TokenSerializer(user.auth_token).data
            register_data['session'] = self.request.session.session_key
            register_data['csrf'] = get_token(self.request)
            return register_data