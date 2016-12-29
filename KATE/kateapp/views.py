import logging
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.db.models import Max
from django.utils import timezone



from .models import Classes, People, Courses, Term, Courses_Term, Courses_Classes, Exercises, Period, Resource, Exercises_Resource, Courses_Resource
from .forms import NewExerciseForm, SubmissionForm

import datetime
import calendar
from datetime import timedelta
from datetime import datetime

from operator import attrgetter, itemgetter

logger = logging.getLogger('django')


def index(request):
    return render(request, 'kateapp/home.html')


def grading_scheme(request):
    return render(request, 'kateapp/grading_scheme.html')


def personal_page(request):
    login = "yw8012"
    person = get_object_or_404(People, login=login)
    #courses = list(Courses.objects.filter(required=person)) + list(Courses.objects.filter(registered=person))
    courses = list(Courses.objects.all())
    courses_exercises = []
    date_now = timezone.now()
    for course in courses:
        courses_exercises = courses_exercises + list(Exercises.objects.filter(
            code=course.code, start_date__lte=date_now, deadline__gte=date_now))
    courses_exercises.sort(key=itemgetter('deadline'))
    for exercise in courses_exercises:
        if((exercise.deadline - date_now).days > 0):
            courses_exercises.append((exercise, (exercise.deadline - date_now).days, True))
        else:
            courses_exercises.append((exercise, (exercise.deadline - date_now).seconds / 3600, False))
    context = {
        'person': person,
        'courses_exercises' : courses_exercises,
    }
    return render(request, 'kateapp/personal_page.html', context)

def individual_record(request, login):
    person = get_object_or_404(People, login=login)
    courses_marks = []
    for course in person.registered_courses.all():
        marks = list(Marks.objects.filter(login=login, exercise__code=course.code).order_by('exercise__number'))
        textual_marks = [convert_mark_number_text(elem) for elem in marks]
        courses_marks.append((course, textual_marks))
    context = {
        'person': person,
        'courses_marks': courses_marks,
    }
    return render(request, 'kateapp/individual_record.html', context)
def convert_mark_number_text(mark):
    number_mark = mark.mark
    if number_mark < 30:
        mark.mark = 'F'
    elif number_mark < 40:
        mark.mark = 'E'
    elif number_mark < 50:
        mark.mark = 'D'
    elif number_mark < 60:
        mark.mark = 'C'
    elif number_mark < 70:
        mark.mark = 'B'
    elif number_mark < 80:
        mark.mark = 'A'
    elif number_mark < 90:
        mark.mark = 'A+'
    else:
        mark.mark = 'A*'
    return mark

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


def course_list(request, letter_yr):
    courses_term1 = get_list_or_404(
        Courses, courses_classes__letter_yr=letter_yr, courses_term__term=1)
    courses_term2 = get_list_or_404(
        Courses, courses_classes__letter_yr=letter_yr, courses_term__term=2)
    courses_term3 = get_list_or_404(
        Courses, courses_classes__letter_yr=letter_yr, courses_term__term=3)
    context = {
        'letter_yr': letter_yr,
        'courses_term1': courses_term1,
        'courses_term2': courses_term2,
        'courses_term3': courses_term3,
    }
    return render(request, 'kateapp/course_list.html', context)


def get_next_exercise_number(exercises):
    nextNumber = exercises.aggregate(Max('number'))['number__max']
    nextNumber = 1 if nextNumber is None else nextNumber + 1
    return nextNumber


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
    context = {
        'course': course,
        'terms': terms,
        'teacher': teacher,
        'exercises_resources': exercises_resources,
        'next_number': next_number,
        'NO': Exercises.NO,
    }
    return render(request, 'kateapp/course.html', context)


def exercise_setup(request, code, number):
    newNumber = get_next_exercise_number(Exercises.objects.filter(code=code))
    course = get_object_or_404(Courses, pk=str(code))
    if int(number) > newNumber:
        raise Http404("Exercise doesn't exist")
    if request.method == 'POST':
        ############ Form Submitted ############
        if request.POST.get('submit'):
            form = NewExerciseForm(request.POST, request.FILES)
            if form.is_valid():
                # get file names
                file_names = form.cleaned_data["file_name"]
                if (file_names == ""):
                    file_names = []
                else:
                    file_names = file_names.split('@')
                if Exercises.objects.filter(code=code, number=number).exists():
                    Exercises.objects.filter(code=code, number=number).update(
                    title=form.cleaned_data["title"],
                    start_date=datetime.datetime.combine(
                                    form.cleaned_data["start_date"],
                                    datetime.time(0,0)),
                    deadline=datetime.datetime.combine(
                                    form.cleaned_data["end_date"],
                                    form.cleaned_data["end_time"]),
                    exercise_type=form.cleaned_data["exercise_type"],
                    assessment=form.cleaned_data["assessment"],
                    submission=form.cleaned_data["submission"],
                    esubmission_files_names=file_names,
                    )
                else:
                    # setup exercise
                    e = Exercises(code=Courses.objects.get(code=code),
                              title=form.cleaned_data["title"],
                              start_date=datetime.datetime.combine(
                                              form.cleaned_data["start_date"],
                                              datetime.time(0,0)),
                              deadline=datetime.datetime.combine(
                                              form.cleaned_data["end_date"],
                                              form.cleaned_data["end_time"]),
                              number=newNumber,
                              exercise_type=form.cleaned_data["exercise_type"],
                              assessment=form.cleaned_data["assessment"],
                              submission=form.cleaned_data["submission"],
                              esubmission_files_names=file_names)
                    e.save()
                    # check if file given
                    if form.cleaned_data["file"]:
                        # setup resource
                        r = Resource(file=request.FILES["file"])
                        # save resource
                        r.save()
                        # setup exercise-resource link
                        er = Exercises_Resource(exercise=e, resource=r)
                        er.save()
                    if form.cleaned_data["resources"]:
                        # setup additional resources
                        for rFile in request.FILES.getlist("resources"):
                            r = Resource(file=rFile)
                            r.save()
                            er = Exercises_Resource(exercise=e,
                                                resource=r)
                            er.save()
                return HttpResponseRedirect('/course/2016/' + code + '/')
            else:
                raise Http404("Form Validation failed")
        elif (request.POST.get('delete')):
            #Delete button pressed
            Exercises.objects.get(code=code, number=number).delete()
            #TODO: What about resource deletion etc..????
            #raise Http404("ret " + res)
            return HttpResponseRedirect('/course/2016/' + code + '/')
    else:
        ############ Form generated ############
        file_names = [""]
        cancel = ""
        if (int(number) == newNumber):
            # Teacher is setting up a new exercise
            form = NewExerciseForm()
        else:
            #Request to edit an exercise
            if Exercises.objects.filter(code=code, number=number).exists():
                #Exercise exists, get it and populate form with data
                exercise = Exercises.objects.get(code=code, number=number)
                if Resource.objects.filter(exercises_resource__exercise__code=exercise.code, exercises_resource__exercise__number=exercise.number).exists():
                    resources = list(Resource.objects.filter(
                        exercises_resource__exercise__code=exercise.code, exercises_resource__exercise__number=exercise.number))
                    mainFile = resources.pop(0)
                else:
                    resources = None
                    mainFile = None
                data = {
                    'title': exercise.title,
                    'start_date': exercise.start_date.date(),
                    'end_date': exercise.deadline.date(),
                    'end_time': exercise.deadline.time(),
                    'exercise_type': exercise.exercise_type,
                    'assessment': exercise.assessment,
                    'submission': exercise.submission,
                    'file': mainFile,
                    'resources': resources,
                }
                form = NewExerciseForm(data)
                #File names are displayed through JS, hence not loaded
                #into form but passed to context
                file_names = exercise.esubmission_files_names
                if file_names == []:
                    file_names = [""]
                #Exercise exists, Delete not Discard
                cancel = "Delete"
            else:
                raise Http404("Exercise doesn't exist")
        context = {
            'form': form,
            'code': code,
            'number': number,
            'course': course,
            'types': Exercises,
            'num_files': len(file_names),
            'file_names': file_names,
            'cancel' : cancel,
        }
        return render(request, 'kateapp/exercise_setup.html', context)


def submission(request, code, number):
    # Check that exercise exists
    if not Exercises.objects.filter(code=code, number=number).exists():
        raise Http404("Exercise doesn't exist")
    exercise = Exercises.objects.get(code=code, number=number)
    # Split, either form is being produced, or submitted
    if request.method == 'POST':
        ############ Form Submitted ############
        form = SubmissionForm(request.POST)
        if form.is_valid():
            # check if submitted already
            if Exercises_Resource.objects.filter(exercise=exercise).exitsts():
                # update submission with new
                Resource.objects.filter(Exercises_Resource__exercise=exercise).update(
                    file=request.FILES["file"])
                r = Resource.objects.get(Exercises_Resource__exercise=exercise)
                Exercises_Resource.objects.filter(
                    exercise=exercise).update(resource=r)
            else:
                # create new submission
                # setup resource
                r = Resource(file=request.FILES["file"])
                r.save()
                # setup exercise-resource link
                er = Exercises_Resource(exercise=exercise,
                                        resource=r)
                er.save()
            return HttpResponseRedirect('/submission/2016/' + code + '/' + number + '/')
    else:
        ############ Form generated ############
        # check if submitted already
        if not Exercises_Resource.objects.filter(exercise=exercise).exists():
            # create new unbound form
            form = SubmissionForm()
        else:
            # create bound form
            data = {
            }
            form = SubmissionForm(data)
        context = {
            'form': form,
            'code': code,
            'number': number,
            'exercise': exercise,
        }
        return render(request, 'kateapp/submission.html', context)
