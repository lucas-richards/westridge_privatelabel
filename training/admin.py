from django.contrib import admin

# Register your models here.
from .models import TrainingModule, TrainingEvent, ProfileTrainingEvents, RoleTrainingModules

admin.site.register(TrainingModule)
admin.site.register(TrainingEvent)
admin.site.register(ProfileTrainingEvents)
admin.site.register(RoleTrainingModules)

