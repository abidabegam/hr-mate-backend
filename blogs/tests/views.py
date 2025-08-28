from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from ..models import BlogPost


class TestBlogPostViewSet(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='email@email.com', first_name='first',
                                             last_name='last', password='bestPW88!')
        self.client.force_authenticate(user=self.user)

    def test_perform_create_post_success(self) -> None:
        url = reverse('blogpost-list')
        data = {'title': 'new here!', 'content': 'hello'}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_post = BlogPost.objects.first()
        self.assertEqual(new_post.author, self.user)
