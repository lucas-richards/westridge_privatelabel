
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
from users.forms import UserRegisterForm, ProfileUpdateForm, UserRegisterForm2
from users.forms import RoleForm
from .models import TrainingEvent, TrainingModule, ProfileTrainingEvents, RoleTrainingModules
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
    supervisors = User.objects.filter(supervisor_profiles__isnull=False).distinct()
    training_modules = TrainingModule.objects.all().order_by('name')
    data = []
    
    for sup in supervisors:
        print('Get supervisor:', sup.username)
        row = {
            'username': sup.first_name + ' ' + sup.last_name,
            'percentage':'',
            'total_modules': '',
            'modules':''
        }
        modules = {
            'completed': [],
            'expired': [],
            'missing': []
        }
        
        for i, training_module in enumerate(training_modules):
            print(i)
            profiles = sup.supervisor_profiles.all()
            profile_training_events = ProfileTrainingEvents.objects.filter(profile__in=profiles).values_list('row', flat=True)
            
            for profile_training_event in profile_training_events:
                profile_training_event = profile_training_event.split(',')[i]
                
                if profile_training_event == '-':
                    continue
                elif profile_training_event[0] == 'T':
                    modules['missing'].append(training_module)
                elif profile_training_event[0] == 'E':
                    modules['expired'].append(training_module)
                else:
                    modules['completed'].append(training_module)
        
        modules['completed'] = list(set(modules['completed']) - set(modules['expired']) - set(modules['missing']))
        modules['expired'] = list(set(modules['expired']))
        modules['missing'] = list(set(modules['missing']))
        
        # percentage of completed modules over total
        row['total_modules'] = len(modules['completed']) + len(modules['expired']) + len(modules['missing'])
        row['percentage'] = round(len(modules['completed']) / row['total_modules'] * 100)
        print('##########', row)
        row['modules'] = modules
        data.append(row)
    
    return render(request, 'training/supervisors.html', {'title':'Supervisors','data': data})

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
    users = sorted(User.objects.all(), key=lambda x: x.username)
    training_modules = sorted(TrainingModule.objects.all(), key=lambda x: x.name)
    if request.method == 'POST':
        user_ids = request.POST.getlist('user1')
        module_ids = request.POST.getlist('training_module1')
        print('POST:', request.POST)
        for user in user_ids:
            for module in module_ids:
                # create a new training event
                try:
                    training_event = TrainingEvent.objects.create(
                        profile=Profile.objects.get(user=user),
                        training_module=TrainingModule.objects.get(pk=module),
                        completed_date=request.POST['completed_date']
                    )
                    training_event.save()
                    print('Training event created:', training_event)
                    messages.success(request, f'Training event {training_event} has been added!')
                    
                except:
                    print('Error creating training event')
                    messages.error(request, 'Error creating training event')
        return redirect('training-history')
        
    form = NewTrainingEvent()
    sidepanel = {
        'title': 'Training',
        'text1': 'Completed all trainings',
        'text2': 'Almost there',
    }

    context = {
        'title': 'New Entry',
        'users': users,
        'training_modules': training_modules,
        'form': form,
        'sidepanel': sidepanel,
        'upload_form': UploadFileForm()
    }

    return render(request, 'training/new_entry.html', context)

@login_required
def new_user(request):
    if request.method == 'POST':
        # the request will receive only first name, last name and email we need to create a username and password with it
        username = request.POST['first_name'] + '_' + request.POST['last_name']
        # replace all spaces with underscores and make it lowercase
        username = username.replace(' ', '_').lower()
        password = username
        print('username:', username, 'password:', password)
        form_r = UserRegisterForm(data={'username': username, 'password1': password, 'password2': password, 'first_name': request.POST['first_name'], 'last_name': request.POST['last_name'], 'email': request.POST['email']}) 
        form_p = ProfileUpdateForm(request.POST)
        if form_r.is_valid() and form_p.is_valid():
            form_r.save()
            # update user profile with form_p data
            user = User.objects.get(username=form_r.cleaned_data['username'])
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
        'form_u': UserRegisterForm2(),
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

@login_required
def training_profile(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    training_events = TrainingEvent.objects.filter(profile=profile).order_by('-completed_date')
    training_modules = profile.must_have_training_modules()
    print('Training modules:', training_modules)
    # zip training events with training modules
    data = []
    for training_module in training_modules:
        events = TrainingEvent.objects.filter(profile=profile, training_module=training_module).order_by('-completed_date')
        row = {}
        row['training_module'] = training_module
        row['events'] = events if events.exists() else 'missing'
        data.append(row)

    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request,f'Account has been updated!')
            return redirect('training-profile', profile_id=profile_id)
    else:
        p_form = ProfileUpdateForm( instance= profile)

    sidepanel = {
        'title': 'Modules History',
        'text1': 'Completed all trainings',
        'text2': '',
    }
    context = {
        'title': 'Profile',
        'profile': profile,
        'training_modules': training_modules,
        'training_events': training_events,
        'sidepanel': sidepanel,
        'p_form':p_form,
        'data': data
    }
    return render(request, 'users/profile.html', context)

@login_required
def dashboard(request):
    # get all the supervisors
    supervisors = User.objects.filter(supervisor_profiles__isnull=False).distinct()
    
    # if the request has a supervisor parameter, filter the profiles by the supervisor
    if 'supervisor' in request.GET:
        selected_supervisor = request.GET['supervisor']
    else:
        selected_supervisor = ''

    if selected_supervisor:
        #  filter profile objects where supervisor = supervisor
        profiles = Profile.objects.filter(supervisor=selected_supervisor)
        print('Profiles:', profiles)
    else:
        profiles = Profile.objects.all()
    training_modules = TrainingModule.objects.all().order_by('name')

    # Prepare data to be sent to the template
    data = []
    for profile in profiles.order_by('user__username'):
        # profile.update_training_events()
        print('Get prepared data for user:', profile.user.username)
        row = {
            'profile': profile,
            'roles': profile.roles.all(),
            'training_events': [],
        }
        profile_training_events = ProfileTrainingEvents.objects.get(profile=profile)
        # if a new user was added and the profile_training_events object was not created
        if profile_training_events.row == '':
            profile_training_events.update_row()
            profile_training_events = ProfileTrainingEvents.objects.get(profile=profile)
            
        row['training_events'] = profile_training_events.row.split(',')
        print('Row:', row)
        data.append(row)
        
    # create a function that returns all the roles in a form format to display it 
    data2 = []
    
    for obj in RoleTrainingModules.objects.all().order_by('role'):
        # role.update_training_modules_row()
        row = {
            'role': obj.role,
            'training_modules':obj.row.split(',')
        }
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
def training_confirm_delete(request, training_event_id):
    training_event = TrainingEvent.objects.get(pk=training_event_id)
    context = {
        'title': 'Delete',
        'training_event': training_event,
        'event': training_event,
    }
    return render(request, 'training/confirm_delete.html', context)

@login_required
def training_delete(request, training_event_id):
    training_event = TrainingEvent.objects.get(pk=training_event_id)
    training_event.delete()
    messages.success(request, f'{training_event} certificate has been deleted!')
    return redirect('training-history')

@login_required
def training_event_delete(request, training_event_id):
    # are you sure you want to delete this training event?
    training_event = TrainingEvent.objects.get(pk=training_event_id)
    training_event.delete()
    messages.success(request, f'{training_event.training_module} certificate has been deleted!')
    return redirect('training-history')

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
                employee_username = row['Employee'].replace(' ', '_').lower()  # Assuming 'Employee' is the column name in Excel
                
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

