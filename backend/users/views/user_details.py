from rest_framework import viewsets, permissions, generics
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from users.models import UserDetails
from users.serializers.user_details import UserDetailsSerializer

# Standard CRUD for the logged-in user’s details
class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset = UserDetails.objects.select_related('user', 'manager', 'job')
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]


# Admin + HR can view any user; employee can view own profile only
class UserDetailsByUserIdView(generics.RetrieveAPIView):
    """
    GET /api/users/user-details/by-user/<user_id>/
    """
    queryset = UserDetails.objects.select_related('user', 'manager', 'job')
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'

    def get_object(self):
        user_id = int(self.kwargs.get("user_id"))

        # Allow ADMIN or HR to access any profile
        if self.request.user.role in ["ADMIN", "HR"]:
            return self.queryset.get(user__id=user_id)

        # Allow EMPLOYEE to access their own profile
        if self.request.user.id == user_id:
            return self.queryset.get(user__id=user_id)

        # Deny access to others
        raise PermissionDenied("You do not have permission to view this profile.")


# Admin: list all user details
class AllUserDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserDetails.objects.select_related('user', 'manager', 'job')
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAdminUser]


# Employee: get *this* user’s job details
class MyJobDetailsView(generics.RetrieveAPIView):
    """
    GET /api/users/job-details/me/
    """
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return UserDetails.objects \
                .select_related('job', 'manager') \
                .get(user=self.request.user)
        except UserDetails.DoesNotExist:
            raise NotFound("No job details found for this user.")
