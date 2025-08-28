from rest_framework import generics, permissions, viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from users.models.onboarding_task import OnboardingTask
from users.models import UserDetails
from users.serializers.onboarding_task import OnboardingTaskSerializer
from users.serializers.user_details import UserDetailsSerializer
from users.emails import UserEmails  # Email integration

#  View: Admin can List and Create onboarding tasks for a specific user
class UserOnboardingTaskListView(generics.ListCreateAPIView):
    serializer_class = OnboardingTaskSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return OnboardingTask.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        user_id = self.kwargs['user_id']
        task = serializer.save(user_id=user_id)
        UserEmails.send_onboarding_task_email(task)  # Send email after task assignment

#  View: Logged-in user can list their own tasks
class MyOnboardingTasksView(generics.ListAPIView):
    serializer_class = OnboardingTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OnboardingTask.objects.filter(user=self.request.user)

# View: User can view task detail (only their own task)
class OnboardingTaskDetailView(generics.RetrieveAPIView):
    serializer_class = OnboardingTaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return OnboardingTask.objects.filter(user=self.request.user)

#  Admin view: Read-only access to all user details
class AllUserDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserDetails.objects.select_related("user", "manager", "job")
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAdminUser]

# View: Logged-in user marks a task as completed
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def complete_task_view(request, id):
    try:
        task = OnboardingTask.objects.get(id=id, user=request.user)
        task.completed = True
        task.save()
        return Response({"success": True, "message": "Task marked as completed."})
    except OnboardingTask.DoesNotExist:
        return Response(
            {"error": "Task not found or not authorized."},
            status=status.HTTP_404_NOT_FOUND
        )
