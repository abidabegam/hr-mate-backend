from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from users.auth import login_for_test, logout_for_test
from ..models import User, RegistrationRequest
from ..auth import JwtTools


class TestRegisterView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.reg_request = RegistrationRequest.objects.create(email='email@email.com')
        cls.user_data = {'email': 'email@email.com', 'first_name': 'first',
                     'last_name': 'last', 'password': 'bestPW88!'}

    def test_post_success(self) -> None:
        url = reverse('register', kwargs={'code': self.reg_request.code})
        response = self.client.post(url, data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.cookies[settings.JWT['AUTH_COOKIE']])

    def test_post_fail_wrongcode(self) -> None:
        url = reverse('register', kwargs={'code': 'wrong'})
        response = self.client.post(url, data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_fail_wrongemail(self) -> None:
        url = reverse('register', kwargs={'code': self.reg_request.code})
        bad_data = {'email': 'wrong@email.com', 'first_name': 'first',
                     'last_name': 'last', 'password': 'bestPW88!'}
        response = self.client.post(url, data=bad_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class TestLoginView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(email='email@email.com', first_name='first',
                                            last_name='last', password='bestPW88!')
        cls.post_url = reverse('login')

    def test_post_success(self) -> None:
        login_data = {'email': 'email@email.com', 'password': 'bestPW88!'}
        response = self.client.post(self.post_url, data=login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.cookies[settings.JWT['AUTH_COOKIE']])

    def test_post_user_not_found(self) -> None:
        login_data = {'email': 'NOTemail@email.com', 'password': 'bestPW88!'}
        response = self.client.post(self.post_url, data=login_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNone(response.cookies.get(
            settings.JWT['AUTH_COOKIE'], None))

    def test_post_wrong_password(self) -> None:
        login_data = {'email': 'email@email.com', 'password': 'Hello'}
        response = self.client.post(self.post_url, data=login_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNone(response.cookies.get(
            settings.JWT['AUTH_COOKIE'], None))


class TestUserView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(email='email@email.com', first_name='first',
                                            last_name='last', password='bestPW88!')
        cls.get_url = reverse('whoami')

    def test_get_success(self) -> None:
        token = JwtTools.gen_token(self.user.id)
        self.client.cookies[
            settings.JWT['AUTH_COOKIE']] = token
        response = self.client.get(self.get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_no_token(self) -> None:
        response = self.client.get(self.get_url)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_token(self) -> None:
        self.client.cookies[
            settings.JWT['AUTH_COOKIE']] = "not cool"
        response = self.client.get(self.get_url)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)


class TestLogoutView(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='email@email.com', first_name='first',
                                             last_name='last', password='bestPW88!')

    def test_post_success(self) -> None:
        token = JwtTools.gen_token(self.user.id)
        self.client.cookies[
            settings.JWT['AUTH_COOKIE']] = token

        url = reverse('logout')
        response = self.client.post(url)
        delete_cookie = response.cookies.get(settings.JWT['AUTH_COOKIE'])
        self.assertIsNotNone(delete_cookie)
        self.assertEqual(delete_cookie.value, '')


class TestRegistrationRequestViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.reg_request = RegistrationRequest.objects.create(email='new@gmail.com')
        cls.list_url = reverse('registrationrequest-list')
        cls.detail_url = reverse('registrationrequest-detail', args=[cls.reg_request.code])
    
    def setUp(self):
        self.user = login_for_test(self.client)

    def test_permissions_unauthorized(self):
        logout_for_test(self.client)

        response = self.client.post(self.list_url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_success(self):
        email = f'new{self.user.email}'
        data = {'email': email}
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], email)

    def test_create_failure(self):
        response = self.client.post(self.list_url, data={'email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('code', response.data[0])

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], self.reg_request.code)

    def test_delete(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RegistrationRequest.objects.filter(code=self.reg_request.code).exists())
    
    
    
    