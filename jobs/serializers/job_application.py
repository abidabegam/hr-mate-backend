from rest_framework import serializers
from jobs.models.job_application import JobApplication
from jobs.models.job import Job

class JobSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title']

class JobApplicationSerializer(serializers.ModelSerializer):
    job = JobSummarySerializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(),
        source='job',
        write_only=True
    )

    class Meta:
        model = JobApplication
        fields = [
            'id',
            'job',
            'job_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'location',         # ✅ New
            'experience',       # ✅ New
            'linkedin',         # ✅ New
            'current_company',  # ✅ New
            'expected_salary',  # ✅ New
            'start_date',       # ✅ New
            'resume',
            'cover_letter',
            'is_employee',
            'created_at',
            'status',
            'admin_notes',
        ]
