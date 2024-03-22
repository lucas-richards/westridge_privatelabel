from django import forms
from .models import CertificationStatus, Certification


class StatusUpdateForm(forms.ModelForm):
    completed_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CertificationStatus
        fields = ['status', 'completed_date']

class UploadFileForm(forms.Form):
    file = forms.FileField()

#  certification update form
class CertificationUpdateForm(forms.ModelForm):
    scheduled_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Certification
        fields = ['name', 'description', 'exp_months', 'scheduled_date', 'roles']


