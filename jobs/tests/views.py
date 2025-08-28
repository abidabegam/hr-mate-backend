from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.auth import login_for_test, logout_for_test
from .. import models
from users.models import User

class TestJobViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.job = models.Job.objects.create(title='title', description='description')
        cls.list_url = reverse('job-list')
        cls.detail_url = reverse('job-detail', args=[cls.job.id]) 

    def setUp(self) -> None:
        self.user = login_for_test(self.client)
        self.data = {'title': 't', 'description': 'd'}

    def test_permissions_unathenticated(self):
        logout_for_test(self.client)
        
        response = self.client.post(self.list_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(self.detail_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(self.detail_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create(self) -> None:
        response = self.client.post(self.list_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.data['title'])

    def test_list(self) -> None:
        models.Job.objects.create(title='title', description='description', is_posted=False)
        models.Job.objects.create(title='title', description='description', is_posted=False)
        models.Job.objects.create(title='title', description='description', is_posted=True)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        logout_for_test(self.client)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for job in response.data :
            self.assertTrue(job['is_posted'])

    def test_retrieve(self) -> None:
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.job.title)

    def test_update(self) -> None:
        response = self.client.put(self.detail_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['title'], self.data['title'])
        self.assertEqual(response.data['description'], self.data['description'])

    def test_partial_update(self) -> None:
        response = self.client.patch(self.detail_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.data['title'])
        self.assertEqual(response.data['description'], self.data['description'])

    def test_delete(self) -> None:
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Job.objects.filter(id=self.job.id).exists())


class TestJobApplicationViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.job = models.Job.objects.create(title='title', description='description', is_posted=True)
        cls.data = {'email': 'email@email.com', 'first_name': 'first', 
                    'last_name': 'last'}
        cls.job_app = models.JobApplication.objects.create(**cls.data, job = cls.job)
        cls.data['job'] = cls.job.id
        cls.list_url = reverse('jobapplication-list')
        cls.detail_url = reverse('jobapplication-detail', args=[cls.job_app.id]) 

    def setUp(self) -> None:
        self.user = login_for_test(self.client)

    def test_permissions_unathenticated(self):
        logout_for_test(self.client)
        
        response = self.client.post(self.list_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(self.detail_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(self.detail_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create(self) -> None:
        response = self.client.post(self.list_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list(self) -> None:
        job2 = models.Job.objects.create(title='title', description='description', is_posted=True)
        self.data.pop('job')
        models.JobApplication.objects.create(**self.data, job = self.job)
        models.JobApplication.objects.create(**self.data, job = job2)
        models.JobApplication.objects.create(**self.data, job = job2)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        response = self.client.get(self.list_url + f'?job={job2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for job_app in response.data :
            self.assertEqual(job_app['job'], job2.id)

    def test_retrieve(self) -> None:
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.job_app.id)

    def test_update(self) -> None:
        response = self.client.put(self.detail_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update(self) -> None:
        response = self.client.patch(self.detail_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self) -> None:
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.JobApplication.objects.filter(id=self.job_app.id).exists())
 

class TestUserJobViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.job = models.Job.objects.create(title='title', description='description')
        cls.user = User.objects.create_user(email='email@test.com', first_name='first',
                                            last_name='last', password='test33!')
        cls.user_job = models.UserJob.objects.create(job=cls.job, user=cls.user)
        cls.list_url = reverse('userjob-list')
        cls.detail_url = reverse('userjob-detail', args=[cls.user_job.id]) 

    def setUp(self) -> None:
        login_for_test(self.client)
        self.data = {'job': self.job.id, 'user': self.user.id, 'pay': 2}

    def test_permissions_unathenticated(self):
        logout_for_test(self.client)
        
        response = self.client.post(self.list_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.put(self.detail_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(self.detail_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create(self) -> None:
        response = self.client.post(self.list_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list(self) -> None:
        job2 = models.Job.objects.create(title='title', description='description')
        user2 = User.objects.create_user(email='email2@test.com', first_name='first2',
                                            last_name='last2', password='test33!')
        self.data.pop('job')
        self.data.pop('user')
        models.UserJob.objects.create(**self.data, job=self.job, user=user2)
        models.UserJob.objects.create(**self.data, job=job2, user=self.user)
        models.UserJob.objects.create(**self.data, job=job2, user=user2)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        response = self.client.get(self.list_url + f'?job={job2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for user_job in response.data :
            self.assertEqual(user_job['job'], job2.id)

        response = self.client.get(self.list_url + f'?user={user2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        for user_job in response.data :
            self.assertEqual(user_job['user'], user2.id)

        response = self.client.get(self.list_url + f'?job={job2.id}&user={user2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        user_job = response.data[0]
        self.assertEqual(user_job['job'], job2.id)
        self.assertEqual(user_job['user'], user2.id)

    def test_retrieve(self) -> None:
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user_job.id)

    def test_update(self) -> None:
        self.data['pay'] += 1
        response = self.client.put(self.detail_url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pay'], self.data['pay'])

    def test_partial_update(self) -> None:
        data = {'pay': self.data['pay'] + 1}
        response = self.client.patch(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pay'], data['pay'])

    def test_delete(self) -> None:
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.UserJob.objects.filter(id=self.user_job.id).exists())