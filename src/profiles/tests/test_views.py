from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class ShowUserProfileViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='john', email='john@mail.com', password='John1234')

    def setUp(self):
        self.client.login(username='john', password='John1234')

    def test_view_url_exists(self):
        response = self.client.get('/john')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('show-user-profile', kwargs={'username': 'john'}))
        self.assertEqual(response.status_code, 200)

    
    # def test_unauthenticated_user_can_not_access_any_user_profile(self):
    #     response = self.client.get(f'/{self.username}')
    #     self.assertRedirects(response, '/')
