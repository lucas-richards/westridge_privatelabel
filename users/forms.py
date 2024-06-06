from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Role
from training.models import TrainingModule


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

# new usewr form only with first name and last name
class UserRegisterForm2(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']



class ProfileUpdateForm(forms.ModelForm):
    # birthday = forms.DateField(widget=forms.SelectDateWidget(years=range(1900,1999)))
    # only show those users that are supervisors
    supervisor = forms.ModelChoiceField(queryset=User.objects.filter(profile__roles__name='SUP'), required=False)
    # roles as checkboxes
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),  # Replace 'Profile' with your actual model name
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Profile
        fields = ['active','supervisor','roles']

#  roles form with modules as checkboxes
class RoleForm(forms.ModelForm):
    training_modules = forms.ModelMultipleChoiceField(
        queryset=TrainingModule.objects.all().order_by('name'),  # Replace 'Profile' with your actual model name
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Role
        fields = ['training_modules']

class RoleUpdateForm(forms.ModelForm):
    training_modules = forms.ModelMultipleChoiceField(
        queryset=TrainingModule.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Role
        fields = ['name','description','training_modules']

# form to login with code, only enter username
# form to login with code, only enter username
class UserLoginCodeForm(forms.Form):
    username = forms.CharField()

# form to submit code password
class UserLoginCodeForm2(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = User
        fields = ['password']


