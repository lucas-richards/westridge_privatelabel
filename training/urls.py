from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='training-home'),
    path('dashboard/', views.dashboard, name='training-dashboard'),
]