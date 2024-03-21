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
    scheduled_date = models.DateField(null=True, blank=True)
    # each certification corresponds to one role
    roles = models.ManyToManyField('users.Role', related_name='certifications', blank=True)

    def __str__(self):
        return f"{self.name}"


class CertificationStatus(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])
    completed_date = models.DateField(null=True, blank=True, default=timezone.now() + timezone.timedelta(days=15) )
    

    def __str__(self):
        return f"{self.profile.user.username} - {self.certification.name}"

    
    # Send email notification when a certification is completed
    def send_schedule_notification(self):
        email_user = os.environ.get('EMAIL_USER')
        email_password = os.environ.get('EMAIL_PASS')
        user_email = self.profile.user.email

        subject = 'Schedule Updated: Certificate Notification'
        message = f'Your certificate {self.certification.name} is scheduled for {self.completed_date}.'

        try:
            send_mail(subject, message, email_user, [user_email], auth_user=email_user, auth_password=email_password)
            logging.info(f'Successfully sent schedule update email to {user_email}')
        except Exception as e:
            logging.error(f'Error sending schedule update email to {user_email}: {str(e)}')
    
class Command(BaseCommand):
    help = 'Send reminder emails for certificates scheduled for tomorrow'

    def handle(self, *args, **options):
        # Set up logging
        logging.basicConfig(filename='email_reminder_log.txt', level=logging.INFO)

        tomorrow = timezone.now() + timezone.timedelta(days=1)
        certificates = CertificationStatus.objects.filter(completed_date=tomorrow)

        email_user = os.environ.get('EMAIL_USER')
        email_password = os.environ.get('EMAIL_PASS')

        for certification_status in certificates:
            user_email = certification_status.profile.user.email
            subject = 'Reminder: Certificate Scheduled for Tomorrow'
            message = f'Your certificate {certification_status.certification.name} is scheduled for tomorrow.'

            try:
                send_mail(subject, message, email_user, [user_email], auth_user=email_user, auth_password=email_password)
                # Log successful email sending
                logging.info(f'Successfully sent reminder email to {user_email}')
            except Exception as e:
                # Log any errors that occur during email sending
                logging.error(f'Error sending email to {user_email}: {str(e)}')