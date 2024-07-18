from django.contrib import admin

# Register your models here.
from .models import TrainingModule, TrainingEvent, ProfileTrainingEvents, RoleTrainingModules, KPI, KPIValue

admin.site.register(TrainingModule)
admin.site.register(TrainingEvent)
admin.site.register(ProfileTrainingEvents)
admin.site.register(RoleTrainingModules)
admin.site.register(KPI)
admin.site.register(KPIValue)


