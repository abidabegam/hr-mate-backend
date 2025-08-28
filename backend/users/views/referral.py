from rest_framework import generics, permissions
from users.models.referral import Referral
from users.serializers.referral import ReferralSerializer

class MyReferralsView(generics.ListAPIView):
    serializer_class = ReferralSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Referral.objects.filter(referrer=self.request.user).order_by('-created_at')


class SubmitReferralView(generics.CreateAPIView):
    serializer_class = ReferralSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(referrer=self.request.user)
