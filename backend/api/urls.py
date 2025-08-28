from django.urls import path
from .views import get_org_chart, get_employee_profile  # Ensure these functions exist in views.py

urlpatterns = [
    path('org-chart/', get_org_chart, name='org_chart'),
    path('employee/profile/', get_employee_profile, name='employee_profile'),
]
