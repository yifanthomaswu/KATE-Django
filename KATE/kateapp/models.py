from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.postgres.fields import ArrayField
import os

@python_2_unicode_compatible
class Classes(models.Model):
    letter_yr = models.CharField(max_length=2, primary_key=True)
    def __str__(self):
        return self.letter_yr

@python_2_unicode_compatible
class Courses(models.Model):
    code = models.CharField(max_length=200, primary_key=True)
    title = models.CharField(max_length=200)
    lecturer = models.ForeignKey('People', on_delete=models.PROTECT)
    def __str__(self):
        return self.code + " " + self.title

@python_2_unicode_compatible
class People(models.Model):
    login = models.CharField(max_length=200, primary_key=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    student_letter_yr = models.ForeignKey(Classes, on_delete=models.PROTECT, null=True)
    tutor = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    required_courses = models.ManyToManyField(Courses, related_name='required')
    registered_courses = models.ManyToManyField(Courses, related_name='registered')
    def __str__(self):
        return self.login

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

    COURSEWORK = 'CW'
    PROJECT = 'PROJ'
    REPORT = 'REP'
    TEST = 'T'
    EXAM = 'WES'
    TUTORIAL = 'TUT'
    TYPE_CHOICES = (
        (COURSEWORK, 'Coursework'),
        (PROJECT, 'Project'),
        (REPORT, 'Report'),
        (TEST, 'Test'),
        (EXAM, 'Exam'),
        (TUTORIAL, 'Tutorial'),
    )

    NO = 'NO'

    INDIVIDUAL = 'INDIVIDUAL'
    GROUP = 'GROUP'
    ASSESSMENT_CHOICES = (
        (NO, 'No Assessment'),
        (INDIVIDUAL, 'Individual'),
        (GROUP, 'Group'),
    )

    HARDCOPY = 'HARDCOPY'
    ELECTRONIC = 'ELECTRONIC'
    SUBMISSION_CHOICES = (
        (NO, 'No submission'),
        (HARDCOPY, 'Hardcopy'),
        (ELECTRONIC, 'Electronic'),
    )

    exercise_type = models.CharField(
        max_length=15,
        choices=TYPE_CHOICES,
    )
    assessment = models.CharField(
        max_length=15,
        choices=ASSESSMENT_CHOICES,
        default=NO,
    )
    submission = models.CharField(
        max_length=15,
        choices=SUBMISSION_CHOICES,
        default=NO,
    )

    esubmission_files_names = ArrayField(models.CharField(max_length=50), default=[])

    mark_release_date = models.DateTimeField(null=True)

    class Meta:
        unique_together = (('code', 'number'),)
    def __str__(self):
        return self.code.code + " " + self.number.__str__()  + " " + self.title + ": " + self.start_date.__str__() + " ~ " + self.deadline.__str__()

@python_2_unicode_compatible
class Period(models.Model):
    period = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return self.period.__str__() + " " + self.period.name + ": " + self.start_date.__str__() + " ~ " + self.end_date.__str__()

@python_2_unicode_compatible
class Resource(models.Model):
    file = models.FileField(upload_to='')
    timestamp = models.DateTimeField(auto_now=True)
    def filename(self):
        return os.path.basename(self.file.name)
    def __str__(self):
        return self.file.name + " " + self.timestamp.__str__()

@python_2_unicode_compatible
class Courses_Resource(models.Model):
    code = models.ForeignKey(Courses, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True)
    link = models.URLField(null=True)
    release_date = models.DateField()

    NOTE = 'NOTE'
    PROBLEM = 'PROBLEM'
    URL = 'URL'
    PANOPTO = 'PANOPTO'
    PIAZZA = 'PIAZZA'
    HOMEPAGE = 'HOMEPAGE'
    TYPE_CHOICES = (
        (NOTE, 'Note'),
        (PROBLEM, 'Problem'),
        (URL, 'Url'),
        (PANOPTO, 'Panopto'),
        (PIAZZA, 'Piazza'),
        (HOMEPAGE, 'Homepage'),
    )
    course_resource_type = models.CharField(
        max_length=15,
        choices=TYPE_CHOICES,
        default=NOTE,
    )
    def __str__(self):
        return self.code.__str__() + " " + self.resource.__str__()

@python_2_unicode_compatible
class Exercises_Resource(models.Model):
    exercise = models.ForeignKey(Exercises, on_delete=models.PROTECT)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    SPECIFICATION = 'SPEC'
    DATA = 'DATA'
    ANSWER = 'ANSWER'
    MARKING = 'MARKING'
    TYPE_CHOICES = (
        (SPECIFICATION, 'Specification'),
        (DATA, 'Data file'),
        (ANSWER, 'Model answer'),
        (MARKING, 'Marking scheme'),
    )
    exercise_resource_type = models.CharField(
        max_length=15,
        choices=TYPE_CHOICES,
        default=SPECIFICATION,
    )
    def __str__(self):
        return self.exercise.__str__() + " " + self.resource.__str__()

@python_2_unicode_compatible
class Submissions(models.Model):
    exercise = models.ForeignKey(Exercises, on_delete=models.PROTECT)
    leader = models.ForeignKey(People, on_delete=models.PROTECT, related_name='leader')
    members = models.ManyToManyField(People, related_name='members')
    files = models.ManyToManyField(Resource)
    timestamp = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.exercise.code.code + " " + self.exercise.number.__str__() + " " + self.leader.__str__() + self.members.all().__str__()

@python_2_unicode_compatible
class Marks(models.Model):
    exercise = models.ForeignKey(Exercises, on_delete=models.PROTECT)
    login = models.ForeignKey(People, on_delete=models.PROTECT)
    mark = models.DecimalField(max_digits=5, decimal_places=2)
    released = models.BooleanField(default=False)
    def __str__(self):
        return self.login.__str__() + " " + self.exercise.code.code + " " + self.exercise.number.__str__() + " " + self.mark.__str__()
