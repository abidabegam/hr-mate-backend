from django.test import TestCase
from .. import models
from users.models import User


class TestJob(TestCase):
    def test__str___returns_str(self) -> None:
        job = models.Job(
            title='title', description='description')
        self.assertEqual(str(job), 'title')

    def test_save_create_not_posted(self) -> None:
        job = models.Job(title='t', description='d', is_posted=False)
        job.save()
        self.assertIsNotNone(job.created_at)
        self.assertIsNone(job.posted_at)

    def test_save_create_is_posted(self) -> None:
        job = models.Job(title='t', description='d', is_posted=True)
        job.save()
        self.assertIsNotNone(job.created_at)
        self.assertEqual(job.created_at, job.posted_at)

    def test_save_update_newly_posted(self) -> None:
        job = models.Job(title='t', description='d', is_posted=False)
        job.save()

        job.is_posted = True
        job.save()
        self.assertIsNotNone(job.posted_at)
        self.assertNotEqual(job.created_at, job.posted_at)

        posted_at = job.posted_at
        job.is_posted = False
        job.save()
        self.assertEqual(job.posted_at, posted_at)

        posted_at = job.posted_at
        job.is_posted = True
        job.save()
        self.assertIsNotNone(job.posted_at)
        self.assertNotEqual(job.posted_at, posted_at)

    def test_save_update_not_newly_posted(self) -> None:
        job = models.Job(title='t', description='d', is_posted=True)
        job.save()
        posted_at = job.posted_at

        job.is_posted = True
        job.save()
        self.assertEqual(job.posted_at, posted_at)

        job.is_posted = False
        job.save()
        self.assertEqual(job.posted_at, posted_at)

        job.is_posted = False
        job.save()
        self.assertEqual(job.posted_at, posted_at)


class TestUserJob(TestCase):
    def test__str___returns_str(self) -> None:
        user = User(first_name='first', last_name='name',
                    email='email@email.com')
        job = models.Job(
            title='title', description='description')
        user_job = models.UserJob(user=user, job=job)
        self.assertEqual(str(user_job), '(email@email.com, title)')


class TestJobApplication(TestCase):
    def test__str___returns_str(self) -> None:
        job = models.Job(
            title='title', description='description')
        job_application = models.JobApplication(
            job=job, email='email@email.com', first_name='first', last_name='last')
        self.assertEqual(str(job_application),
                         f'(email@email.com, title, {job_application.created_at})')
