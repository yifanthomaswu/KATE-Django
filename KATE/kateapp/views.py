from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from .models import People, Classes

from .models import Classes, People, Courses, Term, Courses_Term, Courses_Classes, Exercises, Period

def index(request):
    return render(request, 'kateapp/home.html')

def personal_page(request):
    login = "md3414"
    person = get_object_or_404(People, login=login)
    context = {
        'name' : person.firstname + " " + person.lastname,
        'person' : person,
    }
    return render(request, 'kateapp/personal_page.html', context)

def timetable(request, period_id, letter_yr, login):
    period = get_object_or_404(Period, pk=period_id)
    classes = get_object_or_404(Classes, pk=letter_yr)
    people = get_object_or_404(People, pk=login)
    return render(request, 'kateapp/timetable.html', {'period': period, 'classes': classes, 'people': people})
