from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserLoginCodeForm, UserLoginCodeForm2
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login
from django.contrib.auth import authenticate
from training.models import TrainingEvent, ProfileTrainingEvents


# Django templates
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f' {username} your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()

    
    return render(request, 'users/register.html',{'form':form})

# only when they are logged in, show form to update name user and image.

@login_required
def profile(request):
    # get user 
    user = request.user
    # get all profile training events
    training_events = TrainingEvent.objects.filter(profile=user.profile).order_by('-completed_date')
    # profile must have modules
    training_modules = user.profile.must_have_training_modules()

    data = []
    for training_module in training_modules:
        events = TrainingEvent.objects.filter(profile=user.profile, training_module=training_module).order_by('-completed_date')
        row = {}
        row['training_module'] = training_module
        row['events'] = events if events.exists() else 'missing'
        data.append(row)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm( request.POST,
                                    request.FILES,
                                    instance= request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated!')
            # update the profile training events
            profile_training_events = ProfileTrainingEvents.objects.filter(profile=user.profile).first()
            profile_training_events.update_row()
            print('prof_training_events',profile_training_events)
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm( instance= request.user.profile)

    sidepanel = {
            'title': 'Required Modules',
            'text1': 'Completed all trainings',
            'text2': '',
        }

    context = {
        'u_form':u_form,
        'p_form':p_form,
        'sidepanel': sidepanel,
        'training_events': training_events,
        'training_modules': training_modules,
        'data': data,

    }
    return render(request, 'users/profile.html', context)

def get_code(request):
    form = UserLoginCodeForm()
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.filter(username=username).first()
        if user:
            # if user has staff status
            if user.is_staff:
                if user.email:
                    verification_code = get_random_string(length=6, allowed_chars='0123456789')  # Generate a 6-digit verification code
                    user.set_password(verification_code)  # Set password to verification code
                    user.save()
                    
                    # Send verification code to user's email
                    user.profile.send_code(verification_code)
                    print('code',verification_code)
                    request.session['username'] = username  # Store username in session to verify later
                    # store the time that the code was generated in session
                    request.session['timestamp'] = timezone.now().isoformat()
                    messages.success(request, f'Verification code sent to {user.email}')
                    messages.warning(request, f'Your code expires in 5 minutes')
                    return redirect('login-code')
                else:
                    messages.error(request, 'User does not have a correct email address. Please contact administator to update it.')
                    return render(request, 'users/get_code.html', {'form': form})
            else:
                messages.error(request, 'User is not staff')
                return render(request, 'users/get_code.html', {'form': form})
        else:
            # Handle error if user not found
            messages.error(request, 'User not found')
            return render(request, 'users/get_code.html', {'form': form})
    return render(request, 'users/get_code.html', {'form': form})

def login_code(request):
    if request.method == 'POST':
        verification_code = request.POST['code']
        username = request.session.get('username')
        timestamp_str = request.session.get('timestamp')
        timestamp = timezone.datetime.fromisoformat(timestamp_str)
        
        try:
            
            user = authenticate(request, username=username, password=verification_code)
            if user:
                # check expiration time
                if (timezone.now() - timestamp).seconds > 300:
                    messages.error(request, 'Verification code expired')
                    return render(request, 'users/verify.html')
            login(request, user)
            messages.success(request, 'Login successful')
            del request.session['timestamp']  # Remove code_time from session after successful login
            del request.session['username']  # Remove username from session after successful login
            return redirect('training-dashboard')
        except:
            # Authentication failed, handle error
            messages.error(request, 'Invalid verification code')
            return render(request, 'users/verify.html')
    return render(request, 'users/verify.html')
    
# API
# from rest_framework.decorators import api_view
# from django.http import JsonResponse
# from django.contrib.auth import login
# from django.contrib.auth import authenticate


# @api_view(['POST'])
# def api_login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     print(request.data)
#     user = authenticate(username=username, password=password) 
#     if user is not None:
#         login(request, user)
#         return JsonResponse({'message': 'Login successful'}, status=200)
#     else:
#         return JsonResponse({'message': 'Invalid credentials'}, status=400)



