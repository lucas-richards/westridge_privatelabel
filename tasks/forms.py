from django import forms
from .models import Task

# create task form
class TaskCreateForm(forms.ModelForm):
    
    due_date = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Task
        fields = ['assignee', 'title', 'description', 'due_date']

# updating task form
class TaskUpdateFormAssignee(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['status']

# updating task form
class TaskUpdateFormAuthor(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date']
