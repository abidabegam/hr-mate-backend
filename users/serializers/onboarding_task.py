from rest_framework import serializers
from users.models.onboarding_task import OnboardingTask

class OnboardingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingTask
        fields = ['id', 'user', 'title', 'description', 'due_date',  # ✅ include new fields
                  'completed', 'uploaded_document', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
