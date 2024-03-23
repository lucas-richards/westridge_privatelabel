from django.urls import path
from . import views
from .views import Certifications, StatusCertifications

urlpatterns = [
    path('', views.home, name='training-home'),
    path('dashboard/', views.dashboard, name='training-dashboard'),
    path('certification/<int:certification_id>/', views.certification_detail, name='training-certification-detail'),
    path('statusCertification/<int:certification_id>/', views.statusCertification_detail, name='training-statusCertification-detail'),
    path('upload/', views.upload_file, name='training-upload_file'),
    # api urls
    # path('api/dashboard', views.api_dashboard, name='training-api-dashboard'),
    path('api/certifications', Certifications.as_view(), name='certifications'),
    path('api/statusCertifications', StatusCertifications.as_view(), name='statusCertifications'),
    path('api/certification/<int:certification_id>', views.api_certification_detail, name='training-api-certification-detail'),
    path('api/statusCertification/<int:certification_id>', views.api_statusCertification_detail, name='training-api-statusCertification-detail'),
    path('api/upload', views.api_upload_file, name='training-api-upload_file'),
]