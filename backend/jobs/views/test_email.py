from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

class TestEmailView(APIView):
    def get(self, request):
        try:
            send_mail(
                subject="✅ WorkMate Email Test",
                message="This is a test email from WorkMate.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],  # or your Gmail directly
                fail_silently=False,
            )
            return Response({"success": True, "message": "Test email sent ✅"})
        except Exception as e:
            return Response({"success": False, "error": str(e)})
