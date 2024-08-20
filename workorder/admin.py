from django.contrib import admin

# Register your models here.
from .models import  Vendor, Asset, WorkOrder, WorkOrderRecord, KPI, KPIValue

admin.site.register(Vendor)
admin.site.register(Asset)
admin.site.register(WorkOrder)
admin.site.register(WorkOrderRecord)
admin.site.register(KPI)
admin.site.register(KPIValue)



