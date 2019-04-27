from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField
# from django.contrib.postgres.fields import JSONField

# Create your models here.

class RecordTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class University(RecordTimeStamp):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(AbstractUser):
    # add additional fields in here
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prof_pic = models.ImageField(upload_to="gs://student_profile_pic/", blank=True, null=True)
    skills = ArrayField(models.CharField(max_length=200), blank=True, null = True)
    university = models.ForeignKey(University, null=True, blank=True, on_delete = models.CASCADE, related_name="students")
    score = models.FloatField(default=0)

    def __str__(self):
        return self.email


class Course(RecordTimeStamp):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "code = %s & courseName = %s" %(self.code, self.name)


class StudentCourse(RecordTimeStamp):
    student_id = models.ForeignKey("Student", null=False, blank=False, on_delete = models.CASCADE, related_name="courses_enrolled")
    course_id = models.ForeignKey(Course, null=False, blank=False, on_delete = models.CASCADE, related_name="students_enrolled")
    enrolled = models.BooleanField(default=True)

    def __str__(self):
        return "student = %s %s & course = %s" %(self.student_id.first_name, self.student_id.last_name, self.course_id.name)

class Rating(RecordTimeStamp):
    rating_giver = models.ForeignKey(Student, null=False, blank=False, on_delete = models.CASCADE, related_name="ratings_given")
    rating_receiver = models.ForeignKey(Student, null=False, blank=False, on_delete = models.CASCADE, related_name="ratings_received")
    rating = models.FloatField(default=0)

    def __str__(self):
        return "giver = %s & receiver = %s & rating = %s" %(self.rating_giver.name, self.rating_receiver.name, self.rating)

class Comment(RecordTimeStamp):
    comment_giver = models.ForeignKey(Student, null=False, blank=False, on_delete = models.CASCADE, related_name="comment_given")
    comment_receiver = models.ForeignKey(Student, null=False, blank=False, on_delete = models.CASCADE, related_name="comment_received")
    comment = models.CharField(max_length=500)

    def __str__(self):
        return "giver = %s & receiver = %s & comment = %s" %(self.comment_giver.name, self.comment_receiver.name,
                                                          self.comment)

class LookingForTeammates(RecordTimeStamp):
    student_id = models.ForeignKey(Student, null=False, blank=False, on_delete = models.CASCADE, related_name="courses_looking_for")
    course_id = models.ForeignKey(Course, null=False, blank=False, on_delete = models.CASCADE, related_name="students_looking_for")

    def __str__(self):
        return "student = %s & course = %s" %(self.student_id.name, self.course_id.name)