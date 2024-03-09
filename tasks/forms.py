from django import forms
from .models import Task

# create task form
class TaskCreateForm(forms.ModelForm):
    
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Task
        fields = ['assigned_to', 'title', 'description', 'due_date']

# updating task form
class TaskUpdateFormAssigned_to(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['status']

# updating task form
class TaskUpdateFormAuthor(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date']
