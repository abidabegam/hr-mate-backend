from django.db import models
from django.conf import settings

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages'
    )
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # ✅ NEW FIELD
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.email} ➜ {self.recipient.email}: {self.text[:30]}"
