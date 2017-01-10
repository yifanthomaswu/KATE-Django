from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from ..models import *

def course_management(request, code):
    course = get_object_or_404(Courses, pk=str(code))
    terms = get_list_or_404(Term, courses_term__code=str(code))
    terms.sort(key=lambda x: x.term)

    login = "test01"
    teacher = People.objects.get(login=login).student_letter_yr == None
    
    note = list(Courses_Resource.objects.filter(code=code, course_resource_type='NOTE').order_by('release_date'))
    exercise = list(Courses_Resource.objects.filter(code=code, course_resource_type='PROBLEM').order_by('release_date'))
    url = list(Courses_Resource.objects.filter(code=code, course_resource_type='URL').order_by('release_date'))
    panopto = list(Courses_Resource.objects.filter(code=code, course_resource_type='PANOPTO').order_by('release_date'))
    resource = (note, exercise, url, panopto)
    context = {
        'course': course,
        'terms': terms,
        'teacher': teacher,
        'resource': resource,
    }
    return render(request, 'kateapp/course_management.html', context)