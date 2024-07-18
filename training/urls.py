from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='training-home'),
    path('percentage/', views.percentage, name='training-percentage'),
    path('supervisors/', views.supervisors, name='training-supervisors'),
    # path('roles/', views.roles, name='training-roles'),
    # path('staff_roles/', views.staff_roles, name='training-staff_roles'),
    path('history/', views.history, name='training-history'),
    path('new_entry/', views.new_entry, name='training-new_entry'),
    path('new_user/', views.new_user, name='training-new_user'),
    path('new_module/', views.new_module, name='training-new_module'),
    path('dashboard/', views.dashboard, name='training-dashboard'),
    path('inactive/', views.inactive, name='training-inactive'),
    path('profile/<int:profile_id>/', views.training_profile, name='training-profile'),
    path('training/', views.grid, name='training-grid'),
    path('role/<int:role_id>/', views.training_role_detail, name='training-role-detail'),
    path('training_module/<int:training_module_id>/', views.training_module_detail, name='training-module-detail'),
    path('training_event/<int:training_event_id>/', views.training_event_detail, name='training-event-detail'),
    # confirm delete
    path('training_event/<int:training_event_id>/delete/confirm/', views.training_confirm_delete, name='training-confirm-delete'),
    # delete
    path('training_event/<int:training_event_id>/delete/', views.training_delete, name='training-event-delete'),
    path('upload/', views.upload_file, name='training-upload_file'),
    path('send_reminder_email/<int:training_module_id>/', views.send_reminder_email, name='training-send_reminder_email'),
    # api urls
    # path('api/dashboard', views.api_dashboard, name='training-api-dashboard'),
    # path('api/TrainingModules', TrainingModules.as_view(), name='TrainingModules'),
    # path('api/TrainingEvent', TrainingEvents.as_view(), name='TrainingEvent'),
    
]
