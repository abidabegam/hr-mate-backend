from rest_framework import serializers
from jobs.models import UserJob
from jobs.serializers.job import JobSerializer  # ✅ Use this to get job.title
class UserJobSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)  # ✅ This nests the job objec
    class Meta:
        model = UserJob
        fields = '__all__'
