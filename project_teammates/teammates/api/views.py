from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from teammates.models import Student

from .serializers import StudentSerializer


class StudentRetrieveUpdateAPIView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
