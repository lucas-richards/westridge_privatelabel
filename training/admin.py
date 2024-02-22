from django.contrib import admin

# Register your models here.
from .models import Certification, UserCertificationStatus

admin.site.register(Certification)
admin.site.register(UserCertificationStatus)
