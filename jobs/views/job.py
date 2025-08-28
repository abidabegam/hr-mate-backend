from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from jobs.models import Job
from jobs.serializers import JobSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location', 'department', 'salary', 'experience', 'type', 'is_posted']

    # Option A: simplest
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Option B: explicit per-action (use this instead if you prefer)
    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         return [AllowAny()]
    #     return [IsAuthenticated()]
