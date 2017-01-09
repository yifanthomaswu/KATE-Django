from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
from urllib import urlopen
from collections import Counter

from django.utils import timezone

from datetime import datetime, date

from ..models import Exercises, People, Resource, Courses, Submissions
from ..forms import SubmissionForm

def getUser():
    user_login = "yw8012"
    return get_object_or_404(People, login=user_login)

def isStaff(user, exercises):
    return True

def pastDeadline(exercise):
    now = timezone.now()
    return now > exercise.deadline

def submission(request, code, number):
    exercise = get_object_or_404(Exercises,code=code, number=number)

    user = getUser()
    showMarking = isStaff(user, exercise)

    #Uncomment for testing purposes
    #showMarking = True

    course = get_object_or_404(Courses, pk=code)

    # Computes and puts together the resources that the template uses, ie the files associated with this exercise
    specification = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='SPEC').order_by('exercises_resource__resource__timestamp'))
    data = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='DATA').order_by('exercises_resource__resource__timestamp'))
    answer = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='ANSWER').order_by('exercises_resource__resource__timestamp'))
    if showMarking:
        marking = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='MARKING').order_by('exercises_resource__resource__timestamp'))
        resource = (specification, data, answer, marking)
    else:
        resource = (specification, data, answer)

    #We split here depending on what type of submission will be available
    if exercise.submission == Exercises.NO or pastDeadline(exercise):
        return displayPlainSubmissionPage(request, course, exercise, resource)

    elif exercise.submission == Exercises.HARDCOPY:
        return displayHardcopySubmissionPage(request, course, exercise, resource)

    else:
        return displayElectronicSubmissionPage(request, course, exercise, resource)

def displayPlainSubmissionPage(request, course, exercise, resource):
    #Dispay a plain submission page with some info only
    if pastDeadline(exercise):
        disabled = True
    else:
        disabled = False
    context = {
            'course': course,
            'exercise': exercise,
            'resource' : resource,
            'disabled' : disabled,
        }
    return render(request, 'kateapp/submission.html', context)

def displayHardcopySubmissionPage(request, course, exercise, resource):
    ####################################################################
    user = "yw8012"
    ####################################################################
    if request.method == 'POST':
        ############ Form Submitted ############
        form = SubmissionForm(request.POST)
        if form.is_valid():
            # create new submission
            leader = get_object_or_404(People, login=form.cleaned_data["leader"])
            new_sub = Submissions(exercise=exercise, leader=leader)
            new_sub.save()
            return HttpResponseRedirect('/submission/2016/' + course.code + '/' + str(exercise.number) + '/')
    else:
        ############ Form generated ############
        # check if submitted already
        if not Submissions.objects.filter(exercise=exercise, leader=People.objects.get(login=user)).exists():
            # create new unbound form
            form = SubmissionForm()
            bound = False
        else:
            # create bound form
            data = {
                'leader' : user
            }
            form = SubmissionForm(data)
            bound = True

        context = {
            'form': form,
            'course': course,
            'exercise': exercise,
            'bound' : bound,
            'resource' : resource,
        }
        return render(request, 'kateapp/submission.html', context)

def displayElectronicSubmissionPage(request, course, exercise, resource):
    ####################################################################
    user = "yw8012"
    ####################################################################
    if request.method == 'POST':
        ############ Form Submitted ############
        form = SubmissionForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        if form.is_valid():
            expected_file_names = exercise.esubmission_files_names
            given_file_names = [file.name for file in files]
            leader = get_object_or_404(People, login=form.cleaned_data["leader"])
            # check if submitted already
            # TODO: for groups checking will need to check if any submission where either login or user is memebr
            if Submissions.objects.filter(exercise=exercise, leader=People.objects.get(login=user)).exists():
                #Need to check if files uplaoded are in the expected name formats
                if not set(given_file_names).issubset(expected_file_names):
                    raise Http404(str(given_file_names) + " is not a subset of: " + str(expected_file_names))
                submission = get_object_or_404(Submissions, exercise=exercise, leader=People.objects.get(login=user))
                # Delte the files we are replacing
                # Add the replecement
                for file_name in given_file_names:
                    f = submission.files.filter(file__contains=file_name.split('.')[0]).get(file__contains=file_name.split('.')[1])
                    #Delete the actual file first
                    f.file.delete(False)
                    f.delete()
                for file in files:
                    r = Resource(file=file)
                    r.save()

                    #Do some path magic here #lol
                    import os
                    from django.conf import settings
                    init_path = r.file.path
                    new_name = '2016/CO' + course.code + '/Exercises/Ex' + str(exercise.number) + '/Submissions/' + leader.login + '/' + r.file.name
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
                    
                    # setup submission-resource link
                    submission.files.add(r)

            else:
                #check num/name of uploaded files matches required for exercise
                if not Counter(expected_file_names) == Counter(given_file_names):
                    #if they diff by num or name raise
                    raise Http404(str(given_file_names) + " did not match the required: " + str(expected_file_names))
                # create new submission
                new_sub = Submissions(exercise=exercise, leader=leader)
                new_sub.save()
                # setup resources
                for file in files:
                    r = Resource(file=file)
                    r.save()


                    #Do some path magic here #lol
                    import os
                    from django.conf import settings
                    init_path = r.file.path
                    new_name = '2016/CO' + course.code + '/Exercises/Ex' + str(exercise.number) + '/Submissions/' + leader.login + '/' + r.file.name
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


                    # setup submission-resource link
                    new_sub.files.add(r)
            return HttpResponseRedirect('/submission/2016/' + course.code + '/' + str(exercise.number) + '/')
        else:
            context = {
            'form': form,
            'course': course,
            'exercise': exercise,
            'bound' : True,
            'elec' : True,
            }
            raise Http404("inv")
            #return render(request, 'kateapp/submission.html', context)
    else:
        ############ Form generated ############
        # check if submitted already
        if not Submissions.objects.filter(exercise=exercise, leader=People.objects.get(login=user)).exists():
            # create new unbound form
            form = SubmissionForm()
            bound = False
            uploads = []
        else:
            # create bound form
            data = {
                'leader' : user
            }
            form = SubmissionForm(data)
            bound = True
            uploads = list(Submissions.objects.get(exercise=exercise, leader=People.objects.get(login=user)).files.all())
        context = {
            'form': form,
            'course': course,
            'exercise': exercise,
            'bound' : bound,
            'elec' : True,
            'uploads' : uploads,
            'resource' : resource,
        }
        return render(request, 'kateapp/submission.html', context)

#This method is what generates the Cover sheet for Hardcopy submission
def cover_sheet(request, code, number):
    ##################################################
    user = "yw8012"
    ##################################################

    person = get_object_or_404(People, login=user)
    course = get_object_or_404(Courses, code=code)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="submission.pdf"'
    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4 #keep for later

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    name = person.firstname + " " + person.lastname
    p.drawString(100, 685, "Name: " + name)
    p.drawString(100, 670, "Login: " + person.login)
    courseName = "CO" + course.code + ": " + course.title
    p.drawString(100, 655, "Course: " + courseName)
    p.drawString(100, 640, "Lecturer: " + course.lecturer.firstname + " " + course.lecturer.lastname)
    p.drawString(100, 625, "Excercise number: " + str(number))
    exercise = get_object_or_404(Exercises, code=course, number=number)
    submission = get_object_or_404(Submissions, exercise=exercise, leader=person)
    p.drawString(100, 610, "Submitted: " + submission.timestamp.strftime('%A, %d %B %Y %I:%M %p'))
    p.drawString(100, 40, "Page Generated: " + datetime.now().strftime('%A, %d %B %Y %I:%M %p'))

    p.setFont("Courier-BoldOblique", 25)
    p.drawString(width/2, 750, "KATe")
    p.setFont("Courier-BoldOblique", 13)
    p.drawString(100, 700, "Cover Sheet")

    #We draw the 2 border rectangles here
    a = 10
    p.rect(a, a, width-(2*a), height-(2*a))
    a = 15
    p.setLineWidth(2)
    p.rect(a, a, width-(2*a), height-(2*a))

    #Set the content of the QR message here
    QRmessage = courseName + "%0A" + name + "%0A" + person.login + "%0A" + submission.timestamp.strftime('%A, %d %B %Y %I:%M %p')
    #Set the size of the QR code on the cover sheet, in pixels
    size = 300 #in pixels

    #Use Google Charts to generate QR code
    baseURL = "https://chart.googleapis.com/chart?cht=qr&choe=ISO-8859-1&chld=H"
    dimensions = "&chs=" + str(size) + "x" + str(size)
    baseURL += dimensions
    baseURL += "&chl=" + QRmessage
    img = Image.open(urlopen(baseURL))
    #We draw the actaul QR code here, we can set the x and y, but width and height should be 'size'
    p.drawInlineImage(img, width/2-(size/2), 50, size, size)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
