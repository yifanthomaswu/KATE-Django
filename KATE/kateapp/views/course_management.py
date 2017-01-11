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
        if request.POST.get('remove'):
            c = request.POST.get('remove_file')
            cr = get_object_or_404(Courses_Resource, pk = c)
            if cr.resource:
                #need to delete file and Resource
                cr.resource.file.delete(False)
                cr.resource.delete()
            cr.delete()
            return HttpResponseRedirect('/course/2016/' + course.code + '/manage/')  
        ###### Course Resource being added #####
        form = CourseManagementForm(request.POST, request.FILES)
        if form.is_valid():
            #create new Cource_Resource 
            course_resource_type = form.cleaned_data["course_resource_type"]
            if (course_resource_type == Courses_Resource.NOTE 
                or course_resource_type == Courses_Resource.PROBLEM):
                #we will be working with a file. Setup resource
                r = Resource(file=request.FILES["file"])
                # save resource
                r.save()

                #Do some path magic here #lol
                import os
                from django.conf import settings
                init_path = r.file.path
                new_name = '2016/CO' + course.code + '/Resources/' + r.file.name
                r.file.name = new_name
                new_path = settings.MEDIA_ROOT + '/' + new_name
                new_dir = os.path.dirname(new_path)
                try:
                    os.makedirs(new_dir)
                except OSError:
                    #this happens if directory already exists
                    pass
                    #raise Http404("failed " + new_dir)
                os.rename(init_path, new_path)
                r.save()

                #setup Course - Resource link
                courses_resource = Courses_Resource(code=course,
                                                    title=form.cleaned_data["title"],
                                                    resource=r,
                                                    release_date=form.cleaned_data["release_date"],
                                                    course_resource_type=course_resource_type,
                                                    )
                courses_resource.save()
            else:
                #we have a URL. Setup Course - Resource link
                courses_resource = Courses_Resource(code=course,
                                                    title=form.cleaned_data["title"],
                                                    link=form.cleaned_data["link"],
                                                    release_date=form.cleaned_data["release_date"],
                                                    course_resource_type=course_resource_type,
                                                    )
                courses_resource.save()
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
    piazza = list(Courses_Resource.objects.filter(code=code, course_resource_type='PIAZZA').order_by('release_date'))
    homepage = list(Courses_Resource.objects.filter(code=code, course_resource_type='HOMEPAGE').order_by('release_date'))
    resource = (note, exercise, url, panopto, piazza, homepage)

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