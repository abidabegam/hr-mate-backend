from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.models.performance_review import PerformanceReview
from users.serializers.performance_review import PerformanceReviewSerializer

# Logged-in user's latest review
class MyPerformanceView(generics.RetrieveAPIView):
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        qs = PerformanceReview.objects.filter(user=self.request.user)
        if not qs.exists():
            raise NotFound("No performance reviews found for this user.")
        return qs.latest('created_at')


# Logged-in user's full history
class MyAllReviewsView(generics.ListAPIView):
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PerformanceReview.objects.filter(user=self.request.user).order_by('-created_at')


# User submits a review (e.g., manager to employee)
class SubmitReviewView(generics.CreateAPIView):
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


# ✅ Admin-only: Get all reviews
class AllPerformanceReviewsAdminView(generics.ListAPIView):
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return PerformanceReview.objects.all().order_by('-created_at')
