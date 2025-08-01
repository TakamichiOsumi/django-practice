from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from accounts.models import CustomUser

# Create your tests here.
class AccountsTestCase(TestCase):

    def gen_user(self, username, password, email = None):
        test_user = get_user_model().objects._create_user(
            username = username,
            email = email,
            password = password)
        return test_user

    def test_timeline_index_without_login(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_timeline_login_and_logout(self):
        client = Client()
        test_user = self.gen_user('testuser',
                                  'testpassword')
        client.login(username = 'testuser',
                     password = 'testpassword')
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        # Test the deprecation of GET method of LogoutView.
        # The current logout is implemented by POST method.
        response = client.logout()
        response = client.post('/accounts/logout/')
        self.assertEqual(response.status_code, 302)
