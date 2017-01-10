from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from ..models import *
from ..forms import CourseManagementForm


def course_management(request, code):
    login = "test01"

    course = get_object_or_404(Courses, pk=str(code))

    validation_fail = False
    action= "cancel"

    if request.method == 'POST':
        ###### Course Resource being added #####
        form = CourseManagementForm(request.POST, request.FILES)
        if form.is_valid():
            #create new Cource_Resource 
            
            return HttpResponseRedirect('/course/2016/' + course.code + '/manage/')  
        #Form validation failed 
        validation_fail = True
        action= "refresh"
    else:
        form = CourseManagementForm()
    
    #Get nessecey items to display template
    terms = get_list_or_404(Term, courses_term__code=str(code))
    terms.sort(key=lambda x: x.term)

    teacher = People.objects.get(login=login).student_letter_yr == None
    
    note = list(Courses_Resource.objects.filter(code=code, course_resource_type='NOTE').order_by('release_date'))
    exercise = list(Courses_Resource.objects.filter(code=code, course_resource_type='PROBLEM').order_by('release_date'))
    url = list(Courses_Resource.objects.filter(code=code, course_resource_type='URL').order_by('release_date'))
    panopto = list(Courses_Resource.objects.filter(code=code, course_resource_type='PANOPTO').order_by('release_date'))
    resource = (note, exercise, url, panopto)

    types = Courses_Resource

    context = {
        'form' : form,
        'course': course,
        'terms': terms,
        'teacher': teacher,
        'resource': resource,
        'types' : types,
        'validation_fail' : validation_fail,
        'action': action,
    }
    return render(request, 'kateapp/course_management.html', context)