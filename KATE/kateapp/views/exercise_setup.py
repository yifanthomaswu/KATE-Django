from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404

from datetime import datetime, time

from ..models import Exercises, Courses, Resource, Exercises_Resource
from ..forms import NewExerciseForm
from .helper import get_next_exercise_number

def exercise_setup(request, code, number):
    newNumber = get_next_exercise_number(Exercises.objects.filter(code=code))
    course = get_object_or_404(Courses, pk=str(code))
    if int(number) > newNumber:
        raise Http404("Exercise doesn't exist")
    if request.method == 'POST':
        ############ Form Submitted ############
        return process_exercise_setup_form(newNumber, course, request, code, number)
    else:
        ############ Form generated ############
        file_names = [""]
        cancel = ""
        resource=[]
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
                else:
                    resources = None
                data = {
                    'title': exercise.title,
                    'start_date': exercise.start_date.date(),
                    'end_date': exercise.deadline.date(),
                    'end_time': exercise.deadline.time(),
                    'exercise_type': exercise.exercise_type,
                    'assessment': exercise.assessment,
                    'submission': exercise.submission,
                    'resources': resources,
                }
                #File names are displayed through JS, hence not loaded
                #into form but passed to context
                form = NewExerciseForm(data)

                file_names = exercise.esubmission_files_names
                if file_names == []:
                    file_names = [""]

                #Exercise exists, Delete not Discard
                cancel = "Delete"
                specification = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='SPEC').order_by('exercises_resource__resource__timestamp'))
                data = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='DATA').order_by('exercises_resource__resource__timestamp'))
                answer = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='ANSWER').order_by('exercises_resource__resource__timestamp'))
                marking = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='MARKING').order_by('exercises_resource__resource__timestamp'))
                resource = (specification, data, answer, marking)
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
            'resource' : resource,
        }
        return render(request, 'kateapp/exercise_setup.html', context)

def process_exercise_setup_form(newNumber, course, request, code, number):
    if request.POST.get('submit'):
        # Submit button pressed
        return process_exercise_setup_submission(newNumber, course, request, code, number)
    elif (request.POST.get('delete')):
        # Delete button pressed
        return process_exercise_setup_deletion(code, number)
    elif (request.POST.get('upload')):
        # File upload button pressed
        return process_exercise_setup_file_upload(newNumber, course, request, code, number)
    elif (request.POST.get('remove')):
        # File remove button pressed
        return process_exercise_setup_file_remove(newNumber, course, request, code, number)

def process_exercise_setup_submission(newNumber, course, request, code, number):
    form = NewExerciseForm(request.POST)
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
            start_date=datetime.combine(
                            form.cleaned_data["start_date"],
                            time()),
            deadline=datetime.combine(
                            form.cleaned_data["end_date"],
                            form.cleaned_data["end_time"]),
            exercise_type=form.cleaned_data["exercise_type"],
            assessment=form.cleaned_data["assessment"],
            submission=form.cleaned_data["submission"],
            esubmission_files_names=file_names,
            )
        else:
            # setup exercise
            e = Exercises(code=course,
                      title=form.cleaned_data["title"],
                      start_date=datetime.combine(
                                      form.cleaned_data["start_date"],
                                      time()),
                      deadline=datetime.combine(
                                      form.cleaned_data["end_date"],
                                      form.cleaned_data["end_time"]),
                      number=newNumber,
                      exercise_type=form.cleaned_data["exercise_type"],
                      assessment=form.cleaned_data["assessment"],
                      submission=form.cleaned_data["submission"],
                      esubmission_files_names=file_names)
            e.save()
        return HttpResponseRedirect('/course/2016/' + code + '/')
    else:
        raise Http404("Form Validation failed")

def process_exercise_setup_deletion(code, number):
    exercise = Exercises.objects.get(code=code, number=number)
    Resource.objects.filter(exercises_resource__exercise=exercise).delete()
    exercise.delete()

    #Exercises.objects.get(code=code, number=number).delete()

    #re = Resource.objects.get(pk=r)
    #Exercises_Resource.objects.get(resource=re).delete()
    #re.delete()
    return HttpResponseRedirect('/course/2016/' + code + '/')

def process_exercise_setup_file_upload(newNumber, course, request, code, number):
    # check if file given
    form = NewExerciseForm(request.POST, request.FILES)
    if form.is_valid():
        if form.cleaned_data["file"]:
            # setup resource
            r = Resource(file=request.FILES["file"])
            # save resource
            r.save()

            #Do some path magic here #lol
            import os
            from django.conf import settings
            init_path = r.file.path
            new_name = '2016/CO' + course.code + '/Exercises/Ex' + str(number) + '/Resources/' + r.file.name
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

            #Check if this is upload for a brand new exercsie
            if not Exercises.objects.filter(code=code, number=number).exists():
                #create new exercise here
                e = Exercises(code=course,
                       title=form.cleaned_data["title"],
                       start_date=form.cleaned_data["start_date"],
                       deadline=form.cleaned_data["end_date"],
                       number=newNumber,
                       exercise_type=form.cleaned_data["exercise_type"],
                       assessment=form.cleaned_data["assessment"],
                       submission=form.cleaned_data["submission"],
                       )
                e.save()


            # setup exercise-resource link
            exercise = Exercises.objects.get(code=code, number=number)
            er = Exercises_Resource(exercise=exercise, resource=r, exercise_resource_type=form.cleaned_data["file_type"])
            er.save()

            file_names = exercise.esubmission_files_names
            if file_names == []:
                file_names = [""]
            cancel = "Delete"
            specification = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='SPEC').order_by('exercises_resource__resource__timestamp'))
            data = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='DATA').order_by('exercises_resource__resource__timestamp'))
            answer = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='ANSWER').order_by('exercises_resource__resource__timestamp'))
            marking = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='MARKING').order_by('exercises_resource__resource__timestamp'))
            resource = (specification, data, answer, marking)
            context = {
                'form': form,
                'code': code,
                'number': number,
                'course': course,
                'types': Exercises,
                'num_files': len(file_names),
                'file_names': file_names,
                'cancel' : cancel,
                'resource' : resource,
            }
            return render(request, 'kateapp/exercise_setup.html', context)
    else:
        raise Http404("Form Validation failed")

def process_exercise_setup_file_remove(newNumber, course, request, code, number):
    form = NewExerciseForm(request.POST, request.FILES)
    if request.POST.get('remove_file'):
        r = request.POST.get('remove_file')

        re = get_object_or_404(Resource, pk=r)
        re.file.delete(False)
        re.delete()

        #No need to delete Exercises_Resource as its Resource file field is on CASCADE

        exercise = Exercises.objects.get(code=code, number=number)
        file_names = exercise.esubmission_files_names
        if file_names == []:
            file_names = [""]
        cancel = "Delete"
        specification = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='SPEC').order_by('exercises_resource__resource__timestamp'))
        data = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='DATA').order_by('exercises_resource__resource__timestamp'))
        answer = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='ANSWER').order_by('exercises_resource__resource__timestamp'))
        marking = list(Resource.objects.filter(exercises_resource__exercise__code=code, exercises_resource__exercise__number=number, exercises_resource__exercise_resource_type='MARKING').order_by('exercises_resource__resource__timestamp'))
        resource = (specification, data, answer, marking)
        context = {
            'form': form,
            'code': code,
            'number': number,
            'course': course,
            'types': Exercises,
            'num_files': len(file_names),
            'file_names': file_names,
            'cancel' : cancel,
            'resource' : resource,
        }
        return render(request, 'kateapp/exercise_setup.html', context)
