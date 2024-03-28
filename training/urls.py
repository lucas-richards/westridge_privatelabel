from django.urls import path
from . import views
from .views import Certifications, StatusCertifications

urlpatterns = [
    path('', views.home, name='training-home'),
    path('all_trainings/', views.all_trainings, name='training-all_trainings'),
    path('history/', views.history, name='training-history'),
    path('dashboard/', views.dashboard, name='training-dashboard'),
    path('schedule/<int:certification_id>/', views.schedule, name='training-schedule'),
    path('certification/<int:certification_id>/', views.certification_detail, name='training-certification-detail'),
    path('statusCertification/<int:certification_id>/', views.statusCertification_detail, name='training-statusCertification-detail'),
    path('upload/', views.upload_file, name='training-upload_file'),
    path('send_reminder_email/<int:certification_id>/', views.send_reminder_email, name='training-send_reminder_email'),
    # api urls
    # path('api/dashboard', views.api_dashboard, name='training-api-dashboard'),
    path('api/certifications', Certifications.as_view(), name='certifications'),
    path('api/statusCertifications', StatusCertifications.as_view(), name='statusCertifications'),
    
]