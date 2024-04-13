from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Role
from training.models import TrainingModule

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']


class ProfileUpdateForm(forms.ModelForm):
    # birthday = forms.DateField(widget=forms.SelectDateWidget(years=range(1900,1999)))
    # roles as checkboxes
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),  # Replace 'Profile' with your actual model name
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Profile
        fields = ['supervisor','roles']

#  roles form with modules as checkboxes
class RoleForm(forms.ModelForm):
    training_modules = forms.ModelMultipleChoiceField(
        queryset=TrainingModule.objects.all(),  # Replace 'Profile' with your actual model name
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Role
        fields = ['training_modules']


