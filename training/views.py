
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .forms import TrainingEventUpdateForm, UploadFileForm, TrainingModuleUpdateForm, ScheduleTrainingModuleForm, NewTrainingEvent
from .models import TrainingEvent, TrainingModule
from django.contrib.auth.models import User
import pandas as pd
import datetime
# API imports
from rest_framework.response import Response
from .serializers import TrainingEventSerializer, TrainingModuleSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django.core.paginator import Paginator

@login_required
def home(request):
    profile_instance = Profile.objects.get(user=request.user)
    
    # training_events = TrainingEvent.objects.filter(profile=profile_instance)
    #  get all traininEvents for all users
    training_events = TrainingEvent.objects.all()
    

    
    sidepanel = {
        'title': 'Training',
        'text1': 'Completed all trainings',
        'text2': 'Almost there',
    }
    
    context = {
        'title': 'Home',
        'sidepanel': sidepanel,
        'training_events': training_events,
    }
    return render(request, 'training/home.html', context)

@login_required
def all_trainings(request):
    training_modules = TrainingModule.objects.all().order_by('name')
    # create an array with each training_modules and the name and status of each person

    sidepanel = {
        'title': 'Training',
        'text1': 'Completed all trainings',
        'text2': 'Almost there',
    }
    
    context = {
        'title': 'Home',
        'sidepanel': sidepanel,
        'training_modules': training_modules
    }
    return render(request, 'training/all_trainings.html', context)

@login_required
def new_entry(request):
    if request.method == 'POST':
        form = NewTrainingEvent(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Certificate has been added!')
            return redirect('training-history')
        else:
            messages.error(request, 'Form is not valid. Please check the entered data.')
    else:
        form = NewTrainingEvent()
    sidepanel = {
        'title': 'Training',
        'text1': 'Completed all trainings',
        'text2': 'Almost there',
    }

    context = {
        'title': 'New Entry',
        'form': form,
        'sidepanel': sidepanel
    }

    return render(request, 'training/new_entry.html', context)

def history(request):
    training_events = TrainingEvent.objects.all().order_by('-created_date')
    paginator = Paginator(training_events, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    sidepanel = {
        'title': 'Training',
        'text1': 'Completed all trainings',
        'text2': 'Almost there',
    }
    context = {
        'title': 'History',
        'training_events': page_obj,
        'sidepanel': sidepanel,
    }
    return render(request, 'training/history.html', context)

def get_prepared_data():
    # Fetch profiles and training_modules
    profiles = Profile.objects.all()
    training_modules = TrainingModule.objects.all().order_by('name')

    # Prepare data to be sent to the template
    data = []
    for profile in profiles:
        row = {
            'username': profile.user.username,
            'roles': profile.get_roles(),
            'percentage': profile.get_training_modules_percentage(),
            'training_events': []
        }
        for training_module in training_modules:
            event = TrainingEvent.objects.filter(profile=profile, training_module=training_module).first()
            
            if event:
                cert = event
            elif profile.must_have_training_module(training_module):
                cert = '+'
            else:
                cert = '-'

            row['training_events'].append(cert)
        data.append(row)

        prepare_data = {
            'profiles': profiles,
            'training_modules': training_modules,
            'data': data
        }
    
    return prepare_data

def dashboard(request):
    # Your view function
    prepared_data = get_prepared_data()
    profiles = prepared_data['profiles']
    training_modules = prepared_data['training_modules']
    data = prepared_data['data']
    paginator = Paginator(data, 5)  # Change the number 10 to the desired number of items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Dashboard',
        'profiles': profiles,
        'training_modules': training_modules,
        'data': page_obj,
        'upload_form': UploadFileForm()
    }

    return render(request, 'training/dashboard.html', context)

def schedule(request, training_module_id):
    training_module = TrainingModule.objects.get(pk=training_module_id)
    form = ScheduleTrainingModuleForm(instance=training_module)
    if request.method == 'POST':
        form = ScheduleTrainingModuleForm(request.POST, instance=training_module)
        if form.is_valid():
            form.save()
            messages.success(request, f'{training_module.name} certificate has been scheduled!')
            return redirect('training-schedule', training_module_id=training_module_id)
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
        'training_module': training_module,
        'form': form,

    }
    return render(request, 'training/schedule.html', context)

def send_reminder_email(request, training_module_id):
    training_module = TrainingModule.objects.get(pk=training_module_id)
    certStatuses = training_module.get_incomplete_training_events()
    for certStatus in certStatuses:
        certStatus.send_schedule_notification()
        certStatus.save()
    messages.success(request, f'Reminder emails have been sent for {training_module.name} certificate!')



    return redirect('training-all_trainings')

def training_event_detail(request, training_event_id):
    profiles = Profile.objects.all()
    training_event = TrainingEvent.objects.get(pk=training_event_id)
    form = TrainingEventUpdateForm(instance=training_event)
    if request.method == 'POST':
        form = TrainingEventUpdateForm(request.POST, instance=training_event)
        if form.is_valid():
            form.save()
            messages.success(request, f'{training_event.training_module} certificate has been updated!')
            return redirect('training-event-detail', training_event_id=training_event_id)
        else:
            messages.error(request, 'Form is not valid. Please check the entered data.')
    sidepanel = {
        'title': 'Training',
        'text1': 'Completed all trainings',
        'text2': 'Almost there',
    }

    context = {
        'title': training_event.training_module,
        'training_event': training_event,
        'profiles': profiles,
        'form': form,
        'sidepanel': sidepanel
    }
    return render(request, 'training/training_event_detail.html', context)

def training_module_detail(request, training_module_id):
    profiles = Profile.objects.all()
    training_module = TrainingModule.objects.get(pk=training_module_id)
    form = TrainingModuleUpdateForm(instance=training_module)
    if request.method == 'POST':
        form = TrainingModuleUpdateForm(request.POST, instance=training_module)
        if form.is_valid():
            form.save()
            messages.success(request, f'{training_module.name} certificate has been updated!')
            return redirect('training-module-detail', training_module_id=training_module_id)
        else:
            messages.error(request, 'Form is not valid. Please check the entered data.')
    sidepanel = {
        'title': 'Training',
        'text1': 'Completed all trainings',
        'text2': 'Almost there',
    }

    context = {
        'title': training_module.name,
        'training_module': training_module,
        'profiles': profiles,
        'form': form,
        'sidepanel': sidepanel
    }
    return render(request, 'training/training_module_detail.html', context)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            
            # Rest of your code here
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file, sheet_name='FILL HERE_Performed Date')
            
            # save the values of the first five character of each header in a list
            training_modules = df.columns[1:]
            
            #  save the values of the header in a list
            
            for index, row in df.iterrows():
                # Rest of your code here
                employee_username = row['Employee']  # Assuming 'Employee' is the column name in Excel
                
                print('Analyzing user:', employee_username)
                # Iterate through each certificate and its completion date
                for certificate in training_modules:
                    certificate_name = certificate[0:5]  # Get the first 5 characters of the certificate name
                    completion_date = row[certificate]
                    
                    if pd.notna(completion_date) and completion_date != 'R':
                        try:
                            # Retrieve the profile object using the username
                            user = User.objects.get(username=employee_username)
                            profile = Profile.objects.get(user=user)
                            training_module = TrainingModule.objects.get(name=certificate_name)

                            # Create TrainingEvent object
                            if not TrainingEvent.objects.filter(profile=profile, training_module=training_module, completed_date=completion_date).exists():
                                TrainingEvent.objects.create(
                                    profile=profile,
                                    training_module=training_module,
                                    completed_date=completion_date
                                )

                                print(f'TrainingEvent object created for {profile} and {training_module}')

                        except User.DoesNotExist:
                            print(f"User does not exist for {employee_username}")
                            continue  # Skip the iteration if the user doesn't exist
                        except (Profile.DoesNotExist, TrainingModule.DoesNotExist):
                            print(f"Profile or training_module does not exist for {employee_username} or {certificate_name}")
                            continue  # Skip the iteration if the profile or training_module doesn't exist
                    
                        
                # return render dashoboard.html with successful message
            messages.success(request, f'File has been uploaded successfully!')
            return redirect('training-dashboard')
        else:
            messages.error(request, 'Form is not valid. Please check your input.')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})

# API routes

class TrainingModules(APIView): 
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        return TrainingModule.objects.all().order_by('name')

    def get(self, request):
        training_modules = self.get_queryset()
        serializer = TrainingModuleSerializer(training_modules, many=True)
        return Response(serializer.data)

class TrainingEvents(APIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        return TrainingEvent.objects.all()

    def get(self, request):
        training_modules = self.get_queryset()
        serializer = TrainingEventSerializer(training_modules, many=True)
        return Response(serializer.data)

