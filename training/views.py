from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .models import CertificationStatus, Certification
from .forms import StatusUpdateForm

@login_required
def home(request):
    profiles = Profile.objects.all()
    profile_instance = Profile.objects.get(user=request.user)
    certification_statuses = CertificationStatus.objects.filter(profile=profile_instance)
    if request.method == 'POST':
        certificate_id = request.POST.get('id')
        try:
            certificate_instance = CertificationStatus.objects.get(pk=certificate_id)
            
            # Create a form instance with the posted data
            form = StatusUpdateForm(request.POST, instance=certificate_instance)
            
            if form.is_valid():
                # Update certificate instance with form data
                # check which fields have been updated
                updated_fields = form.changed_data
                # pass the updated fields to the save method
                print('updated_fields', updated_fields)
                form.save()
                messages.success(request, f'{certificate_instance} certificate has been updated!')
            else:
                messages.error(request, 'Form is not valid. Please check the entered data.')

        except CertificationStatus.DoesNotExist:
            messages.error(request, f'Certificate with ID {certificate_id} does not exist.')

        return redirect('training-home')

    # Create forms for each certificate using the StatusUpdateForm
    forms = [StatusUpdateForm(instance=certificate) for certificate in certification_statuses]
    formswithcert = zip(certification_statuses, forms)
    
    sidepanel = {
        'title': 'Training',
        'text1': 'Completed all trainings',
        'text2': 'Almost there',
    }
    
    context = {
        'title': 'Home',
        'sidepanel': sidepanel,
        'certificates': certification_statuses,
        'forms': forms,
        'profiles': profiles,
        'formswithcert': formswithcert
    }
    return render(request, 'training/home.html', context)

def dashboard(request):
    profiles = Profile.objects.all()
    certificates = Certification.objects.all()
    
    # Prepare data to be sent to the template
    data = []
    for profile in profiles:
        row = {
            'username': profile.user.username,
            'certifications_status': []
        }
        for certification in certificates:
            status_obj = CertificationStatus.objects.filter(profile=profile, certification=certification).first()
            cert = status_obj if status_obj else '-'
            row['certifications_status'].append(cert)
        data.append(row)
    print('data', data)

    context = {'data': data}

    sidepanel = {
        'title': 'Training',
        'text1': 'Completed all trainings',
        'text2': 'Almost there',
    }

    context = {
        'title': 'Dashboard',
        'sidepanel': sidepanel,
        'profiles': profiles,
        'certificates': certificates,
        'data': data
    }

    return render(request, 'training/dashboard.html', context)