from django import forms
from .models import Exercises, Exercises_Resource

class NewExerciseForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    resources = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}),
                                required=False)
    file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    file_type = forms.ChoiceField(choices=Exercises_Resource.TYPE_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker form-control'}, format='%m/%d/%Y'),
                                input_formats=['%m/%d/%Y','%m/%d/%y'])
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker form-control'}, format='%m/%d/%Y'),
                                input_formats=['%m/%d/%Y','%m/%d/%y'])
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class':'timepicker form-control'}, format='%H:%M'),
                                input_formats=['%H:%M'])
    exercise_type = forms.ChoiceField(choices=Exercises.TYPE_CHOICES, widget=forms.Select(attrs={'class':'form-control', 'onchange' : 'exercise()'}))
    assessment = forms.ChoiceField(choices=Exercises.ASSESSMENT_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    submission = forms.ChoiceField(choices=Exercises.SUBMISSION_CHOICES, widget=forms.Select(attrs={'class':'form-control', 'onchange' : 'electronic()'}))
    file_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'style' : 'display:none'}) )

class SubmissionForm(forms.Form):
    #Is it Electronic submission?
    file = forms.FileField(label='Document')
    # How many files to upload?
    #Add group members?
    #Generate smt else if not electronic?...
