from django.contrib.auth import get_user_model
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from .models import Post, Like
from accounts.models import CustomUser
from django.http import HttpRequest

# Create your tests here.
class TimelineTestCase(TestCase):

    def gen_user(self, username, password, email = None):
        test_user = get_user_model().objects._create_user(
            username = username,
            email = email,
            password = password)
        return test_user

    @override_settings(AXES_ENABLED = False)
    def test_timeline_post(self):
        client = Client()
        test_user = self.gen_user('testuser',
                                  'testpassword')
        client.login(username = 'testuser',
                     password = 'testpassword')
        client.post('/create/', { 'text' : 'Hello World', 'photo': ''})
        latest_post = Post.objects.latest('created_at')
        self.assertEqual(latest_post.text, 'Hello World')

    @override_settings(AXES_ENABLED = False)
    def test_global_timeline(self):
        # Set up two login users.
        clients = []
        test_users = []
        for idx in range(2):
            clients.append(Client())
            user = f'testuser_{idx}'
            password = f'testpassword_{idx}'
            test_users.append(self.gen_user(user, password))
            clients[idx].login(username = user, password = password)

        # One user posts two short messages.
        clients[0].post('/create/', { 'text' : 'This is the first message', 'photo': ''})
        latest_post = Post.objects.latest('created_at')
        clients[0].post('/create/', { 'text' : 'This is the second message', 'photo': ''})

        # The other user can see the posted messages.
        response = clients[1].get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find(b'This is the first message') >= 0)
        self.assertTrue(response.content.find(b'This is the second message') >= 0)

        # The user who posted it deletes the first message.
        response = clients[0].post(reverse('timeline:delete',
                                           kwargs = { 'pk' : latest_post.pk }))

        # Now, the other user cannot find the first message.
        # On the other hand, she can get the second one which isn't deleted.
        response = clients[1].get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.find(b'This is the first message'), -1)
        self.assertTrue(response.content.find(b'This is the second message') >= 0)

        # Add a test for the Like feature.
        left_post = Post.objects.latest('created_at')
        like = Like.objects.filter(user = test_users[1])
        self.assertEqual(like.count(), 0)
        response = clients[1].post(reverse('timeline:like',
                                           kwargs = { 'pk' : left_post.pk }))
        like = Like.objects.filter(user = test_users[1])
        self.assertEqual(like.count(), 1)
        self.assertEqual(like.get().post.id, left_post.id)
