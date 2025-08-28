from rest_framework import serializers
from users.models import RegistrationRequest

class RegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationRequest
        fields = '__all__'
