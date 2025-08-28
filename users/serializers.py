#uers/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# User Serializer used in login/register/profile views
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role"]
        read_only_fields = ["id"]

# Register Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(
        choices=[("ADMIN", "ADMIN"), ("HR", "HR"), ("EMPLOYEE", "EMPLOYEE")],
        default="EMPLOYEE"
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "role"]
        extra_kwargs = {"username": {"required": False}}

    def validate(self, data):
        if not data.get("username"):
            data["username"] = data.get("email")  # Use email as username fallback
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            role=validated_data.get("role", "EMPLOYEE")
        )
        return user
