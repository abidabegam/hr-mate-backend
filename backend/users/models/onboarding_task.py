# backend/users/models/onboarding_task.py

from django.db import models
from django.conf import settings

class OnboardingTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # ✅ NEW
    due_date = models.DateField(blank=True, null=True)     # ✅ NEW
    completed = models.BooleanField(default=False)
    uploaded_document = models.FileField(upload_to='onboarding_docs/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({'Done' if self.completed else 'Pending'})"
