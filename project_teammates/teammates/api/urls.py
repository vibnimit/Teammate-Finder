from django.urls import path

from .views import StudentRetrieveUpdateAPIView


urlpatterns = [
    path('', StudentRetrieveUpdateAPIView.as_view())

]