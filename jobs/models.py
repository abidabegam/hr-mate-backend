from django.db import models
from django.utils import timezone
from users.models import User


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, default="American Technology Initiative")
    description = models.TextField()
    location = models.CharField(max_length=255, null=True, blank=True)
    base_pay_low = models.FloatField(null=True, blank=True)
    base_pay_high = models.FloatField(null=True, blank=True)
    is_hourly_pay = models.BooleanField(default=False)
    posted_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_posted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} at {self.company}"


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    resume = models.FileField(upload_to="resumes/")
    is_employee = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # ✅ NEW
    admin_notes = models.TextField(blank=True, null=True)  # ✅ NEW
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job.title}"


class UserJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_assignments")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="assigned_users")
    pay = models.FloatField()
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.job.title}"


class RegistrationRequest(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    code = models.CharField(max_length=64)
    company = models.CharField(max_length=255, default="American Technology Initiative")
    created_at = models.DateTimeField(auto_now_add=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
