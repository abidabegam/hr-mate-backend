from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
import csv

from .models.job import Job
from .models.job_application import JobApplication
from .models.user_job import UserJob
from .models.prescreening_task import PrescreeningTask


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'company', 'description', 'department','location', 'is_posted', 'posted_at', 'created_at']
    list_display_links = ['title']  # ✅ this line makes the title clickable
    search_fields = ['title', 'company', 'description', 'department','location']
    ordering = ['-posted_at']
    list_filter = ['is_posted', 'posted_at']


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'email', 'phone_number', 'location', 'experience',
        'linkedin', 'current_company', 'expected_salary', 'start_date',
        'job', 'is_employee', 'created_at'
    )
    search_fields = ['first_name', 'last_name', 'email', 'job__title', 'location', 'current_company']
    list_filter = ['job', 'is_employee', 'created_at']
    ordering = ['-created_at']
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=job_applications.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export selected applications to CSV"


@admin.register(UserJob)
class UserJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'job', 'pay', 'start_date', 'end_date']
    search_fields = ['user__email', 'job__title']
    list_filter = ['status', 'start_date', 'end_date']


@admin.register(PrescreeningTask)
class PrescreeningTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_job_title', 'title', 'status', 'created_at']
    search_fields = ['title']
    list_filter = ['status']
