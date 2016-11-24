from django import forms
from .models import Exercises

class NewExerciseForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    file = forms.FileField(label='Document')
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker form-control'
                                }))
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker form-control'
                                }))
    exercise_type = forms.ChoiceField(choices=Exercises.TYPE_CHOICES)
    assessment = forms.ChoiceField(choices=Exercises.ASSESSMENT_CHOICES)
    submission = forms.ChoiceField(choices=Exercises.SUBMISSION_CHOICES)

class SubmissionForm(forms.Form):
    #Is it Electronic submission?
    file = forms.FileField(label='Document')
    # How many files to upload?
    #Add group members?
    #Generate smt else if not electronic?...
