from django import forms
from .models import TrainingEvent, TrainingModule
from users.models import Profile


class TrainingEventUpdateForm(forms.ModelForm):
    completed_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = TrainingEvent
        fields = ['completed_date']

class UploadFileForm(forms.Form):
    file = forms.FileField()

#  training module update form
class TrainingModuleUpdateForm(forms.ModelForm):
    scheduled_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = TrainingModule
        fields = ['name', 'description', 'retrain_months', 'scheduled_date']

#  schedule training module form
class ScheduleTrainingModuleForm(forms.ModelForm):
    scheduled_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = TrainingModule
        fields = ['scheduled_date']

# new TrainingEvent
class NewTrainingEvent(forms.ModelForm):
    # choose a profile from dropdown
    profile = forms.ModelChoiceField(queryset=Profile.objects.all())
    # choose a training_module from dropdown
    training_module = forms.ModelChoiceField(queryset=TrainingModule.objects.all())
    # select a completed date
    completed_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = TrainingEvent
        fields = ['profile', 'training_module', 'completed_date']




    


