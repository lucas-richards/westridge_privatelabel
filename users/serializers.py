# from rest_framework import serializers
# from .models import User, Profile, Role

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username']  # Include only the 'username' field

# class ProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer()  # Include UserSerializer as a nested serializer

#     class Meta:
#         model = Profile
#         fields = '__all__'
