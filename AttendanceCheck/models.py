from datetime import datetime
from django.db import models


class ICcard(models.Model):
    card_id = models.CharField(unique=True, max_length=16)

    def __str__(self):
        return self.card_id


class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    ic_card = models.ForeignKey(ICcard)

    def __str__(self):
        return self.name


class Staff(models.Model):
    staff_id = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    ic_card = models.ForeignKey(ICcard)
    user_name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def authorize(self, user_name, password):
        return self.user_name == user_name and self.password == password


class Course(models.Model):
    course_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50, unique=True)
    year = models.IntegerField()
    # course_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course)
    staff = models.ManyToManyField(Staff)
    student = models.ManyToManyField(Student)

    def __str__(self):
        return self.name

    def count_student(self):
        return Student.objects.filter(enrollment=self).count()

class AttendanceCheckingSession(models.Model):
    enrollment = models.ForeignKey(Enrollment)
    created_on = models.DateTimeField(editable=True)

    def __str__(self):
        return "Attendance checking session created on " + self.created_on

    def init(self):
        student_list = Student.objects.filter(enrollment=self.enrollment)
        # for student in student_list:
            # if StudentStatus.objects.filter(session=self, status=2, student=student).count() == 0:
            #     StudentStatus.objects.create(session=self, status=2, student=student)
        return

class StudentStatus(models.Model):
    status = models.IntegerField()
    student = models.ForeignKey(Student)
    session = models.ForeignKey(AttendanceCheckingSession)

    def __str__(self):
        if self.status == 0:
            return "ontime"
        elif self.status == 1:
            return "late"
        elif self.status == 2:
            return  "absent"
