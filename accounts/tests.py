from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from accounts.models import CustomUser

from config.settings import AXES_FAILURE_LIMIT

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

    def test_brute_force_attacks(self):
        client = Client()
        login_url = reverse('accounts:login')
        auth_info = {'username': 'invalid_user',
                     'password': 'invalid_password' }
        # Login attemps before the account lockout
        for i in range(AXES_FAILURE_LIMIT - 1):
            response = self.client.post(login_url, auth_info)
            self.assertEqual(response.content.find(b'Account Lockout'), -1)
        # Trigger the account lockout by one more login failure
        response = self.client.post(login_url, auth_info)
        self.assertTrue(response.content.find(b'Account Lockout') >= 0)

    @override_settings(AXES_ENABLED = False)
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
