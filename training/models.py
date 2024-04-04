from django.db import models
from users.models import Profile
from datetime import date
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
import logging
import os


# Create your models here.

    
class TrainingModule(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # expiration time in months
    retrain_months = models.IntegerField(null=True, blank=True)
    # schedule date for the TrainingModule
    scheduled_date = models.DateTimeField(null=True, blank=True)
    # each TrainingModule corresponds to one role
    roles = models.ManyToManyField('users.Role', related_name='TrainingModules', blank=True)

    def __str__(self):
        return f"{self.name}"
    
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

    # get training events for this training module
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
    
    
    #  date that the training_module expires based on the cert retrain_months and conpleted_date
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
        
    #  create a function that gives a satus of the training_module: expired, about to expire, of ok
    def status(self):
        today = timezone.now().date()
        if self.completed_date:
            if self.expiration_date():
                if self.expiration_date() < today:
                    return 'Expired'
                elif self.expiration_date() < today + timezone.timedelta(days=90):
                    return 'About to expire'
                else:
                    return 'Ok'
            else:
                return 'Ok'
        else:
            return 'Incomplete'

    
    # Send email notification when a training_module is completed
    def send_schedule_notification(self):
        email_user = os.environ.get('EMAIL_USER')
        email_password = os.environ.get('EMAIL_PASS')
        user_email = self.profile.user.email

        subject = f'Schedule Updated: {self.training_module.name} was scheduled'
        message = f'Your certificate {self.training_module.name} is due. New training scheduled on {timezone.localtime(self.training_module.scheduled_date)}.'

        try:
            send_mail(subject, message, email_user, [user_email], auth_user=email_user, auth_password=email_password)
            logging.info(f'Successfully sent schedule update email to {user_email}')
        except Exception as e:
            logging.error(f'Error sending schedule update email to {user_email}: {str(e)}')

    
