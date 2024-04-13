from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='training-home'),
    path('percentage/', views.percentage, name='training-percentage'),
    path('supervisors/', views.supervisors, name='training-supervisors'),
    path('modules/', views.modules, name='training-modules'),
    # path('roles/', views.roles, name='training-roles'),
    # path('staff_roles/', views.staff_roles, name='training-staff_roles'),
    path('history/', views.history, name='training-history'),
    path('new_entry/', views.new_entry, name='training-new_entry'),
    path('new_user/', views.new_user, name='training-new_user'),
    path('', views.dashboard, name='training-dashboard'),
    path('schedule/<int:training_module_id>/', views.schedule, name='training-schedule'),
    path('training_module/<int:training_module_id>/', views.training_module_detail, name='training-module-detail'),
    path('training_event/<int:training_event_id>/', views.training_event_detail, name='training-event-detail'),
    path('upload/', views.upload_file, name='training-upload_file'),
    path('send_reminder_email/<int:training_module_id>/', views.send_reminder_email, name='training-send_reminder_email'),
    # api urls
    # path('api/dashboard', views.api_dashboard, name='training-api-dashboard'),
    # path('api/TrainingModules', TrainingModules.as_view(), name='TrainingModules'),
    # path('api/TrainingEvent', TrainingEvents.as_view(), name='TrainingEvent'),
    
]