from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.utils import timezone
from datetime import datetime, time

from ..models import Exercises, Courses, Submissions, Marks
from ..forms import MarkingForm

def marking(request, code, number):
    exercise = Exercises.objects.get(code=code, number=number)
    course = get_object_or_404(Courses, pk=code)
    submissions = Submissions.objects.filter(exercise_id=exercise.id).order_by('leader_id')
    #TODO get all subscribed students and group them if group submission
    # Split, either form is being produced, or submitted
    if request.method == 'POST':
        ############ Form submitted ############
        return process_marking_form(exercise, course, submissions, request, code, number)
    else:
        ############ Form generated ############
        return generate_marking_form(exercise, course, submissions, request, code, number)

def process_marking_form(exercise, course, submissions, request, code, number):
    form = MarkingForm(request.POST)
    if form.is_valid():
        marks_string = form.cleaned_data["marks"]
        if(marks_string != ""):
            marks = marks_string.split("@")
            for mark in marks:
                student_id = mark.split("_")[0]
                student_mark = mark.split("_")[1]
                # check if marked already
                if Marks.objects.filter(login_id=student_id, exercise_id=exercise.id).exists():
                    # check if mark changed
                    mark_object = Marks.objects.get(login_id=student_id, exercise_id=exercise.id)
                    if not mark_object.mark == student_mark:
                        Marks.objects.filter(login_id=student_id, exercise_id=exercise.id).update(mark=student_mark)
                else:
                    #setup mark
                    m = Marks(mark=student_mark,
                            exercise_id=exercise.id,
                            login_id=student_id)
                    m.save()
        all_marked = True
        for submission in submissions:
            if not Marks.objects.filter(login_id=submission.leader_id, exercise_id=exercise.id).exists():
                #TODO Check all marks? not only leader
                all_marked = False
                break
        if all_marked:
            Exercises.objects.filter(code=code, number=number).update(marked=True)
            #publish marks
            if request.POST.get('publish'):
                release_date = form.cleaned_data["release_date"]
                release_time = form.cleaned_data["release_time"]
                release_datetime = timezone.now()
                if release_time is None:
                    if release_date is not None:
                        release_datetime = datetime.combine(release_date,
                                                        timezone.now().time)
                else:
                    release_datetime = datetime.combine(release_date, release_time)
                Exercises.objects.filter(code=code, number=number).update(mark_release_date=release_datetime)
                return HttpResponseRedirect('/personal_page')

        return HttpResponseRedirect('/marking/2016/' + code + '/' + number + '/')
    else:
        return Http404("Form Validation failed")

def generate_marking_form(exercise, course, submissions, request, code, number):
    # check if submitted already
    if not Marks.objects.filter(exercise_id=exercise.id).exists():
        # create new unbound form
        form = MarkingForm()
    else:
        # create bound form
        marks_string = ""
        for submission in submissions:
            if Marks.objects.filter(login_id=submission.leader_id, exercise_id=exercise.id).exists():
                mark = Marks.objects.get(login_id=submission.leader_id, exercise_id=exercise.id)
                marks_string += mark.login_id + "_" + str(mark.mark) + "@"
        if marks_string != "":
            marks_string = marks_string[:-1]
        data = {
            'marks': marks_string,
        }
        form = MarkingForm(data)
    context = {
        'form': form,
        'course': course,
        'exercise': exercise,
        'submissions': submissions,
        'code': code,
        'number': number,
        'num_submissions': submissions.count(),
        'all_marked': exercise.marked
    }
    return render(request, 'kateapp/marking.html', context)
