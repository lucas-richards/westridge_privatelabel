from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .models import UserCertificationStatus
from .forms import StatusUpdateForm

@login_required
def home(request):
    profiles = Profile.objects.all()
    certificates = UserCertificationStatus.objects.filter(user_id=request.user.id)
    
    if request.method == 'POST':
        certificate_id = request.POST.get('certification')
        try:
            certificate_instance = UserCertificationStatus.objects.get(certification=certificate_id, user=request.user.id)
            
            # Create a form instance with the posted data
            form = StatusUpdateForm(request.POST, instance=certificate_instance)
            
            if form.is_valid():
                # Update certificate instance with form data
                form.save()
                messages.success(request, f'{certificate_instance} certificate has been updated!')
            else:
                messages.error(request, 'Form is not valid. Please check the entered data.')

        except UserCertificationStatus.DoesNotExist:
            messages.error(request, f'Certificate with ID {certificate_id} does not exist.')

        return redirect('training-home')

    # Create forms for each certificate using the StatusUpdateForm
    forms = [StatusUpdateForm(instance=certificate) for certificate in certificates]
    print(forms)

    context = {
        'title': 'Home',
        'certificates': certificates,
        'forms': forms,
        'profiles': profiles
    }
    return render(request, 'training/home.html', context)