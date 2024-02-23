from django.db import models
from users.models import Profile
from datetime import date

# Create your models here.

    
class Certification(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"


class CertificationStatus(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])
    scheduled_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.profile.user.username} - {self.certification.name}"
    
    def is_past_due(self):
        return date.today() > self.due_date