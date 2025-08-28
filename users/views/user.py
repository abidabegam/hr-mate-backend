from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import User, RegistrationRequest
from users.serializers import (
    RegistrationRequestSerializer,
    UserSerializer,
    RegisterSerializer,
)

# Registration view
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# Profile view for authenticated user
class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# Admin/User viewset (for listing or managing users)
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


# Registration request viewset
class RegistrationRequestViewSet(viewsets.ModelViewSet):
    serializer_class = RegistrationRequestSerializer
    queryset = RegistrationRequest.objects.all()
    permission_classes = [IsAuthenticated]
