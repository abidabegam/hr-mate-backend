from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, JobApplicationViewSet, UserJobViewSet
from jobs.views.user_history import JobHistoryView
from jobs.views.prescreening_task_view import PrescreeningTaskViewSet
from jobs.views.job_application import ApplyJobView  # ✅ updated
from jobs.views.download_resume import download_resume
from jobs.views.metrics import JobCountView
from jobs.views.test_email import TestEmailView

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'job-applications', JobApplicationViewSet, basename='job-application')
router.register(r'user-jobs', UserJobViewSet, basename='user-job')
router.register(r'prescreening-tasks', PrescreeningTaskViewSet)

urlpatterns = [
    path('apply/<int:job_id>/', ApplyJobView.as_view(), name='apply-job'),
    #path('apply-job/<int:job_id>/', ApplyJobView.as_view(), name='apply-job'),
    path('user-history/', JobHistoryView.as_view(), name='job-history'),
    path('applications/<int:app_id>/resume/', download_resume, name='download_resume'),
    path('count/', JobCountView.as_view(), name='job-count'),
    path('', include(router.urls)),
    path('test-email/', TestEmailView.as_view()),
]
