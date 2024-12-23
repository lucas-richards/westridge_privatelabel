from django.contrib import admin

# Register your models here.
from .models import Customer, Product, Order, Note, Component

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Note)
admin.site.register(Component)



