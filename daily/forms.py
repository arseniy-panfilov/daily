from django import forms

class AreaForm(forms.Form):
    your_name = forms.CharField(
        label='', 
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'special'})
    )

class TaskForm(forms.Form):
    your_name = forms.CharField(
        label='', 
        max_length=50, 
        required=False
    )