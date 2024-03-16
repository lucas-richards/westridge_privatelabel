from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from datetime import date
import logging
import os

# tasks model

class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_asignee')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Not Started')
    priority = models.CharField(max_length=50, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Low')
    due_date = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def is_past_due(self):
        return date.today() > self.due_date
    
    #  count how many tasks a user has
    @property
    def count_tasks(self):
        return Task.objects.filter(assigned_to=self.assigned_to).count()
    
    # when a task is created, it will send an email to both the author and the asignee with the due date
    def save(self, *args, **kwargs):
        is_new = not self.pk
        # make status default not started
        if is_new:
            self.status = 'Not Started'
        super().save(*args, **kwargs)
        if is_new:
            email_user = os.environ.get('EMAIL_USER')
            email_password = os.environ.get('EMAIL_PASS')
            author_email = self.author.email
            assigned_to_email = self.assigned_to.email

            subject = f' New task created for {self.assigned_to.username}'
            message = f' A new task has been created for {self.assigned_to.username} by {self.author.username}. The task is titled {self.title} and is due on {self.due_date}.'

            try:
                send_mail(subject, message, email_user, [author_email, assigned_to_email], auth_user=email_user, auth_password=email_password)
                logging.info(f'Successfully sent schedule update email to {author_email, assigned_to_email}')
            except Exception as e:
                logging.error(f'Error sending schedule update email to {author_email, assigned_to_email}: {str(e)}')
