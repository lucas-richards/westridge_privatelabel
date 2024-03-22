
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .forms import StatusUpdateForm, UploadFileForm, CertificationUpdateForm
from .models import CertificationStatus, Profile, Certification
from django.contrib.auth.models import User
import pandas as pd

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
        'formswithcert': formswithcert,
    }
    return render(request, 'training/home.html', context)

def dashboard(request):
    profiles = Profile.objects.all()
    certificates = Certification.objects.all().order_by('name')
    
    # Prepare data to be sent to the template
    data = []
    for profile in profiles:
        row = {
            'username': profile.user.username,
            'roles': profile.get_roles(),
            'percentage': profile.get_certifications_percentage(),
            'certifications_status': []
        }
        for certification in certificates:
            status_obj = CertificationStatus.objects.filter(profile=profile, certification=certification).first()
            
            if status_obj:
                cert = status_obj
            
            elif profile.must_have_certification(certification):
                cert = '+'
            else:
                cert = '-'

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
        'data': data,
        'upload_form': UploadFileForm()
    }

    return render(request, 'training/dashboard.html', context)

def statusCertification_detail(request, certification_id):
    profiles = Profile.objects.all()
    certification = CertificationStatus.objects.get(pk=certification_id)
    form = StatusUpdateForm(instance=certification)
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            messages.success(request, f'{certification.certification} certificate has been updated!')
            return redirect('training-statusCertification-detail', certification_id=certification_id)
        else:
            messages.error(request, 'Form is not valid. Please check the entered data.')
    sidepanel = {
        'title': 'Training',
        'text1': 'Completed all trainings',
        'text2': 'Almost there',
    }

    context = {
        'title': certification.certification,
        'certification': certification,
        'profiles': profiles,
        'form': form,
        'sidepanel': sidepanel
    }
    return render(request, 'training/certification_status_detail.html', context)

def certification_detail(request, certification_id):
    profiles = Profile.objects.all()
    certification = Certification.objects.get(pk=certification_id)
    form = CertificationUpdateForm(instance=certification)
    if request.method == 'POST':
        form = CertificationUpdateForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            messages.success(request, f'{certification.name} certificate has been updated!')
            return redirect('training-certification-detail', certification_id=certification_id)
        else:
            messages.error(request, 'Form is not valid. Please check the entered data.')
    sidepanel = {
        'title': 'Training',
        'text1': 'Completed all trainings',
        'text2': 'Almost there',
    }

    context = {
        'title': certification.name,
        'certification': certification,
        'profiles': profiles,
        'form': form,
        'sidepanel': sidepanel
    }
    return render(request, 'training/certification_detail.html', context)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            
            # Rest of your code here
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file, sheet_name='FILL HERE_Performed Date')
            
            # save the values of the first five character of each header in a list
            certificates = df.columns[1:]
            
            #  save the values of the header in a list
            
            for index, row in df.iterrows():
                # Rest of your code here
                employee_username = row['Employee']  # Assuming 'Employee' is the column name in Excel
                
                print('Analyzing user:', employee_username)
                # Iterate through each certificate and its completion date
                for certificate in certificates:
                    certificate_name = certificate[0:5]  # Get the first 5 characters of the certificate name
                    completion_date = row[certificate]
                    # if completion_date is "R" make it empty and the status "Not Started"
                    if completion_date == "R":
                        completion_date = None
                        status = "Not Started"
                    else:
                        status = "Completed"
                    if pd.notna(completion_date) or completion_date == None:  # Check if completion_date is not NaN
                        try:
                            # Retrieve the profile object using the username
                            user = User.objects.get(username=employee_username)
                            profile = Profile.objects.get(user=user)
                            certification = Certification.objects.get(name=certificate_name)
                        except User.DoesNotExist:
                            print(f"User does not exist for {employee_username}")
                            continue  # Skip the iteration if the user doesn't exist
                        except (Profile.DoesNotExist, Certification.DoesNotExist):
                            print(f"Profile or Certification does not exist for {employee_username} or {certificate_name}")
                            continue  # Skip the iteration if the profile or certification doesn't exist

                        # Create CertificationStatus object
                        certification_status, created = CertificationStatus.objects.get_or_create(
                            profile=profile,
                            certification=certification,
                            defaults={
                                'status': status,
                                'completed_date': completion_date
                            }
                        )

                        if not created:
                            certification_status.status = status
                            certification_status.completed_date = completion_date
                            certification_status.save()
                        print(f'CertificationStatus object created for {profile} and {certification}')

                # return render dashoboard.html with successful message
            messages.success(request, f'File has been uploaded successfully!')
            return redirect('training-dashboard')
        else:
            messages.error(request, 'Form is not valid. Please check your input.')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})



