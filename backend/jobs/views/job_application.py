from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from jobs.models import Job
from jobs.serializers.job_application import JobApplicationSerializer
import logging
import traceback
import os

logger = logging.getLogger(__name__)

class ApplyJobView(APIView):
    def post(self, request, job_id):
        try:
            # ✅ Check if job exists
            try:
                job = Job.objects.get(id=job_id)
            except Job.DoesNotExist:
                logger.error(f"❌ Job with id {job_id} not found.")
                return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

            # ✅ Fix: match expected serializer field name
            data = request.data.copy()
            data['job'] = job.id

            serializer = JobApplicationSerializer(data=data)
            if serializer.is_valid():
                application = serializer.save()
                validated = serializer.validated_data
                logger.info(f"✅ Application submitted for {validated.get('email')}")

                # ✅ Send confirmation email
                applicant_email = validated.get("email")
                if applicant_email:
                    subject = f"Application Received for {job.title}"
                    message = f"""Hi {validated.get('first_name')},

Thank you for applying for the position of {job.title} at WorkMate.
We have received your application and will be reviewing it shortly.

Best regards,  
WorkMate Team
"""
                    from_email = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@workmate.com")
                    logger.info(f"📧 Sending email to {applicant_email} from {from_email}")
                    try:
                        send_mail(subject, message, from_email, [applicant_email])
                        logger.info("✅ Email sent successfully")
                    except Exception as email_error:
                        logger.error(f"❌ Failed to send email: {email_error}")

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            logger.error(f"❌ Validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error("❌ Exception during job application: " + str(e))
            logger.debug(traceback.format_exc())
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
