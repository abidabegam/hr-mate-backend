from rest_framework import viewsets, permissions
from users.models.registration_request import RegistrationRequest
from users.serializers.registration_request import RegistrationRequestSerializer

class RegistrationRequestViewSet(viewsets.ModelViewSet):
    queryset = RegistrationRequest.objects.all()
    serializer_class = RegistrationRequestSerializer
    permission_classes = [permissions.IsAdminUser]
