from rest_framework import serializers
from teammates.models import Student, Course, University

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('__all__')


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('__all__')


class UniversitySerializer(serializers.ModelSerializer):

    class Meta:
        model = University
        fields = ('__all__')


class StudentSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('__all__')