from django import forms
from .models import Exercises, Exercises_Resource

DATE_FORMATS = ['%d/%m/%Y', '%d/%m/%y']
TIME_FORMATS = ['%I:%M %p', '%I:%M%p', '%H:%M']

class NewExerciseForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    resources = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': True}),
                                required=False)
    file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    file_type = forms.ChoiceField(choices=Exercises_Resource.TYPE_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker form-control'}, format=DATE_FORMATS[0]),
                                input_formats=DATE_FORMATS)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker form-control'}, format=DATE_FORMATS[0]),
                                input_formats=DATE_FORMATS)
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'class':'timepicker form-control'}, format=TIME_FORMATS[0]),
                                input_formats=TIME_FORMATS)
    exercise_type = forms.ChoiceField(choices=Exercises.TYPE_CHOICES, widget=forms.Select(attrs={'class':'form-control', 'onchange' : 'exercise()'}))
    assessment = forms.ChoiceField(choices=Exercises.ASSESSMENT_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    submission = forms.ChoiceField(choices=Exercises.SUBMISSION_CHOICES, widget=forms.Select(attrs={'class':'form-control', 'onchange' : 'electronic()'}))
    file_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'style' : 'display:none'}) )

class SubmissionForm(forms.Form):
    files = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class':'form-control','multiple': True}))
    leader = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}) )
    #What about a group??

class MarkingForm(forms.Form):
    marks = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
