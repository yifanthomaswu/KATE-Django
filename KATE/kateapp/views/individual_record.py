from django.shortcuts import get_object_or_404, render

from ..models import People, Marks

def individual_record(request, login):
    person = get_object_or_404(People, login=login)
    courses_marks = []
    for course in person.registered_courses.all():
        marks = list(Marks.objects.filter(login=login, exercise__code=course.code, released=True).order_by('exercise__number'))
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
