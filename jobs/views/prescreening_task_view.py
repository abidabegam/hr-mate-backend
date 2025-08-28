# backend/jobs/views/prescreening_task_view.py

from rest_framework import viewsets, permissions
from django.core.mail import send_mail
from django.conf import settings

from jobs.models.prescreening_task import PrescreeningTask
from jobs.serializers.prescreening_task import PrescreeningTaskSerializer

class PrescreeningTaskViewSet(viewsets.ModelViewSet):  # ✅ this is the required name!
    queryset = PrescreeningTask.objects.all()
    serializer_class = PrescreeningTaskSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        task = serializer.save()
        applicant_email = task.application.email

        if applicant_email:
            try:
                send_mail(
                    subject="Prescreening Task Assigned",
                    message=(
                        "Hello,\n\n"
                        "You have been assigned a prescreening task for the job application.\n"
                        "Please log in to WorkMate and complete your task.\n\n"
                        "Thanks,\nWorkMate Team"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[applicant_email],
                    fail_silently=False,
                )
                print(f"✅ Email sent to {applicant_email}")
            except Exception as e:
                print(f"❌ Email sending failed: {e}")
