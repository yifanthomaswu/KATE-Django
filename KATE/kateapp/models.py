from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models

@python_2_unicode_compatible
class Classes(models.Model):
    letter_yr = models.CharField(max_length=2, primary_key=True)
    def __str__(self):
        return self.letter_yr

@python_2_unicode_compatible
class People(models.Model):
    login = models.CharField(max_length=200, primary_key=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    student_letter_yr = models.ForeignKey(Classes, on_delete=models.PROTECT, null=True)
    tutor = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    def __str__(self):
        return self.login

@python_2_unicode_compatible
class Courses(models.Model):
    code = models.CharField(max_length=200, primary_key=True)
    title = models.CharField(max_length=200)
    lecturer = models.ForeignKey(People, on_delete=models.PROTECT)
    def __str__(self):
        return self.code + " " + self.title

@python_2_unicode_compatible
class Term(models.Model):
    term = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.term.__str__() + ": " + self.name

@python_2_unicode_compatible
class Courses_Term(models.Model):
    code = models.ForeignKey(Courses, on_delete=models.PROTECT)
    term = models.ForeignKey(Term, on_delete=models.PROTECT)
    def __str__(self):
        return self.code.__str__() + " " + self.term.__str__()

@python_2_unicode_compatible
class Courses_Classes(models.Model):
    code = models.ForeignKey(Courses, on_delete=models.PROTECT)
    letter_yr = models.ForeignKey(Classes, on_delete=models.PROTECT)
    def __str__(self):
        return self.code.__str__() + " " + self.letter_yr.__str__()

@python_2_unicode_compatible
class Exercises(models.Model):
    code = models.ForeignKey(Courses, on_delete=models.PROTECT)
    number = models.IntegerField()
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    deadline = models.DateTimeField()
    class Meta:
        unique_together = (("code", "number"),)
    def __str__(self):
        return self.title + ": " + self.start_date.__str__() + " ~ " + self.deadline.__str__()

@python_2_unicode_compatible
class Period(models.Model):
    period = models.IntegerField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return self.period.__str__() + ": " + self.start_date.__str__() + " ~ " + self.end_date.__str__()
