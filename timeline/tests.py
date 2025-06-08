from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from .models import Post
from accounts.models import CustomUser

# Create your tests here.
class TimelineTestCase(TestCase):

    def gen_user(self, username, password, email):
        test_user = get_user_model().objects._create_user(
            username = username,
            email = email,
            password = password)
        return test_user

    def test_timeline_index_without_login(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_timeline_index_with_login(self):
        client = Client()
        test_user = self.gen_user('testuser_foo',
                                  'password_foo_123',
                                  'testuser_foo@example.com')
        client.login(username = 'testuser_foo',
                     password = 'password_foo_123')
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_timeline_post(self):
        client = Client()
        test_user = self.gen_user('testuser_foo',
                                  'password_foo_123',
                                  'testuser_foo@example.com')
        client.login(username = 'testuser_foo',
                     password = 'password_foo_123')
        client.post('/create/', { 'text' : 'Hello World', 'photo': ''})
        latest_post = Post.objects.latest('created_at')
        self.assertEqual(latest_post.text, 'Hello World')
