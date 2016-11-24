from django import forms
from .models import Exercises

class NewExerciseForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    file = forms.FileField(label='Document', widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker form-control'
                                }))
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker form-control'
                                }))
    #number = forms.IntegerField(widget=forms.NumberInput(attrs={'class' : 'form-control'}))
    exercise_type = forms.ChoiceField(choices=Exercises.TYPE_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    assessment = forms.ChoiceField(choices=Exercises.ASSESSMENT_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    submission = forms.ChoiceField(choices=Exercises.SUBMISSION_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))


class SubmissionForm(forms.Form):
    #Is it Electronic submission?
    file = forms.FileField(label='Document')
    # How many files to upload?
    #Add group members?
    #Generate smt else if not electronic?...
