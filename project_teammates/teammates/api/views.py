from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from teammates.models import Student, Course, University, StudentCourse, Rating, Comment
from teammates.views import get_data
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

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
from project_teammates.settings import BASE_DIR
#============================================================================
import argparse
import sys
import six
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
import statistics
import uuid

#=============================================================================
# from teammates.CustomTokenSerializer import MyTokenSerializer


# path = "CSE578-43fcff5cabbc.json"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

class StudentListAPIView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class CoursesListAPIView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class UniversityListAPIView(ListAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class RetrieveStudentsAPIView(RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = StudentSearchSerializer

    def retrieve(self, request, *args, **kwargs):
        course_code = kwargs.get('course_code')
        print('request= ',kwargs.get('course_code'))
        # StudentCourse.objects.filter(code=course_code)
        students = Student.objects.filter(id__in=StudentCourse.objects.filter(course_id='255c4f44-a155-4eb6-9b7b-c8147d081693',  is_active = True).values('student_id'))
        serializer = StudentSearchSerializer(students)
        return Response(serializer.data)
        # return students

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def getStudents(request, *args ,**kwargs):
    if request.method == "GET":
        # session = request.GET.get('session')
        # print("============  Matched ==============", request.user)
        # print('key  ',get_token(request))
        # if session == request.session.session_key:
        #     print("============  Matched ==============")
        filtered_result = []
        students = Student.objects.filter(id__in=StudentCourse.objects.filter(course_id=kwargs.get('course_id'), is_active=True).values('student_id')).order_by('-score')
        result = serializers.serialize("json", students)
        # print('result============> ', result)
        results = json.loads(result)
        for result in results:
            filtered_result.append(
                {
                    "student_id": result['pk'],
                    "username": result['fields']['username'],
                    "first_name": result['fields']['first_name'],
                    "last_name": result['fields']['last_name'],
                    "email": result['fields']['email'],
                    "skills": result['fields']['skills'],
                    "university": result['fields']['university'],
                    "score": result['fields']['score'],
                    "students_rated": result['fields']['students_rated'],
                    "students_reviewed": result['fields']['students_reviewed'],
                    "avg_rating": result['fields']['avg_rating'],
                    "words": json.loads(result['fields']['words'])[:5] if result['fields']['words'] else []
                })

        return HttpResponse(json.dumps(filtered_result), content_type='application/json')

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def submitFeedback(request):
    if request.method == 'POST':
        decoded = request.body.decode('utf-8')
        print(json.loads(decoded))
        # request.body = request.body.decode('utf-8')
        json_obj = json.loads(decoded)
        giver = json_obj.get('student_from')
        print(giver)
        receiver = json_obj['student_to']
        comment = json_obj['comment']
        rating = json_obj.get('rating', None)

        if not rating:
            print('not rating')
            return HttpResponse("Rating is Mandatory", status=400, content_type="application/text")
        if rating:
            Rating.objects.create(rating_giver_id = giver, rating_receiver_id = receiver, rating = rating)

        if comment:
            Comment.objects.create(comment_giver_id=giver, comment_receiver_id=receiver, comment=comment)
        return HttpResponse("Success", status=200, content_type="application/text")



def updateStudentRank(request):
    students = Student.objects.all()
    # calculateScore(students)
    stud_data = {}
    for student in students:
        ratings = Rating.objects.filter(rating_receiver=student.id).values_list("rating", flat=True)
        comments = Comment.objects.filter(comment_receiver=student.id).values_list("comment", flat=True)
        stud_data[str(student.id)] = {
            "comments": list(comments),
            "ratings": list(ratings)
        }
    # print("===========>> ",stud_data)
    score_dict = function_by_Jagriti(stud_data)
    # print("==============================&===================  \n", score_dict)
    for student in students:
        calculated_values = score_dict.get(str(student.id))
        # print("values = ", calculated_values)
        if calculated_values:
            student.score = calculated_values[0]
            student.students_rated = calculated_values[1]
            student.students_reviewed = calculated_values[2]
            student.avg_rating = calculated_values[3]
            student.words = json.dumps(calculated_values[4]) if len(calculated_values[4]) !=0 else []
            student.save()
    return HttpResponse("<h1>Success</h1>")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------Modified by Jagriti---------------------------------------------------------------

def entity_sentiment_text(annotations,text):
    client = language.LanguageServiceClient()
    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')
    document = types.Document(content=text,type=enums.Document.Type.PLAIN_TEXT)
    encoding = enums.EncodingType.UTF32
    if sys.maxunicode == 65535:
        encoding = enums.EncodingType.UTF16
    result = client.analyze_entity_sentiment(document)
    for entity in result.entities:
        # print(u'Name: "{}"'.format(entity.name))
        for mention in entity.mentions:
            print(u'Magnitude : {}'.format(mention.sentiment.magnitude))
        if entity.sentiment.score>0:
            print('Positive\n')
        elif entity.sentiment.score<0:
            print('Negative\n')
        else:
            print("Neutral\n")


def print_result(annotations,content):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude
    if score>0:
        sent = 'Positive'
    elif score<0:
        sent = 'Negative'
    else:
        sent = "Neutral"
    # print("Overall Sentiment: {}, Magnitude {}, Score {}\n".format(sent, magnitude, score))
    #entity_sentiment_text(annotations,content)
    return score



def analyze(content):
    client = language.LanguageServiceClient()
    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)
    sent_score = print_result(annotations,content)
    return sent_score


def function_by_Jagriti(dic):
    scores = {}

    path = BASE_DIR+"/teammates/api/CSE578-43fcff5cabbc.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path     #####Check this before running the code
    for student in dic.keys():
        review_score = 0.0
        rating_score = 0.0
        temp = []
        word_sentiment = []
        #scores[student] = 4.0
        each_stud = dic[student]
        list_comment = each_stud['comments']
        student_rating = each_stud['ratings']
        if list_comment:
            avg_review_score = []
            word_sentiment = performSentimentAnalysis(list_comment)
            for comment in list_comment:
                overall_sent_score = analyze(comment)
                avg_review_score.append(overall_sent_score)
                print("ooo", overall_sent_score)
            review_score = statistics.mean(avg_review_score)    ####Final review score
            # print('rrrrrrrrrrr',review_score)
        if student_rating:
            normalized_rating_score = [x for x in student_rating] ##removed /5 to have it in scale 0 to 5
            rating_score = statistics.mean(normalized_rating_score)  ####Final rating score
        # print("arrarara", rating_score)
        scor = review_score*5 + rating_score  ##for a scale of 0 to 10
        temp.append(round(scor,2))
        temp.append(len(list_comment))
        temp.append(len(student_rating))
        temp.append(rating_score)
        temp.append(word_sentiment)
        scores[student] = temp
        # print('score=  ', scor)
    # print('temp=  ', temp)
    return scores                                                   ### scores = {stud_id: [overall_rating, no of people commented, no of people rated],stud_id:[overall_rating, no of people commented, no of people rated]}
	
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
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
            }
            serializer = serializer_class(instance=data,
                                          context={'request': self.request})
        else:
            serializer = serializer_class(instance=self.token,
                                          context={'request': self.request})
        serialize_data = serializer.data
        serialize_data['session'] = self.request.session.session_key
        serialize_data['csrf'] = get_token(self.request)
        serialize_data['name'] = self.user.first_name+" "+self.user.last_name
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

        # print("ress",response)
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

# @csrf_exempt
@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_or_setCourses(request, student_id=None):
    if request.method == 'POST':
        # print(request.POST.__dict__)
        print("===========",request.data)
        if request.POST.get("student_id", None) == None:
            json_obj = request.data
            # json_obj = json.loads(decoded)
            student_id = json_obj.get('student_id')
            student_id = uuid.UUID(str(student_id)).hex
            courses = json_obj.get("courses")

        else:
            student_id = request.POST.get("student_id")
            courses = request.POST.get("courses")
        enrolled = courses.get("current")
        past = courses.get("past")

        enrolled = courses.get("current")
        past = courses.get("past")

        student_obj = Student.objects.get(id = student_id)
        course_enrolled_in_db = student_obj.courses_enrolled.all()
        course_enrolled_in_db.update(is_active=False)

        try:
            for course in enrolled:
                course_obj, created = StudentCourse.objects.update_or_create(student_id_id = student_id, course_id_id = course, defaults={"enrolled": True, "is_active": True})

            for course in past:
                course_obj, created = StudentCourse.objects.update_or_create(student_id_id = student_id, course_id_id = course, defaults={"enrolled": False, "is_active": True})

        except Exception as e:
            print("Exception occurred in get_or_setCourses", e)
            return HttpResponse("Courses Update failed", status = 204, content_type='application/text')

        return HttpResponse("Courses Updated", status = 200, content_type='application/text')

    elif request.method == 'GET':
        # student_id = request.GET.get('student_id', None)
        if student_id == None:
            filtered_data = []
            all_courses = Course.objects.all()
            results = getJSONSerializedData(all_courses) #Note this will data after json.dumps()
            # print(type(json.loads(results)))

            results = json.loads(results)
            for result in results:
                filtered_data.append(
                    {
                        "course_id":result['pk'],
                        "code":result['fields']['code'],
                        "name":result['fields']['name']
                    })

            return HttpResponse(json.dumps(filtered_data), content_type='application/json')
        student = Student.objects.get(id = student_id)
        courses = student.courses_enrolled.filter(is_active=True)
        result = {
            "current":[],
            "past":[]
        }
        for course in courses:
            if course.enrolled:
                result["current"].append({
                    "name": course.course_id.name,
                    "course_id": str(course.course_id_id),
                    "code": course.course_id.code
                })
            elif course.enrolled == False:
                result["past"].append({
                    "name": course.course_id.name,
                    "course_id": str(course.course_id_id),
                    "code": course.course_id.code
                })

        return HttpResponse(json.dumps(result), content_type='application/json')


def getJSONSerializedData(data):
    result = serializers.serialize("json", data)
    return result


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def getStudentInfo(request, student_id=None):
    if request.method == 'GET':
        filtered_result = []
        if student_id != None:
            student_obj = Student.objects.filter(id = student_id)
            result = serializers.serialize("json", student_obj)
            # print('result============> ', result)
            results = json.loads(result)
            for result in results:
                filtered_result.append(
                    {
                        "student_id": result['pk'],
                        "username": result['fields']['username'],
                        "first_name": result['fields']['first_name'],
                        "last_name": result['fields']['last_name'],
                        "email": result['fields']['email'],
                        "skills": json.dumps(result['fields']['skills']),
                        "university": result['fields']['university'],
                        "score": result['fields']['score'],
                        "students_rated": result['fields']['students_rated'],
                        "students_reviewed": result['fields']['students_reviewed'],
                        "avg_rating": result['fields']['avg_rating'],
                        "words": json.loads(result['fields']['words'])[:5]
                    })

        return HttpResponse(json.dumps(filtered_result), content_type='application/json')


def performSentimentAnalysis(comments_list):
    sorted_words = get_data(comments_list)
    # sorted_words = sorted(important_words, key=lambda k: k['count'])
    result = []



    for word in sorted_words.keys():
        result.append(
            {
                "word": word,
                "count": int(sorted_words[word])
                # "sentiment": "positive" if word['positive'] > word['negative'] else "negative"
            }
        )

    # print(type(result))
    return result
# def getStudentsOfACourse(request):
#

