from rest_framework import serializers
from .models import Job, UserJob
from .serializers.job_application import JobApplicationSerializer  # ✅ Correct import
from .prescreening_task import PrescreeningTaskSerializer


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title']


class UserJobSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)

    class Meta:
        model = UserJob
        fields = [
            'id',
            'user',
            'job',
            'pay',
            'started_at',
            'ended_at',
        ]
