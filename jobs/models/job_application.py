from django.db import models
from .job import Job

class JobApplication(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)

    # ✅ New fields
    location = models.CharField(max_length=100, blank=True, null=True)
    experience = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    current_company = models.CharField(max_length=100, blank=True, null=True)
    expected_salary = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications', null=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    cover_letter = models.TextField(blank=True)
    is_employee = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("shortlisted", "Shortlisted"),
            ("interview", "Interview"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )
    admin_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job.title if self.job else 'No Job'}"
