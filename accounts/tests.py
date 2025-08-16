from django.contrib.auth import get_user_model
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from accounts.models import CustomUser, Connection
from config.settings import AXES_FAILURE_LIMIT
import time

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
        auth_info = { 'username': 'invalid_user',
                      'password': 'invalid_password' }
        # Login attemps before the account lockout
        for i in range(AXES_FAILURE_LIMIT - 1):
            response = client.post(login_url, auth_info)
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

    @override_settings(AXES_ENABLED = False,
                       AUTO_LOGOUT = { 'IDLE_TIME': 2 })
    def test_auto_logout(self):
        client = Client()
        test_user = self.gen_user('testuser2',
                                  'testpassword2')
        client.login(username = 'testuser2',
                     password = 'testpassword2')
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check if the response includes the link of new post or not.
        self.assertTrue(response.content.find(b'Post something new') >= 0)

        # Cause the timeout
        time.sleep(3)
        response = client.get('/', follow = True)
        self.assertTrue(response.content.find(b'Login') >= 0)

    @override_settings(AXES_ENABLED = False)
    def test_following_and_followed_status(self):
        # Set up three login users.
        clients = []
        users = []
        for i in range(4):
            clients.append(Client())
            user = f'testuser_{i}'
            password = f'testpassword_{i}'
            users.append(self.gen_user(user, password))
            clients[i].login(username = user, password = password)

        # Build follow relationship
        clients[0].post(reverse('accounts:detail', args=[ users[1].id ]))
        clients[0].post(reverse('accounts:detail', args=[ users[2].id ]))
        clients[1].post(reverse('accounts:detail', args=[ users[2].id ]))
        clients[2].post(reverse('accounts:detail', args=[ users[0].id ]))
        clients[3].post(reverse('accounts:detail', args=[ users[2].id ]))

        conns = Connection.objects.all()
        self.assertTrue(conns.count() == 5)
        self.assertTrue(conns.filter(following_id = users[0].id).count() == 2)
        self.assertTrue(conns.filter(followed_id  = users[0].id).count() == 1)
        self.assertTrue(conns.filter(following_id = users[1].id).count() == 1)
        self.assertTrue(conns.filter(followed_id  = users[1].id).count() == 1)
        self.assertTrue(conns.filter(following_id = users[2].id).count() == 1)
        self.assertTrue(conns.filter(followed_id  = users[2].id).count() == 3)
        self.assertTrue(conns.filter(following_id = users[3].id).count() == 1)
        self.assertTrue(conns.filter(followed_id  = users[3].id).count() == 0)
