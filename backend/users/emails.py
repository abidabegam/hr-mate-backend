from django.core.mail import send_mail
from django.conf import settings
from users.models.onboarding_task import OnboardingTask

APP_NAME = getattr(settings, 'APP_NAME', 'WorkMate')
URL = getattr(settings, 'WEB_URL', 'http://localhost:3000')

class UserEmails:

    @staticmethod
    def send_welcome_email(email: str, first_name: str, last_name: str) -> None:
        send_mail(
            f'Welcome to {APP_NAME}',
            f'Hello {first_name} {last_name},\n\n'
            f'Thank you for signing up for {APP_NAME}.\n\nSincerely,\nThe {APP_NAME} Team',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=True
        )

    @staticmethod
    def send_registration_request_email(email: str, code: str) -> None:
        send_mail(
            f'{APP_NAME} Registration Request',
            f'Hello {email},\n\n'
            f'You have been requested to register for a {APP_NAME} account with us.'
            f'\n\nPlease use this link to bring you to the registration page:'
            f'\n\n{URL}/register/{code}'
            f'\n\nSincerely,\nThe {APP_NAME} Team',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=True
        )

    @staticmethod
    def send_onboarding_task_email(task: OnboardingTask) -> None:
        user = task.user
        subject = f"New Onboarding Task Assigned - {APP_NAME}"
        message = (
            f"Hello {user.first_name},\n\n"
            f"You have been assigned a new onboarding task:\n\n"
            f"Title: {task.title}\n"
            f"Due Date: N/A\n\n"
            f"Please log in to the {APP_NAME} portal to complete it.\n\n"
            f"- The {APP_NAME} Team"
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
