from django.shortcuts import get_object_or_404, get_list_or_404, render

import calendar
from datetime import timedelta

from ..models import Period, People, Courses, Exercises

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
        courses = get_list_or_404(Courses.objects.order_by(
            'code'), courses_classes__letter_yr=letter_yr, courses_term__term=term_id)
    courses_exercises = []
    for course in courses:
        exercises = list(Exercises.objects.filter(
            code=course.code).order_by('start_date', 'deadline'))
        bins = []
        for exercise in exercises:
            exercise_start = exercise.start_date.date()
            exercise_end = exercise.deadline.date()
            if period.start_date <= exercise_start <= period.end_date or period.start_date <= exercise_end <= period.end_date or (exercise_start < period.start_date and exercise_end > period.end_date):
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
                last_end = item_end
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
    days = []
    current_d = period.start_date + timedelta(0)
    while current_d <= period.end_date:
        weekday = True
        if 5 <= current_d.weekday() <= 6:
            weekday = False
        days.append((current_d.day, weekday))
        current_d = current_d + timedelta(1)
    context = {
        'period': period,
        'person': person,
        'courses': courses_exercises,
        'months': months,
        'weeks': weeks,
        'days': days,
    }
    return render(request, 'kateapp/timetable.html', context)
