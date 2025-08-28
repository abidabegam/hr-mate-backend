from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from users.models.message import Message
from users.serializers.message import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        # ✅ Allow marking messages as read
        instance = self.get_object()

        if instance.recipient != request.user:
            return Response({"detail": "You are not authorized to update this message."},
                            status=status.HTTP_403_FORBIDDEN)

        is_read = request.data.get("is_read", None)
        if is_read is not None:
            instance.is_read = is_read
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return Response({"detail": "Nothing to update."}, status=status.HTTP_400_BAD_REQUEST)
