from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db import models
from .models import Certification, CertificationStatus
from users.models import Profile

# @receiver(m2m_changed, sender=Certification.departments.through)
# def create_certification_status_for_departments(sender, instance, action, **kwargs):
#     print('Signal triggered', instance, action, instance.departments.all())
#     if action == 'post_add':
#         # Get all profiles in the associated departments
#         profiles_in_departments = Profile.objects.filter(department__in=instance.departments.all()).distinct()
#         # Create a CertificationStatus for each profile
#         for profile in profiles_in_departments:
#             CertificationStatus.objects.create(certification=instance, profile=profile)