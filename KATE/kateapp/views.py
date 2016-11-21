from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponse
from django.template import loader

from .models import Classes, People, Courses, Term, Courses_Term, Courses_Classes, Exercises, Period

import datetime, calendar
from datetime import timedelta

def index(request):
    return render(request, 'kateapp/home.html')

def personal_page(request):
    login = "test01"
    person = get_object_or_404(People, login=login)
    context = {
        'person' : person,
    }
    return render(request, 'kateapp/personal_page.html', context)

def timetable(request, period_id, letter_yr, login):
    period = get_object_or_404(Period, pk=period_id)
    classes = get_object_or_404(Classes, pk=letter_yr)
    person = get_object_or_404(People, pk=login)
    courses = get_list_or_404(Courses_Classes, letter_yr=person.student_letter_yr)
    term_id = 0
    if period_id == 1:
        term_id = 1
    elif period_id == 3:
        term_id = 2
    elif period_id == 5:
        term_id = 3
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
        'person' : person,
        'months' : months,
        'weeks' : weeks,
        'days' : days,
    }
    return render(request, 'kateapp/timetable.html', context)

def course_list(request, letter_yr):
    courses_term1 = get_list_or_404(Courses, courses_classes__letter_yr=letter_yr, courses_term__term=1)
    courses_term2 = get_list_or_404(Courses, courses_classes__letter_yr=letter_yr, courses_term__term=2)
    courses_term3 = get_list_or_404(Courses, courses_classes__letter_yr=letter_yr, courses_term__term=3)
    context = {
        'letter_yr' : letter_yr,
        'courses_term1' : courses_term1,
        'courses_term2' : courses_term2,
        'courses_term3' : courses_term3,
    }
    return render(request, 'kateapp/course_list.html', context)

def course(request, letter_yr, code):
    course = get_object_or_404(Courses, courses_classes__letter_yr=letter_yr, pk=str(code))
    terms = get_list_or_404(Term, courses_term__code=str(code))
    terms.sort(key=lambda x: x.term)
    login = "test01"
    teacher = People.objects.get(login=login).student_letter_yr == None
    #exercises = get_list_or_404(Exercises, code=str(code))
    #exercises.sort(key=lambda x: x.number)
    context = {
        'course' : course,
        'letter_yr' : letter_yr,
        'terms' : terms,
        'teacher' : teacher,
        #'exercises' : exercises,
    }
    return render(request, 'kateapp/course.html', context)
