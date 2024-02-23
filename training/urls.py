from django.urls import path
from .views import home
                    # TrainingDetailView, 
                    # TrainingCreateView, 
                    # TrainingUpdateView,
                    # TrainingDeleteView,
                    # UserTrainingListView)
from . import views



urlpatterns = [
    path('', views.home, name='training-home'),
    
]