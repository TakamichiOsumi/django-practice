from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from .models import Post
from accounts.models import CustomUser

# Create your tests here.
class TimelineTestCase(TestCase):

    def test_index(self):
        client = Client()
        self.test_user = get_user_model().objects._create_user(
            username = 'testuser_foo',
            email = 'testuser_foo@example.com',
            password = 'password_foo')
        client.login(username = 'testuser_foo', password = 'password_foo')
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
