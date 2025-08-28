from django.test import TestCase
from ..models import BlogPost
from users.models import User

# Create your tests here.


class TestBlogPost(TestCase):
    def test__str___returns_str(self) -> None:
        user = User(first_name='first', last_name='name',
                    email='email@email.com')
        blog_post = BlogPost(
            title='title', content='content', author=user)
        self.assertEqual(str(blog_post), 'title by email@email.com')
