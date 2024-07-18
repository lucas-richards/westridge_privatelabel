from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='tasks-home'),
    path('create/', views.create, name='tasks-create'),
    path('assigned/', views.assigned , name='tasks-assigned'),
    path('update/<int:pk>/', views.update, name='tasks-update'),
    path('delete/<int:pk>/', views.delete, name='tasks-delete'),
]