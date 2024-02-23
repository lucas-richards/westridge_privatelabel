from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile
from .models import UserCertificationStatus, Certification

# class UserRegisterForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['username','email','password1','password2']

class StatusUpdateForm(forms.ModelForm):
    certification = forms.ModelChoiceField(queryset=Certification.objects.all(), widget=forms.Select(attrs={'readonly': 'readonly'}))
    scheduled_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    due_date = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = UserCertificationStatus
        fields = ['certification','completion_status', 'scheduled_date', 'due_date']


