# backend/jobs/serializers/prescreening_task.py

from rest_framework import serializers
from jobs.models.prescreening_task import PrescreeningTask
from jobs.models.job_application import JobApplication

class PrescreeningTaskSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    job_title = serializers.SerializerMethodField()

    class Meta:
        model = PrescreeningTask
        fields = [
            'id',
            'application',
            'title',
            'description',
            'file',
            'status',
            'submitted_file',
            'submitted_at',
            'created_at',
            'email',
            'job_title',
        ]
        read_only_fields = ['submitted_at', 'submitted_file']

    def get_email(self, obj):
        return obj.application.email if obj.application else None

    def get_job_title(self, obj):
        return obj.application.job.title if obj.application and obj.application.job else None
