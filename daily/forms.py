from django import forms

class AreaForm(forms.Form):
    your_name = forms.CharField(label='Your Area', max_length=20)

class TaskForm(forms.Form):
    your_name = forms.CharField(label='Your Task', max_length=50)