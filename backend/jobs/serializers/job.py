from rest_framework import serializers
from jobs.models.job import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description','department', 'company', 'location', 'salary', 'experience', 'is_posted', 'posted_at', 'created_at']
