import os
from django.http import HttpResponse, Http404
from django.conf import settings
from jobs.models import JobApplication

def download_resume(request, app_id):
    try:
        application = JobApplication.objects.get(id=app_id)
        resume_path = application.resume.path
        if not os.path.exists(resume_path):
            raise Http404("Resume not found.")

        with open(resume_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(resume_path)}"'
            return response

    except JobApplication.DoesNotExist:
        raise Http404("Application not found.")
