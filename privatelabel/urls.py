from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='privatelabel-dashboard'),
    path('customers/', views.customers, name='privatelabel-customers'),
    path('orders/', views.orders, name='privatelabel-orders'),
    
]
