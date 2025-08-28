from rest_framework import serializers
from users.models.referral import Referral

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = [
            'id', 'referrer', 'full_name', 'email', 'phone',
            'position', 'notes', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'referrer', 'status', 'created_at']
