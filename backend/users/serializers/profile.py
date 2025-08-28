from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.serializers.user_details import UserDetailsSerializer

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    details = UserDetailsSerializer(source='userdetails', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'details']
