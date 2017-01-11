import logging
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.utils import timezone

from ..models import *
from ..forms import MarkingForm

from .helper import get_next_exercise_number

from datetime import datetime, time, timedelta

logger = logging.getLogger('django')


def index(request):
    return render(request, 'kateapp/home.html')

def grading_scheme(request):
    return render(request, 'kateapp/grading_scheme.html')

def course_list(request, letter_yr):
    courses_term1 = list(Courses.objects.filter(courses_classes__letter_yr=letter_yr, courses_term__term=1).order_by('code'))
    courses_term2 = list(Courses.objects.filter(courses_classes__letter_yr=letter_yr, courses_term__term=2).order_by('code'))
    courses_term3 = list(Courses.objects.filter(courses_classes__letter_yr=letter_yr, courses_term__term=3).order_by('code'))
    context = {
        'letter_yr': letter_yr,
        'courses_term1': courses_term1,
        'courses_term2': courses_term2,
        'courses_term3': courses_term3,
    }
    return render(request, 'kateapp/course_list.html', context)


def course(request, code):
    course = get_object_or_404(Courses, pk=str(code))
    terms = get_list_or_404(Term, courses_term__code=str(code))
    terms.sort(key=lambda x: x.term)
    login = "test01"
    teacher = People.objects.get(login=login).student_letter_yr == None
    exercises = Exercises.objects.filter(code=str(code))
    next_number = get_next_exercise_number(exercises)
    exercises_resources = []
    for exercise in list(exercises):
        resources = list(Resource.objects.filter(
            exercises_resource__exercise__code=exercise.code, exercises_resource__exercise__number=exercise.number))
        exercises_resources.append((exercise, resources))
    note = list(Courses_Resource.objects.filter(code=code, course_resource_type='NOTE').order_by('release_date'))
    exercise = list(Courses_Resource.objects.filter(code=code, course_resource_type='PROBLEM').order_by('release_date'))
    url = list(Courses_Resource.objects.filter(code=code, course_resource_type='URL').order_by('release_date'))
    panopto = list(Courses_Resource.objects.filter(code=code, course_resource_type='PANOPTO').order_by('release_date'))
    piazza = list(Courses_Resource.objects.filter(code=code, course_resource_type='PIAZZA').order_by('release_date'))
    homepage = list(Courses_Resource.objects.filter(code=code, course_resource_type='HOMEPAGE').order_by('release_date'))
    resource = (note, exercise, url, panopto, piazza, homepage)
    context = {
        'course': course,
        'terms': terms,
        'teacher': teacher,
        'exercises_resources': exercises_resources,
        'next_number': next_number,
        'NO': Exercises.NO,
        'resource': resource,
    }
    return render(request, 'kateapp/course.html', context)
