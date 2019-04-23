from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField
# from django.contrib.postgres.fields import JSONField

# Create your models here.

class University(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(AbstractUser):
    # add additional fields in here
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prof_pic = models.ImageField(upload_to="gs://student_profile_pic/", blank=True, null=True)
    skills = ArrayField(models.CharField(max_length=200), blank=True, null = True)
    university = models.ForeignKey(University, null=True, blank=True, on_delete = models.CASCADE)

    def __str__(self):
        return self.email


