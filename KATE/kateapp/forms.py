from django import forms

class NewExerciseForm(forms.Form):
    exercise = forms.CharField(label='Exercise Title', max_length=200)
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
    number = forms.IntegerField()