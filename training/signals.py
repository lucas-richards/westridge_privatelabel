from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db import models
from .models import TrainingModule, TrainingEvent
from users.models import Profile

# @receiver(m2m_changed, sender=TrainingModule.departments.through)
# def create_TrainingModule_status_for_departments(sender, instance, action, **kwargs):
#     print('Signal triggered', instance, action, instance.departments.all())
#     if action == 'post_add':
#         # Get all profiles in the associated departments
#         profiles_in_departments = Profile.objects.filter(department__in=instance.departments.all()).distinct()
#         # Create a TrainingEvent for each profile
#         for profile in profiles_in_departments:
#             TrainingEvent.objects.create(TrainingModule=instance, profile=profile)