from django.db import models
from django.contrib.auth.models import User
from users.models import Department
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.

    
class Certification(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    departments = models.ManyToManyField(Department, related_name='certifications')

    def __str__(self):
        return f"{self.name}"


class UserCertificationStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certification_statuses')
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE)
    completion_status = models.CharField(max_length=50, choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])
    scheduled_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.certification.name}"

    def save(self, *args, **kwargs):
        # Check if a similar entry already exists for the same user and certification
        existing_entry = UserCertificationStatus.objects.filter(user=self.user, certification=self.certification).exclude(pk=self.pk).first()

        if existing_entry:
             raise ValidationError(_("A certification status for this user and certification already exists. Please choose a different certification or user."))

        super(UserCertificationStatus, self).save(*args, **kwargs)