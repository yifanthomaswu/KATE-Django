from django import forms
from .models import Exercises

class NewExerciseForm(forms.Form):
    title = forms.CharField(label='Exercise Title', max_length=200)
    file = forms.FileField(label='Document')
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    number = forms.IntegerField()
    exercise_type = forms.ChoiceField(choices=Exercises.TYPE_CHOICES)
    assessment = forms.ChoiceField(choices=Exercises.ASSESSMENT_CHOICES)
    submission = forms.ChoiceField(choices=Exercises.SUBMISSION_CHOICES)
