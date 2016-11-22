from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.db.models import Max

from .models import Classes, People, Courses, Term, Courses_Term, Courses_Classes, Exercises, Period
from .forms import NewExerciseForm

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
    person = get_object_or_404(People, pk=login)
    term_id = 0
    if period.period == 1:
        term_id = 1
    elif period.period == 3:
        term_id = 2
    elif period.period == 5:
        term_id = 3
    courses = []
    if term_id != 0:
        courses = get_list_or_404(Courses.objects.order_by('code'), courses_classes__letter_yr=letter_yr, courses_term__term=term_id)
    courses_exercises = []
    for course in courses:
        exercises = list(Exercises.objects.filter(code=course.code).order_by('number'))
        exercises_date = []
        for exercise in exercises:
            exercises_date.append(((exercise.start_date.date() - period.start_date).days, (exercise.deadline.date() - period.start_date).days))
        courses_exercises.append((course, exercises, exercises_date))
    months = []
    d_count = 0
    current_d = period.start_date + timedelta(0)
    current_m = current_d.month
    while current_d <= period.end_date:
        if current_m != current_d.month:
            months.append((calendar.month_name[current_m], d_count))
            d_count = 0
            current_m = current_d.month
        d_count += 1
        current_d = current_d + timedelta(1)
    months.append((calendar.month_name[period.end_date.month], period.end_date.day))
    weeks = []
    d_count = 0
    current_d = period.start_date + timedelta(0)
    while current_d <= period.end_date:
        d_count += 1
        if current_d.weekday() == 4:
            weeks.append(d_count)
            d_count = 0
        current_d = current_d + timedelta(1)
    days = []
    current_d = period.start_date + timedelta(0)
    while current_d <= period.end_date:
        weekday = True
        if 5 <= current_d.weekday() <= 6:
            weekday = False
        days.append((current_d.day, weekday))
        current_d = current_d + timedelta(1)
    context = {
        'period' : period,
        'person' : person,
        'courses' : courses_exercises,
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

def get_next_exercise_number(exercises):
    nextNumber = exercises.aggregate(Max('number'))['number__max']
    nextNumber = 1 if nextNumber is None else nextNumber + 1 
    return nextNumber   

def course(request, letter_yr, code):
    course = get_object_or_404(Courses, courses_classes__letter_yr=letter_yr, pk=str(code))
    terms = get_list_or_404(Term, courses_term__code=str(code))
    terms.sort(key=lambda x: x.term)
    login = "test01"
    teacher = People.objects.get(login=login).student_letter_yr == None
    exercises = Exercises.objects.filter(code=str(code))
    next_number = get_next_exercise_number(exercises)
    #exercises.sort(key=lambda x: x.number)
    context = {
        'course' : course,
        'letter_yr' : letter_yr,
        'terms' : terms,
        'teacher' : teacher,
        'exercises' : exercises,
        'next_number' : next_number,
    }
    return render(request, 'kateapp/course.html', context)

def exercise_setup(request, letter_yr, code, number):
    newNumber = get_next_exercise_number(Exercises.objects.filter(code=code))
    if int(number) > newNumber:
        raise Http404("Exercise doesn't exists1")
    if request.method == 'POST':
        form = NewExerciseForm(request.POST)
        if form.is_valid():
            if Exercises.objects.filter(code=code, number = number).exists():
                Exercises.objects.filter(code=code, number = number).update(
                    title=form.cleaned_data["exercise"], 
                    start_date=form.cleaned_data["start_date"], 
                    deadline=form.cleaned_data["end_date"], 
                    exercise_type=form.cleaned_data["exercise_type"],
                    assessment=form.cleaned_data["assessment"],
                    submission=form.cleaned_data["submission"],
                    )
            else:
                e = Exercises(
                    code=Courses.objects.get(code=code),
                    number=newNumber,
                    title=form.cleaned_data["exercise"], 
                    start_date=form.cleaned_data["start_date"], 
                    deadline=form.cleaned_data["end_date"], 
                    exercise_type=form.cleaned_data["exercise_type"],
                    assessment=form.cleaned_data["assessment"],
                    submission=form.cleaned_data["submission"],
                )
                e.save()
            return HttpResponseRedirect('/course/2016/' + letter_yr + '/' + code + '/')
    else:
        if (int(number) == newNumber):
            form = NewExerciseForm()
        else:
            if Exercises.objects.filter(code=code, number = number).exists():
                exercise = Exercises.objects.get(code=code, number = number)
                data = {
                    'exercise' : exercise.title,
                    'start_date' : exercise.start_date,
                    'end_date' : exercise.deadline,
                    'exercise_type' : exercise.exercise_type,
                    'assessment' : exercise.assessment,
                    'submission' : exercise.submission,
                    }
                form = NewExerciseForm(data)
            else:
                raise Http404("Exercise doesn't exists2")
        context = {
            'form': form,
            'letter_yr' : letter_yr,
            'code' : code,
            'number' : number,
            }
        return render(request, 'kateapp/exercise_setup.html', context)
