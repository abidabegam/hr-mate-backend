from rest_framework import serializers
from users.models.performance_review import PerformanceReview

class PerformanceReviewSerializer(serializers.ModelSerializer):
    reviewer_email = serializers.EmailField(source='reviewer.email', read_only=True)

    class Meta:
        model = PerformanceReview
        fields = ['id', 'user', 'reviewer', 'rating', 'comments', 'created_at', 'reviewer_email']
