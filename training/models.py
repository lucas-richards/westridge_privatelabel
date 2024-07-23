from django.db import models
from users.models import Profile, User, Role
from datetime import date
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
import logging
import os


# KPI models
class KPI(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class KPIValue(models.Model):
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.kpi.name} - {self.date}: {self.value}"
    
class TrainingModule(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # other boolean to identify modules other than required by FDA
    other = models.BooleanField(default=False)
    # expiration time in months
    retrain_months = models.IntegerField(null=True, blank=True)
    


    def __str__(self):
        return f"{self.name}"

    # when a module is created, update the RoleTrainingModules row and Profile trainings
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for role in Role.objects.all():
            role_training_modules = RoleTrainingModules.objects.get(role=role)
            role_training_modules.update_row()
        print('RoleTrainingModules updated')

        for profile in Profile.objects.all():
            print('profile',profile)
            profile_training_events = ProfileTrainingEvents.objects.get(profile=profile)
            profile_training_events.update_row()
        print('ProfileTrainingEvents updated')
    
    # profiles with this cert 
    def get_incomplete_training_modules_profiles(self):
        profiles = []
        for profile in Profile.objects.all():
            must_have = profile.must_have_training_modules()
            event = TrainingEvent.objects.filter(profile=profile, training_module=self).first()
            print(f'Event: {event}, status: {event.status() if event else ""}')
            status = event.status() if event else ''
            if status == 'Ok':
                continue
            if status == 'Expired' or status == 'About to expire' or self in must_have:
                profiles.append(profile)
        return profiles

#     # get training events for this training module
    def get_training_events(self):
        return TrainingEvent.objects.filter(training_module=self)

class TrainingEvent(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    training_module = models.ForeignKey(TrainingModule, on_delete=models.CASCADE)
    completed_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-completed_date']
    

    def __str__(self):
        return f"{self.profile.user.username} - {self.training_module.name}"
    
    # update the ProfileTrainingEvents row when a TrainingEvent is created or deleted
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        profile_training_event = ProfileTrainingEvents.objects.get(profile=self.profile)
        profile_training_event.update_row()
        print(f'ProfileTrainingEvents updated for {self.profile.user.username}')
    
    
#     #  date that the training_module expires based on the cert retrain_months and conpleted_date
    def expiration_date(self):
        if self.completed_date:
            # Assuming retrain_months is a field in the training_module model
            if self.training_module.retrain_months:
                expiration_months = self.training_module.retrain_months
                return self.completed_date + timezone.timedelta(days=30 * expiration_months)
            else:
                return None
        else:
            return None
        
#     #  create a function that gives a satus of the training_module: expired, about to expire, of ok
    def status(self):
        today = timezone.now().date()
        if self.completed_date:
            if self.expiration_date():
                if self.expiration_date() < today:
                    return 'Expired'
                elif self.expiration_date() < today + timezone.timedelta(days=90):
                    return 'To Expire'
                else:
                    return self.completed_date.strftime('%m/%d/%y')
            else:
                return self.completed_date.strftime('%m/%d/%y')
        else:
            return 'Incomplete'
    
class ProfileTrainingEvents(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    row = models.TextField(default='', blank=True)

    def __str__(self):
        return f"{self.profile} {self.row}"
    
    def update_row(self):
        must_have = self.profile.must_have_training_modules()
        training_modules = TrainingModule.objects.all().order_by('name')  # Order training modules alphabetically
        events = []
        for training_module in training_modules:
            event = TrainingEvent.objects.filter(profile=self.profile, training_module=training_module).first()

            if event and training_module in must_have:
                events.append(event.completed_date.strftime('%m/%d/%y'))
            elif event and training_module not in must_have:
                events.append('+')
            elif training_module not in must_have:
                events.append('-')
            else:
                events.append(training_module.name)

        self.row = ','.join(events)
        print(f'{self.profile} updated training events: {self.row}')
        self.save()

class RoleTrainingModules(models.Model):
    role = models.OneToOneField(Role, on_delete=models.CASCADE)
    row = models.TextField(default='', blank=True)

    def __str__(self):
        return f"{self.role.name} {self.row}"
    
    def update_row(self):
        from training.models import TrainingModule
        training_modules = TrainingModule.objects.all().order_by('name')
        row = []
        for training_module in training_modules:
            if training_module in self.role.training_modules.all():
                row.append(training_module.name)
            else:
                row.append('-')
        self.row = ','.join(row)
        self.save()