from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='privatelabel-dashboard'),
    path('customers/', views.customers, name='privatelabel-customers'),
    path('orders/', views.orders, name='privatelabel-orders'),
    path('order/new/', views.new_order, name='privatelabel-new_order'),
    path('order/<str:pk>/', views.order, name='privatelabel-order'),
    path('customer/new/', views.new_customer, name='privatelabel-new_customer'),
    path('customer/<str:pk>/', views.customer, name='privatelabel-customer'),
    path('customer/<str:pk>/new_product/', views.new_product, name='privatelabel-new_product'),
    path('order/<str:pk>/add_note/', views.add_note, name='privatelabel-add-note'),
    

    
]
