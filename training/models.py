from django.db import models
from users.models import Profile
from datetime import date
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
import logging
import os


# Create your models here.

    
class Certification(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # expiration time in months
    exp_months = models.IntegerField(null=True, blank=True)
    # schedule date for the certification
    scheduled_date = models.DateTimeField(null=True, blank=True)
    # each certification corresponds to one role
    roles = models.ManyToManyField('users.Role', related_name='certifications', blank=True)

    def __str__(self):
        return f"{self.name}"
    
    # profiles with this cert and their status
    def get_incomplete_certification_statuses(self):
        return CertificationStatus.objects.filter(certification=self, status__in=['To be Scheduled', 'Scheduled', 'Expired', 'About To Expired'])


class CertificationStatus(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('To be Scheduled', 'To be Scheduled'),('Scheduled', 'Scheduled'), ('Expired', 'Expired'), ('About To Expired', 'About To Expired'), ('Completed', 'Completed')], default='To be Scheduled')
    completed_date = models.DateField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.profile.user.username} - {self.certification.name}"
    
    
    #  date that the certification expires based on the cert exp_months and conpleted_date
    def expiration_date(self):
        if self.completed_date:
            # Assuming exp_months is a field in the Certification model
            if self.certification.exp_months:
                expiration_months = self.certification.exp_months
                return self.completed_date + timezone.timedelta(days=30 * expiration_months)
            else:
                return None
        else:
            return None

    
    # Send email notification when a certification is completed
    def send_schedule_notification(self):
        email_user = os.environ.get('EMAIL_USER')
        email_password = os.environ.get('EMAIL_PASS')
        user_email = self.profile.user.email

        subject = f'Schedule Updated: {self.certification.name} was scheduled'
        message = f'Your certificate {self.certification.name} status is {self.status}. New training scheduled on {timezone.localtime(self.certification.scheduled_date)}.'

        try:
            send_mail(subject, message, email_user, [user_email], auth_user=email_user, auth_password=email_password)
            logging.info(f'Successfully sent schedule update email to {user_email}')
        except Exception as e:
            logging.error(f'Error sending schedule update email to {user_email}: {str(e)}')
