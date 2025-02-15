from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.utils import get_username_max_length
from teammates.api.serializers import UniversitySerializer
from .models import University


class StudentSerializerOveride(RegisterSerializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )

    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    skills = serializers.ListField( child = serializers.CharField())
    students = UniversitySerializer(many = True, read_only = True)

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        print('================dataa============* \n',self.cleaned_data)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])

        return user


    def get_cleaned_data(self):
        # print("***************SELF*************\n",self.__dict__)
        university_id = self.__dict__.get('_kwargs').get('data').get('university')
        try:
            University.objects.get(id=university_id)
        except:
            university_id = None

        if university_id == None:
            university_id = ''

        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'skills': self.validated_data.get('skills', ''),
            'university': university_id,

        }
