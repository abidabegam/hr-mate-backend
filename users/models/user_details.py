from django.db import models
from django.conf import settings
from jobs.models import Job

class UserDetails(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="details"
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="team_members"
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    department     = models.CharField(max_length=100, blank=True)
    job_title      = models.CharField(max_length=100, blank=True)
    location       = models.CharField(max_length=100, blank=True)

    # Compensation fields
    salary         = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    bonus          = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    stock_options  = models.PositiveIntegerField(default=0)
    updated_at     = models.DateTimeField(auto_now=True)

    phone          = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(
        upload_to="profiles/",
        null=True,
        blank=True
    )
    approved       = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Details for {self.user.email}"
