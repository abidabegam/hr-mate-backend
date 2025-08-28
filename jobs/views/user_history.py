# backend/jobs/views/user_history.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from jobs.models import UserJob
from jobs.serializers import UserJobSerializer

class JobHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_jobs = UserJob.objects.filter(user=request.user).order_by('-start_date')  # sort by latest first
        serializer = UserJobSerializer(user_jobs, many=True)
        return Response(serializer.data)
