from rest_framework import serializers
from .models import CertificationStatus, Certification
from users.serializers import ProfileSerializer


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

class CertificationStatusSerializer(serializers.ModelSerializer):
    certification = CertificationSerializer()  # Include CertificationSerializer as a nested serializer
    profile = ProfileSerializer()  # Include ProfileSerializer as a nested serializer
    
    class Meta:
        model = CertificationStatus
        fields = '__all__'