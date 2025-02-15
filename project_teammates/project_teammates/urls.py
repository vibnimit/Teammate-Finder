"""project_teammates URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from allauth.account.views import confirm_email
# from scripts.calc_rating import
from teammates.api.views import updateStudentRank
from teammates.api.views import CustomLogin, CustomRegisterView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/login/', CustomLogin.as_view()),
    path('rest-auth/registration/', CustomRegisterView.as_view()),

    path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/account-confirm-email/(?P<key>.+)/', confirm_email, name='account_confirm_email'),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/',include('teammates.api.urls')),
    path('cron/calculateScore', updateStudentRank)

]
