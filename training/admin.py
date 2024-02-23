from django.contrib import admin

# Register your models here.
from .models import Certification, CertificationStatus

admin.site.register(Certification)
admin.site.register(CertificationStatus)
