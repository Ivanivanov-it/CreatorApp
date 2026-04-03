from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthTest(TestCase):
    def setUp(self):
        UserModel = get_user_model()
        self.user = UserModel.objects.create_user(username='test',password="password123")

    def test_login_with_correct_credentials(self):

        response = self.client.post(reverse('account:login'),{
            'username': 'test',
            'password': 'password123'
        })

        self.assertEqual(response.status_code, 302)

    def test_login_with_wrong_credentials(self):
        response = self.client.post(reverse('account:login'), {
            'username': 'test',
            'password': 'password12'
        })

        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username='test', password='password12')
        response = self.client.post(reverse('account:logout'))
        self.assertEqual(response.status_code, 302)
