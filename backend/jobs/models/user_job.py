# backend/jobs/models/user_job.py

from django.db import models
from django.conf import settings
from .job import Job

class UserJob(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    pay = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    start_date = models.DateField(null=True, blank=True)  # ✅ Confirmed field name
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.job.title} ({self.status})"
