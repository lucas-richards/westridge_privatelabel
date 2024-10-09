from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='privatelabel-dashboard'),
    path('customers/', views.customers, name='privatelabel-customers'),
    path('orders/', views.orders, name='privatelabel-orders'),
    path('order/new/', views.new_order, name='privatelabel-new_order'),
    path('order/<str:pk>/', views.order, name='privatelabel-order'),
    

    
]
