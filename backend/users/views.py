from django.contrib.auth import get_user_model
from rest_framework import status, permissions, viewsets, mixins
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import (
    UserSerializer,
    RegisterSerializer,
    RegistrationRequestSerializer,
)
from users.serializers.profile import UserProfileSerializer
from users.serializers.user_details import UserDetailsSerializer
from users.models import RegistrationRequest, UserDetails
from users.models.message import Message  # ✅ Import Message model

User = get_user_model()


def is_valid_user(user):
    return user.is_active


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"detail": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if not is_valid_user(user):
        return Response({"detail": "Inactive user"}, status=status.HTTP_403_FORBIDDEN)

    refresh = RefreshToken.for_user(user)
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": UserSerializer(user).data,
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        UserDetails.objects.create(user=user)

        # ✅ Send welcome message
        try:
            sender = User.objects.filter(is_staff=True).first() or User.objects.exclude(id=user.id).first()
            if sender:
                Message.objects.create(
                    sender=sender,
                    recipient=user,
                    text="🎉 Welcome to WorkMate! Let us know if you need help.",
                )
        except Exception as e:
            print("⚠️ Failed to send welcome message:", e)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def user_profile_view(request):
    user = request.user
    user_details, created = UserDetails.objects.get_or_create(user=user)

    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserDetailsSerializer(user_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserDetails.objects.select_related('user', 'manager', 'job').all()

    @action(detail=False, methods=['get'], url_path='by-user/(?P<user_id>[^/.]+)')
    def by_user(self, request, user_id=None):
        try:
            details = UserDetails.objects.select_related('user', 'manager', 'job').get(user__id=user_id)
            serializer = self.get_serializer(details)
            return Response(serializer.data)
        except UserDetails.DoesNotExist:
            return Response({'detail': 'User details not found'}, status=404)
