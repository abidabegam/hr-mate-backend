from django.db import models
from django.utils import timezone
from django.conf import settings


class RegistrationRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registration_requests'
    )
    posted_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"RegistrationRequest for {self.user.email}"
