from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader

from .models import Classes, People, Courses, Term, Courses_Term, Courses_Classes, Exercises, Period

import datetime, calendar

def index(request):
    return render(request, 'kateapp/home.html')

def personal_page(request):
    login = "yw8012"
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
    months = []
    d_count = 0
    current_d = period.start_date + timedelta(0)
    current_m = current_d.month
    # while (current_d <= period.end_date):

    # for m in range(period.start_date.month, period.end_date.month):
    #     d = calendar.monthrange(year, month)
    #     months.append((calendar.month_name[m], ))
    return render(request, 'kateapp/timetable.html', {'period': period, 'classes': classes, 'people': people})
