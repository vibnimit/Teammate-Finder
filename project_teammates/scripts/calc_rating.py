# scripts/delete_all_questions.py

from teammates.models import Student

def run():
    # Fetch all Students
    students = Student.objects.all()

    students.update(score=2.0)