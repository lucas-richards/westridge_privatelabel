from django import forms
from .models import CertificationStatus


class StatusUpdateForm(forms.ModelForm):
    completed_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = CertificationStatus
        fields = ['status', 'completed_date']

class UploadFileForm(forms.Form):
    file = forms.FileField()


