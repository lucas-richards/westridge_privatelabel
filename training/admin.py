from django.contrib import admin

# Register your models here.
from .models import TrainingModule, TrainingEvent

admin.site.register(TrainingModule)
admin.site.register(TrainingEvent)
