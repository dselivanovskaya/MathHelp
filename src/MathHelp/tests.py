from django.test import Client, TestCase

from django.contrib.auth.models import User


class LoginTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username = 'john', 
        email = 'john@mail.ru', password = 'knowledge2000')
        self.user.save()
        print(self.user)

    def test_login_url_exists(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_url_redirects_to_user_profile(self):
        response = self.client.post('/login/',
                    {
                     'username': self.user.username,
                     'password': 'knowledge2000'
                     })
        self.assertRedirects(response, '/john')

class LogoutTestCase(TestCase):
    
    def test_logout_url_redirects_to_home_page(self):
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/')