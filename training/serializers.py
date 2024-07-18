# from rest_framework import serializers
# from .models import TrainingEvent, TrainingModule
# from users.serializers import ProfileSerializer


# class TrainingModuleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TrainingModule
#         fields = '__all__'

# class TrainingEventSerializer(serializers.ModelSerializer):
#     training_module = TrainingModuleSerializer()  # Include TrainingModuleSerializer as a nested serializer
#     profile = ProfileSerializer()  # Include ProfileSerializer as a nested serializer
    
#     class Meta:
#         model = TrainingEvent
#         fields = '__all__'