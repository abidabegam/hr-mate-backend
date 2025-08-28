from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import UserDetails
from jobs.serializers import JobSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role"]
        read_only_fields = ["id", "role"]

class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]

    def create(self, validated_data):
        email = validated_data["email"]
        user = User.objects.create_user(
            username=email,            # IMPORTANT ➔ Username = Email!
            email=email,
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user

class UserDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    manager = UserSerializer(read_only=True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = UserDetails
        fields = [
            "id",
            "user",
            "manager",
            "job",
            "phone",
            "location",
            "salary",
            "profile_picture",
            "department",
            "created_at",
        ]





#from rest_framework import serializers
#from users.models import User


#class RegisterSerializer(serializers.ModelSerializer):
   # password = serializers.CharField(write_only=True, min_length=8)

    #class Meta:
        #model = User
        #fields = ['id', 'email', 'first_name', 'last_name', 'password']

    #def create(self, validated_data):
        #user = User.objects.create_user(**validated_data)
        #return user
