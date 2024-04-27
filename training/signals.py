from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from .models import TrainingEvent, ProfileTrainingEvents, RoleTrainingModules
from users.models import Role, Profile

# update the ProfileTrainingEvents object every time a TrainingEvent has been deleted
@receiver(post_delete, sender=TrainingEvent)
def update_profile_training_events(sender, instance, **kwargs):
    profile_training_events = ProfileTrainingEvents.objects.get(profile=instance.profile)
    profile_training_events.update_row()


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
    
