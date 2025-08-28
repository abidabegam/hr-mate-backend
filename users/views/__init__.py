from .login import login_view, logout_view
from .register import register_view
from .profile import user_profile_view
from .user import UserViewSet, RegistrationRequestViewSet
from .user_details import UserDetailsViewSet, UserDetailsByUserIdView  # ✅ fix:
#from .user_details import UserDetailsViewSet
from .org_chart import OrgChartView

__all__ = [
    "login_view",
    "logout_view",
    "register_view",
    "user_profile_view",
    "UserViewSet",
    "RegistrationRequestViewSet",
    "UserDetailsViewSet",
    "UserDetailsByUserIdView",
    "OrgChartView",
]
