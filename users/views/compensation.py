# backend/users/views/compensation.py

from rest_framework import generics, permissions
from users.serializers.user_details import UserDetailsSerializer
from users.models.user_details import UserDetails
from rest_framework.exceptions import NotFound

class MyCompensationView(generics.RetrieveAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return UserDetails.objects.get(user=self.request.user)
        except UserDetails.DoesNotExist:
            raise NotFound("User compensation info not found.")
