from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from jobs.models import Job, JobApplication
from users.models import User  # Make sure this is imported

class JobCountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        total_jobs = Job.objects.count()
        candidates = JobApplication.objects.values('email').distinct().count()
        employees = User.objects.filter(role='EMPLOYEE').count()

        return Response({
            "total_jobs": total_jobs,
            "candidates": candidates,
            "employees": employees,
            "last_updated": "Today",
        })
