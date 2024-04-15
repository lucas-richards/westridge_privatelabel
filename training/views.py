
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import Profile, Role
from .forms import (
    TrainingEventUpdateForm,
    UploadFileForm,
    TrainingModuleUpdateForm,
    ScheduleTrainingModuleForm,
    NewTrainingEvent
)
from users.forms import UserRegisterForm, ProfileUpdateForm
from users.forms import RoleForm
from .models import TrainingEvent, TrainingModule
from django.contrib.auth.models import User
import pandas as pd
from django.core.paginator import Paginator

@login_required
def home(request):
    profile_instance = Profile.objects.get(user=request.user)
    must_have = profile_instance.must_have_training_modules()
    # go over must have training modules and check if they have been completed and if it's not save as '-
    data = []
    
    for training_module in must_have:
        event = TrainingEvent.objects.filter(profile=profile_instance, training_module=training_module).first()
        print(training_module, event)
        row = {}
        row['training_module'] = training_module
        row['event'] = event
        data.append(row) 
    print(data)
    percentage = profile_instance.get_training_modules_percentage()
   
    
    sidepanel = {
        'title': 'Training',
        'text1': 'Completed all trainings',
        'text2': 'Almost there',
    }
    
    context = {
        'title': 'Home',
        'sidepanel': sidepanel,
        'data': data,
        'percentage': percentage
    }
    return render(request, 'training/home.html', context)

@login_required
def percentage(request):
    profiles = Profile.objects.all()
    data = []
    for profile in profiles:
        row = {
            'username': profile.user.username,
            'percentage': profile.get_training_modules_percentage()
        }
        data.append(row)
    # sort them by percentage
    data = sorted(data, key=lambda x: x['percentage'], reverse=True)

    return render(request, 'training/percentage.html', {'title':'Percentage','data': data})

@login_required
def supervisors(request):
    profiles = Profile.objects.all()
    data = []
    # go over the profiles and get the people they are supervising
    for profile in profiles:
        user = User.objects.get(username=profile.user.username)
        row = {
            'username': user,
            'supervised': user.supervisor_profiles.all()
        }
        data.append(row)
    
    return render(request, 'training/supervisors.html', {'title':'Supervisors','data': data})

@login_required
def modules(request):
    prepared_data = get_prepared_data('')
    profiles = prepared_data['profiles']
    training_modules = prepared_data['training_modules']
    data = prepared_data['data']

    context = {
        'title': 'Modules',
        'profiles': profiles,
        'data': data,
        'zip_data': zip(training_modules, range(len(training_modules))),
    }
    return render(request, 'training/modules.html', context)

@login_required
# def staff_roles(request):
#     profiles = Profile.objects.all()
#     sidepanel = {
#         'title': 'Training',
#         'text1': 'Completed all trainings',
#         'text2': 'Almost there',
#     }
#     context = {
#         'title': 'Staff Roles',
#         'profiles': profiles,
#         'sidepanel': sidepanel
#     }
#     return render(request, 'training/staff_roles.html', context)

# @login_required
# def roles(request):
#     roles = Role.objects.all()
#     sidepanel = {
#         'title': 'Training',
#         'text1': 'Completed all trainings',
#         'text2': 'Almost there',
#     }
#     context = {
#         'title': 'Roles',
#         'roles': roles,
#         'sidepanel': sidepanel
#     }
#     return render(request, 'training/roles.html', context)

@login_required
def new_entry(request):
    if request.method == 'POST':
        form = NewTrainingEvent(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Training event has been added!')
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
        'sidepanel': sidepanel,
        'upload_form': UploadFileForm()
    }

    return render(request, 'training/new_entry.html', context)

@login_required
def new_user(request):
    if request.method == 'POST':
        form_u = UserRegisterForm(request.POST)
        form_p = ProfileUpdateForm(request.POST)
        if form_u.is_valid() and form_p.is_valid():
            form_u.save()
            # update user profile with form_p data
            user = User.objects.get(username=form_u.cleaned_data['username'])
            form_p = ProfileUpdateForm(request.POST, instance=user.profile)
            form_p.save()
            messages.success(request, 'New user has been created!')
            return redirect('training-new_user')
        else:
            messages.error(request, 'Form is not valid. Please check the entered data.')
    
    sidepanel = {
        'title': 'Training',
        'text1': 'Completed all trainings',
        'text2': 'Almost there',
    }

    context = {
        'title': 'New User',
        'form_u': UserRegisterForm(),
        'form_p': ProfileUpdateForm(),
        'sidepanel': sidepanel
    }

    return render(request, 'training/new_user.html', context)

@login_required
def history(request):
    training_events = TrainingEvent.objects.all().order_by('-created_date')
    paginator = Paginator(training_events, 10)
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

def get_prepared_data(supervisor):
    # Fetch profiles and training_modules
    if supervisor:
        #  filter profile objects where supervisor = supervisor
        supervisor = User.objects.get(id=supervisor)
        profiles = Profile.objects.filter(supervisor=supervisor)
        print('Profiles:', profiles)
    else:
        profiles = Profile.objects.all()
    training_modules = TrainingModule.objects.all().order_by('name')

    # Prepare data to be sent to the template
    data = []
    for profile in profiles:
        print('Get prepared data for user:', profile.user.username)
        row = {
            'username': profile.user.username,
            'roles': profile.roles.all(),
            'training_events': [],
        }
        
        must_have = profile.must_have_training_modules()
        for training_module in training_modules:
            event = TrainingEvent.objects.filter(profile=profile, training_module=training_module).first()
            
            if event:
                event = event
            elif training_module not in must_have:
                event = '-'
            else:
                event = training_module.name

            row['training_events'].append(event)
        data.append(row)

        prepare_data = {
            'profiles': profiles,
            'training_modules': training_modules,
            'data': data
        }
    
    return prepare_data

@login_required
def dashboard(request):
    # Your view function
    supervisors = [user for user in User.objects.all() if user.supervisor_profiles.all().count() != 0]

    # if the request has a supervisor parameter, filter the profiles by the supervisor
    if 'supervisor' in request.GET:
        selected_supervisor = request.GET['supervisor']
    else:
        selected_supervisor = '59'

    prepared_data = get_prepared_data(selected_supervisor)
    profiles = prepared_data['profiles']
    training_modules = prepared_data['training_modules']
    data = prepared_data['data']
    
    # create a function that returns all the roles in a form format to display it 
    data2 = []

    for role in Role.objects.all():
        row = {
            'role': role,
            'training_modules': []
        }
        for training_module in training_modules:
            if training_module in role.training_modules.all():
                row['training_modules'].append(training_module)
            else:
                row['training_modules'].append('-')
        data2.append(row)

    context = {
        'title': 'Grid',
        'profiles': profiles,
        'training_modules': training_modules,
        'supervisors': supervisors,
        'selected_supervisor': int(selected_supervisor) if selected_supervisor else selected_supervisor,
        'data': data,
        'data2': data2
    }

    return render(request, 'training/dashboard.html', context)

@login_required
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

@login_required
def send_reminder_email(request, training_module_id):
    training_module = TrainingModule.objects.get(pk=training_module_id)
    certStatuses = training_module.get_incomplete_training_events()
    for certStatus in certStatuses:
        certStatus.send_schedule_notification()
        certStatus.save()
    messages.success(request, f'Reminder emails have been sent for {training_module.name} certificate!')



    return redirect('training-all_trainings')

@login_required
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
    return render(request, 'training/event_detail.html', context)

@login_required
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
    return render(request, 'training/module_detail.html', context)

@login_required
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
            return redirect('training-history')
        else:
            messages.error(request, 'Form is not valid. Please check your input.')
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})

# API routes

# class TrainingModules(APIView): 
#     permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

#     def get_queryset(self):
#         return TrainingModule.objects.all().order_by('name')

#     def get(self, request):
#         training_modules = self.get_queryset()
#         serializer = TrainingModuleSerializer(training_modules, many=True)
#         return Response(serializer.data)

# class TrainingEvents(APIView):
#     permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

#     def get_queryset(self):
#         return TrainingEvent.objects.all()

#     def get(self, request):
#         training_modules = self.get_queryset()
#         serializer = TrainingEventSerializer(training_modules, many=True)
#         return Response(serializer.data)

