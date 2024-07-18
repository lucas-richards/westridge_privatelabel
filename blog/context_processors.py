from django.contrib.auth.models import User
from operator import attrgetter
from users.models import Profile

# make users available to all templates

def all_users(request):
    # filter user with birthday
    users = User.objects.exclude(profile__birthday__isnull=True)
    sorted_users = sorted(users, key=attrgetter('profile.birthday'))
    return {'users': sorted_users}

def all_profiles(request):
    # filter user with birthday
    profiles = Profile.objects.all()
    return {'profiles': profiles}