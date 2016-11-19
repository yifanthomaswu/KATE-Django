from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader

from .models import Classes, People, Courses, Term, Courses_Term, Courses_Classes, Exercises, Period

import datetime, calendar
from datetime import timedelta

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
    while (current_d <= period.end_date):
        if (current_m != current_d.month):
            months.append((calendar.month_name[current_m], d_count))
            d_count = 0
            current_m = current_d.month
        d_count += 1
        current_d = current_d + timedelta(1)
    months.append((calendar.month_name[period.end_date.month], period.end_date.day))
    weeks = []
    d_count = 0
    current_d = period.start_date + timedelta(0)
    while (current_d <= period.end_date):
        d_count += 1
        if (current_d.weekday() == 4):
            weeks.append(d_count)
            d_count = 0
        current_d = current_d + timedelta(1)
    days = []
    current_d = period.start_date + timedelta(0)
    while (current_d <= period.end_date):
        weekday = True
        if (5 <= current_d.weekday() <= 6):
            weekday = False
        days.append((current_d.day, weekday))
        current_d = current_d + timedelta(1)
    context = {
        'period' : period,
        'classes' : classes,
        'people' : people,
        'months' : months,
        'weeks' : weeks,
        'days' : days,
    }
    return render(request, 'kateapp/timetable.html', context)
