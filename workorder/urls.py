from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='workorder-dashboard'),
    path('assets/', views.assets, name='workorder-assets'),
    path('asset/<int:id>/', views.asset, name='workorder-asset'),
    path('asset/add/', views.add_asset, name='workorder-add-asset'),
    path('asset/edit/<int:id>/', views.edit_asset, name='workorder-edit-asset'),
    path('asset/delete/<int:id>/', views.delete_asset, name='workorder-delete-asset'),
    path('vendors/', views.vendors, name='workorder-vendors'),
    path('vendor/<int:id>/', views.vendor, name='workorder-vendor'),
    path('vendor/add/', views.add_vendor, name='workorder-add-vendor'),
    path('vendor/edit/<int:id>/', views.edit_vendor, name='workorder-edit-vendor'),
    path('vendor/delete/<int:id>/', views.delete_vendor, name='workorder-delete-vendor'),
    path('workorders/', views.workorders, name='workorder-workorders'),
    path('workorder/<int:id>/', views.workorder, name='workorder-workorder'),
    path('workorder/add/', views.add_workorder, name='workorder-add-workorder'),
    path('workorder/edit/<int:id>/', views.edit_workorder, name='workorder-edit-workorder'),
    path('workorder/delete/<int:id>/', views.delete_workorder, name='workorder-delete-workorder'),
    
]
