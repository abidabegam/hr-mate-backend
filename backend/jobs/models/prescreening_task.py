from django.db import models
from .job_application import JobApplication  # adjust import if needed

class PrescreeningTask(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='prescreening_tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='prescreening/', null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('assigned', 'Assigned'),
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
    ], default='assigned')
    submitted_file = models.FileField(upload_to='prescreening/submissions/', null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.application.email})"

    def get_job_title(self):
        if self.application and self.application.job:
            return self.application.job.title
        return "-"
    get_job_title.short_description = "Job"
