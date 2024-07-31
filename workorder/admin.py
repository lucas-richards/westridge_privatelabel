from django.contrib import admin

# Register your models here.
from .models import Location, Vendor, Asset, WorkOrder

admin.site.register(Location)
admin.site.register(Vendor)
admin.site.register(Asset)
admin.site.register(WorkOrder)


