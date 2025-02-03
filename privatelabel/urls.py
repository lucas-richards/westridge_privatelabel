from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='privatelabel-dashboard'),
    path('customers/', views.customers, name='privatelabel-customers'),
    path('orders/', views.orders, name='privatelabel-orders'),
    path('orders/accounting/', views.orders_accounting, name='privatelabel-orders-accounting'),
    path('orders/gregg/', views.orders_gregg, name='privatelabel-orders-gregg'),
    path('order/new/', views.new_order, name='privatelabel-new_order'),
    path('order/<str:pk>/', views.order, name='privatelabel-order'),
    path('order_attachments/<str:pk>/', views.order_attachments, name='privatelabel-order-attachments'),
    path('customer/new/', views.new_customer, name='privatelabel-new_customer'),
    path('customer/<str:pk>/', views.customer, name='privatelabel-customer'),
    path('customer/<str:pk>/new_product/', views.new_product, name='privatelabel-new_product'),
    path('order/<str:pk>/add_note/', views.add_note, name='privatelabel-add-note'),
    path('order/<str:pk>/delete/', views.delete_order, name='privatelabel-order-delete'),
    

    
]
