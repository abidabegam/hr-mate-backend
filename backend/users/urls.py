from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views.onboarding import complete_task_view
# ← Add MyJobDetailsView here
from users.views.user_details import (
    UserDetailsByUserIdView,
    MyJobDetailsView,               # ← newly imported
)
from users.views.user_details import UserDetailsByUserIdView
from users.views.onboarding import (
    UserOnboardingTaskListView,
    MyOnboardingTasksView,
    OnboardingTaskDetailView,
    AllUserDetailsViewSet,
)
from users.views.message import MessageViewSet
from users.views.referral import MyReferralsView, SubmitReferralView
from users.views.performance import MyPerformanceView, SubmitReviewView, MyAllReviewsView
from users.views.notification import NotificationViewSet
from users.views.compensation import MyCompensationView
from users.views.performance import AllPerformanceReviewsAdminView
#from users.views.compensation import CompensationView
from users.views import (
    login_view,
    logout_view,
    register_view,
    user_profile_view,
    UserViewSet,
    RegistrationRequestViewSet,
    UserDetailsViewSet,
    OrgChartView,
)

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')  # ✅ Move this up
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'registration-requests', RegistrationRequestViewSet, basename='registration-request')
router.register(r'user-details', UserDetailsViewSet, basename='user-details')
router.register(r'details', AllUserDetailsViewSet, basename='all-user-details')
router.register(r'', UserViewSet, basename='user')  # ✅ This must be last

urlpatterns = [
    # Auth & profile
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', user_profile_view, name='profile'),

    # Org Chart + User detail
    path('org-chart/', OrgChartView.as_view(), name='org-chart'),
    path('user-details/by-user/<int:user_id>/', UserDetailsByUserIdView.as_view(), name='user-details-by-user-id'),

    # Onboarding
    path('<int:user_id>/onboarding-tasks/', UserOnboardingTaskListView.as_view(), name='user-onboarding-tasks'),
    path('my-tasks/', MyOnboardingTasksView.as_view(), name='my-onboarding-tasks'),
    path('onboarding-tasks/<int:id>/', OnboardingTaskDetailView.as_view(), name='onboarding-task-detail'),
    path('onboarding-tasks/<int:id>/complete/', complete_task_view, name='complete-task'),

    # Referrals
    path('referrals/mine/', MyReferralsView.as_view(), name='my-referrals'),
    path('referrals/', SubmitReferralView.as_view(), name='submit-referral'),

    # Performance
    path('performance/me/', MyPerformanceView.as_view(), name='my-performance'),
    path('reviews/submit/', SubmitReviewView.as_view(), name='submit-review'),
    path('performance/my-all-reviews/', MyAllReviewsView.as_view(), name='my-all-reviews'),
    path('compensation/me/', MyCompensationView.as_view(), name='my-compensation'),
    path('performance/all-reviews/', AllPerformanceReviewsAdminView.as_view(), name='all-performance-reviews'),


    # **New**: Job Details for current user
    path('job-details/me/',   MyJobDetailsView.as_view(),     name='my-job-details'),


    # ✅ ViewSets
    path('', include(router.urls)),
]
