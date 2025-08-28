from django.test import TestCase
from ..models import User, get_sentinel_user, UserDetails, generate_random_code, RegistrationRequest


class TestUserManager(TestCase):
    def test_create_user_success(self) -> None:
        user = User.objects.create_user(
            email='email@email.com')
        self.assertTrue(isinstance(user, User))

    def test_create_user_invalid_email(self) -> None:
        self.assertRaises(
            ValueError,
            lambda: User.objects.create_user(email=None)
        )

    def test_create_superuser_success(self) -> None:
        superuser = User.objects.create_superuser(
            email='email@email.com')
        self.assertTrue(isinstance(superuser, User))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_is_staff_false(self) -> None:
        self.assertRaises(
            ValueError,
            lambda: User.objects.create_superuser(
                email='email@email.com', is_staff=False)
        )

    def test_create_superuser_is_superuser_false(self) -> None:
        self.assertRaises(
            ValueError,
            lambda: User.objects.create_superuser(
                email='email@email.com', is_superuser=False)
        )


class TestGetSentinelUser(TestCase):
    def test_get_sentinel_user_gets_user(self):
        sentinel_user = get_sentinel_user()
        self.assertIsInstance(sentinel_user, User)
        self.assertEqual(sentinel_user.email, 'deleted@deleted.com')


class TestUserDetails(TestCase):
    def test__str___returns_str(self):
        user = User(first_name='first', last_name='name',
                    email='email@email.com')
        user_details = UserDetails(user=user)
        self.assertEqual(str(user_details), 'email@email.com')

class TestGenerateRandomCode(TestCase):
    def test_generate_random_code_success(self):
        length = 10
        rand_str = generate_random_code(length)
        self.assertIsInstance(rand_str, str)
        self.assertEqual(len(rand_str), length)


class TestRegistrationRequest(TestCase):
    def test___str___returns_str(self):
        email = 'hey@gmail.com'
        reg_request = RegistrationRequest(email=email)
        rep = str(reg_request)
        self.assertIsInstance(rep, str)
        self.assertEqual(rep, f'{reg_request.email} @{reg_request.created_at}')
