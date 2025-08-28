from rest_framework import serializers
from users.models.message import Message
from users.serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)  # ✅ Full recipient object
    recipient_id = serializers.IntegerField(write_only=True)
    is_read = serializers.BooleanField(read_only=False, required=False)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'recipient_id',  # used when sending
            'recipient',     # used when displaying
            'text',
            'timestamp',
            'is_read',
        ]
        read_only_fields = ['id', 'timestamp', 'sender']
