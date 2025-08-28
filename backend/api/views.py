from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
#from .models import UserDetails, User  # Ensure these models exist
from django.contrib.auth import get_user_model
from .models import UserDetails
User = get_user_model()  # Get the correct User model dynamically
@login_required
def get_org_chart(request):
    employees = UserDetails.objects.select_related('user', 'manager').all()
    org_data = [
        {
            "id": emp.user.id,
            "name": f"{emp.user.first_name} {emp.user.last_name}",
            "manager_id": emp.manager.id if emp.manager else None
        }
        for emp in employees
    ]
    return JsonResponse(org_data, safe=False)

@login_required
def get_employee_profile(request):
    user = request.user
    try:
        profile = UserDetails.objects.get(user=user)
        data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "manager_id": profile.manager.id if profile.manager else None
        }
        return JsonResponse(data, safe=False)
    except UserDetails.DoesNotExist:
        return JsonResponse({"error": "Profile not found"}, status=404)
