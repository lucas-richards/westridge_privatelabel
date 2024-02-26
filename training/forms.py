from django import forms
from .models import CertificationStatus


class StatusUpdateForm(forms.ModelForm):
    scheduled_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    due_date = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = CertificationStatus
        fields = ['status', 'scheduled_date', 'due_date']


