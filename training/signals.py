from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from .models import TrainingEvent, ProfileTrainingEvents, RoleTrainingModules
from users.models import Role, Profile


# update the ProfileTrainingEvents row when a TrainingEvent is created
@receiver(post_save, sender=TrainingEvent)
def update_profile_training_events(sender, instance, created, **kwargs):
    if created:
        try:
            profile_training_event = ProfileTrainingEvents.objects.get(profile=instance.profile)
            profile_training_event.update_row()
            print(f'ProfileTrainingEvents updated for {instance.profile.user.username}')
        except:
            print('error updating profile training events row')

# update the RoleTrainingModules object every time a role has been updated
@receiver(post_save, sender=Role)
def create_role_training_modules(sender, instance, created, **kwargds):
    if created:
        role_training_modules = RoleTrainingModules.objects.create(role=instance)
    else:
        role_training_modules = RoleTrainingModules.objects.get(role=instance)
    role_training_modules.update_row()

@receiver(post_save, sender=Profile)
def create_profile_training(sender, instance, created, **kwargds):
    if created:
        profile_training_events = ProfileTrainingEvents.objects.create(profile=instance)
    else:
        profile_training_events = ProfileTrainingEvents.objects.get(profile=instance)
    
