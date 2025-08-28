from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.exceptions import AuthenticationFailed

from users.auth import JwtTools
from users.serializers import UserSerializer, RegisterSerializer
from users.models import User


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = JwtTools.gen_token(user.id)

        response = Response()
        JwtTools.set_cookie(response, token)
        response.data = {"message": "User registered successfully"}
        return response


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            raise AuthenticationFailed("Invalid credentials")

        token = JwtTools.gen_token(user.id)
        response = Response()
        JwtTools.set_cookie(response, token)
        response.data = {"message": "Login successful"}
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie(settings.JWT['AUTH_COOKIE'])
        response.data = {"message": "Logged out successfully"}
        return response


class UserView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
