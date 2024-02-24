from django.contrib.auth.models import User
from operator import attrgetter

# make users available to all templates

def all_users(request):
    users = User.objects.all()
    sorted_users = sorted(users, key=attrgetter('profile.birthday'))
    return {'users': sorted_users}