
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .forms import StatusUpdateForm, UploadFileForm, CertificationUpdateForm, ScheduleCertificationForm
from .models import CertificationStatus, Certification
from django.contrib.auth.models import User
import pandas as pd
from django.core.cache import cache
# API imports
from django.http import HttpResponse
from django.core import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import CertificationStatusSerializer, CertificationSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

@login_required
def home(request):
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
        'formswithcert': formswithcert,
    }
    return render(request, 'training/home.html', context)

@login_required
def all_trainings(request):
    certificates = Certification.objects.all().order_by('name')
    # create an array with each certificates and the name and status of each person

    sidepanel = {
        'title': 'Training',
        'text1': 'Completed all trainings',
        'text2': 'Almost there',
    }
    
    context = {
        'title': 'Home',
        'sidepanel': sidepanel,
        'certificates': certificates
    }
    return render(request, 'training/all_trainings.html', context)

def prepare_data():
    # Fetch profiles and certificates
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
    
    return profiles, certificates, data

def get_prepared_data():
    # Retrieve prepared data from cache
    prepared_data = cache.get('prepared_data')
    if prepared_data is None:
        # If data is not in cache, prepare it and save to cache
        profiles, certificates, data = prepare_data()
        prepared_data = {
            'profiles': profiles,
            'certificates': certificates,
            'data': data
        }
        cache.set('prepared_data', prepared_data, timeout=None)  # Set cache indefinitely or with appropriate timeout
    return prepared_data

def dashboard(request):
    # Your view function
    prepared_data = get_prepared_data()
    profiles = prepared_data['profiles']
    certificates = prepared_data['certificates']
    data = prepared_data['data']
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

def schedule(request, certification_id):
    certification = Certification.objects.get(pk=certification_id)
    form = ScheduleCertificationForm(instance=certification)
    if request.method == 'POST':
        form = ScheduleCertificationForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            messages.success(request, f'{certification.name} certificate has been scheduled!')
            return redirect('training-schedule', certification_id=certification_id)
        else:
            messages.error(request, 'Form is not valid. Please check the entered data.')
    
    sidepanel = {
        'title': 'Training',
        'text1': 'Completed all trainings',
        'text2': 'Almost there',
    }

    context = {
        'title': 'Schedule',
        'sidepanel': sidepanel,
        'certification': certification,
        'form': form,

    }
    return render(request, 'training/schedule.html', context)

def send_reminder_email(request, certification_id):
    certification = Certification.objects.get(pk=certification_id)
    certStatuses = certification.get_incomplete_certification_statuses()
    for certStatus in certStatuses:
        certStatus.send_schedule_notification()
        certStatus.save()
    messages.success(request, f'Reminder emails have been sent for {certification.name} certificate!')



    return redirect('training-all_trainings')
    


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
                    # if completion_date is "R" make it empty and the status "To be Scheduled"
                    if completion_date == "R":
                        completion_date = None
                    
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
                                'completed_date': completion_date
                            }
                        )

                        if not created:
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

# API routes



class Certifications(APIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        return Certification.objects.all().order_by('name')

    def get(self, request):
        certificates = self.get_queryset()
        serializer = CertificationSerializer(certificates, many=True)
        return Response(serializer.data)

class StatusCertifications(APIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        return CertificationStatus.objects.all()

    def get(self, request):
        certificates = self.get_queryset()
        serializer = CertificationStatusSerializer(certificates, many=True)
        return Response(serializer.data)

