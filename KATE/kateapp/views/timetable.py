from django.shortcuts import get_object_or_404, get_list_or_404, render

import calendar
from datetime import timedelta, datetime
from django.utils import timezone

from ..models import Period, People, Courses, Exercises, Classes

def timetable(request, period_id, letter_yr, login):
    classes = list(Classes.objects.all())
    periods = list(Period.objects.all())
    date_now = timezone.now()
    period_now = get_object_or_404(Period, start_date__lte=date_now, end_date__gte=date_now)
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
        courses = get_list_or_404(Courses.objects.order_by(
            'code'), courses_classes__letter_yr=letter_yr, courses_term__term=term_id)
    days = []
    current_d = period.start_date + timedelta(0)
    while current_d <= period.end_date:
        weekday = True
        if 5 <= current_d.weekday() <= 6:
            weekday = False
        today = False
        if current_d == datetime.today().date():
            today = True
        days.append((current_d.day, weekday, today))
        current_d = current_d + timedelta(1)
    courses_exercises = []
    subscribed = []
    for d in days:
        subscribed.append([d[1], 0, 0])
    for course in courses:
        exercises = list(Exercises.objects.filter(
            code=course.code).order_by('start_date', 'deadline'))
        bins = []
        for exercise in exercises:
            exercise_start = exercise.start_date.date()
            exercise_end = exercise.deadline.date()
            if period.start_date <= exercise_start <= period.end_date or period.start_date <= exercise_end <= period.end_date or (exercise_start < period.start_date and exercise_end > period.end_date):
                if exercise.exercise_type == "T" or exercise.exercise_type == "WES":
                    subscribed[(exercise_end - period.start_date).days][2] += 1
                elif exercise.submission != "NO":
                    subscribed[(exercise_end - period.start_date).days][1] += 1
                placed = False
                if bins:
                    for bin in bins:
                        can_place = True
                        for item in bin:
                            if item.start_date.date() <= exercise_start <= item.deadline.date() or item.start_date.date() <= exercise_end <= item.deadline.date() or (exercise_start < item.start_date.date() and exercise_end > item.deadline.date()):
                                can_place = False
                                break
                        if can_place:
                            bin.append(exercise)
                            placed = True
                            break
                if not placed:
                    bin = [exercise]
                    bins.append(bin)
        rows = []
        for bin in bins:
            row = []
            last_end = period.start_date
            for item in bin:
                item_start = item.start_date.date()
                item_end = item.deadline.date()
                row.append((None, (item_start - last_end).days))
                row.append((item, (item_end - item_start).days + 1))
                last_end = item_end + timedelta(1)
            rows.append(row)
        if not rows:
            rows.append([])
        courses_exercises.append((course, rows))
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
    months.append(
        (calendar.month_name[period.end_date.month], period.end_date.day))
    weeks = []
    d_count = 0
    current_d = period.start_date + timedelta(0)
    while current_d <= period.end_date:
        d_count += 1
        if current_d.weekday() == 4:
            weeks.append(d_count)
            d_count = 0
        current_d = current_d + timedelta(1)
    context = {
        'period': period,
        'person': person,
        'courses': courses_exercises,
        'months': months,
        'weeks': weeks,
        'days': days,
        'classes': classes,
        'periods': periods,
        'period_id': period_id,
        'letter_yr': letter_yr,
        'period_now': period_now,
        'subscribed': subscribed,
    }
    return render(request, 'kateapp/timetable.html', context)
