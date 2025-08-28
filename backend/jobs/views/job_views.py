from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from jobs.models import Job, JobApplication, UserJob
from jobs.serializers import JobSerializer, JobApplicationSerializer, UserJobSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role != 'ADMIN':
            return Response({'detail': 'Only admins can create jobs.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.user.role != 'ADMIN':
            return Response({'detail': 'Only admins can update jobs.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'ADMIN':
            return Response({'detail': 'Only admins can delete jobs.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]


class UserJobViewSet(viewsets.ModelViewSet):
    queryset = UserJob.objects.all()
    serializer_class = UserJobSerializer
    permission_classes = [IsAuthenticated]
