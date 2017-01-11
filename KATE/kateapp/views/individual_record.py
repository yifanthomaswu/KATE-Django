from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from ..models import People, Marks, Submissions, Exercises

def individual_record(request, login):
    # get the logged in student
    person = get_object_or_404(People, login=login)
    # set up data structure to store data for html template
    courses_marks = []
    # traverse all registered courses for the student
    for course in person.registered_courses.all():
        # get the marks for the current course
        marks = list(Marks.objects.filter(login_id=login, exercise__code=course.code, exercise__mark_release_date__lte=timezone.now()).order_by('exercise__number'))
        # convert the mark numbers to text
        textual_marks = [(convert_mark_number_text(mark),
                         (Submissions.objects.get(leader_id=login, exercise_id=mark.exercise_id).timestamp >
                                    Exercises.objects.get(id=mark.exercise_id).deadline)) for mark in marks]
        # append the course with corresponding marks to the datastructure
        courses_marks.append((course, textual_marks))
    #set up the context for the html template
    context = {
        'person': person,
        'courses_marks': courses_marks,
    }
    return render(request, 'kateapp/individual_record.html', context)

def convert_mark_number_text(mark):
    # returns the textual mark for number marks
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
