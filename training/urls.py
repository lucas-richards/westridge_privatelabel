from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='training-home'),
    path('dashboard/', views.dashboard, name='training-dashboard'),
    path('certification/<int:certification_id>/', views.certification_detail, name='training-certification-detail'),
    path('upload/', views.upload_file, name='training-upload_file'),
]