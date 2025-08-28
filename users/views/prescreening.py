from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from django.conf import settings

from jobs.models.prescreening_task import PrescreeningTask
from jobs.serializers.prescreening_task import PrescreeningTaskSerializer

# ✅ Admin: List and create prescreening tasks
class PrescreeningTaskListCreateView(generics.ListCreateAPIView):
    queryset = PrescreeningTask.objects.all()
    serializer_class = PrescreeningTaskSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        task = serializer.save()
        application = task.application

        # ✅ Defensive check and send email
        if application and application.email:
            send_mail(
                subject='Prescreening Task Assigned',
                message=f"Dear {application.first_name},\n\nYou have been assigned a new prescreening task for the position: {application.job.title if application.job else 'N/A'}.\n\nPlease log in to the portal to complete it.\n\nThanks,\n{settings.APP_NAME} Team",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[application.email],
                fail_silently=False,
            )

# ✅ Logged-in user can view their prescreening tasks
class MyPrescreeningTasksView(generics.ListAPIView):
    serializer_class = PrescreeningTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PrescreeningTask.objects.filter(application__email=self.request.user.email)

# ✅ Admin deletes a prescreening task
@api_view(["DELETE"])
@permission_classes([permissions.IsAdminUser])
def delete_prescreening_task_view(request, pk):
    try:
        task = PrescreeningTask.objects.get(pk=pk)
        task.delete()
        return Response({"success": True})
    except PrescreeningTask.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
