# backend/jobs/models/job.py
from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255, null=True, blank=True)  # allow nulls
    location = models.CharField(max_length=255, null=True, blank=True)  # allow nulls
    salary = models.IntegerField(null=True, blank=True)  # ✅ New
    experience = models.IntegerField(null=True, blank=True)  # ✅ New
    department = models.CharField(max_length=100, null=True, blank=True)  # ✅ Add
    is_posted = models.BooleanField(default=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
