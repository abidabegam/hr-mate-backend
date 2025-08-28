from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models.user_details import UserDetails
from users.serializers.user import UserSerializer
from jobs.serializers import JobSerializer, UserJobSerializer

User = get_user_model()

class OrgChartUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'role')

class UserDetailsSerializer(serializers.ModelSerializer):
    user      = OrgChartUserSerializer(read_only=True)
    manager   = OrgChartUserSerializer(read_only=True)
    job       = JobSerializer(read_only=True)
    user_jobs = UserJobSerializer(
        source='user.job_assignments',
        many=True,
        read_only=True
    )

    class Meta:
        model = UserDetails
        fields = [
            'id',
            'user',
            'manager',
            'job',
            'department',
            'job_title',
            'location',

            # ← new compensation fields:
            'salary',
            'bonus',
            'stock_options',
            'updated_at',

            'phone',
            'profile_picture',
            'approved',
            'created_at',
            'user_jobs',
        ]
        read_only_fields = ['id', 'created_at']
