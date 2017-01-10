from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.utils import timezone

from ..models import People, Courses, Exercises, Period

def personal_page(request):
    teacher = False
    login = "yw8012"
    person = get_object_or_404(People, login=login)
    if(teacher):
        context = display_teacher_personal_page(person, login)
    else:
        context = display_student_personal_page(person, login)
    return render(request, 'kateapp/personal_page.html', context)

def display_teacher_personal_page(person, login):
    login = "test01"
    current_term = 1 #TODO which term?
    courses = get_list_or_404(Courses, lecturer_id=login, courses_term__term=current_term)
    exercises = []
    date_now = timezone.now()
    period = get_object_or_404(Period, start_date__lte=date_now, end_date__gte=date_now)
    for course in courses:
        exercises = exercises + list(Exercises.objects.filter(
            code=course.code, deadline__lte=date_now, assessment__in=["GROUP", "INDIVIDUAL"], mark_release_date=None))
    exercises.sort(key=lambda x:x.deadline)
    courses_exercises = []
    for exercise in exercises:
        if((date_now - exercise.deadline).days > 0):
            courses_exercises.append((exercise, (date_now - exercise.deadline).days, True))
        else:
            courses_exercises.append((exercise, (date_now - exercise.deadline).seconds / 3600, False))
    context = {
        'teacher': True,
        'person': person,
        'courses': courses,
        'courses_exercises' : courses_exercises,
        'period' : period,
    }
    return context

def display_student_personal_page(person, login):
    #courses = list(Courses.objects.filter(required=person)) + list(Courses.objects.filter(registered=person))
    courses = list(Courses.objects.all())
    exercises = []
    date_now = timezone.now()
    period = get_object_or_404(Period, start_date__lte=date_now, end_date__gte=date_now)
    for course in courses:
        exercises = exercises + list(Exercises.objects.filter(
            code=course.code, start_date__lte=date_now, deadline__gte=date_now))
    exercises.sort(key=lambda x:x.deadline)
    courses_exercises = []
    for exercise in exercises:
        if((exercise.deadline - date_now).days > 0):
            courses_exercises.append((exercise, (exercise.deadline - date_now).days, True))
        else:
            courses_exercises.append((exercise, (exercise.deadline - date_now).seconds / 3600, False))
    context = {
        'teacher': False,
        'person': person,
        'courses_exercises' : courses_exercises,
        'period' : period,
    }
    return context
