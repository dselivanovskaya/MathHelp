from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class GetUserProfileViewTest(TestCase):

    JOHN_USERNAME = 'john'
    JOHN_EMAIL = 'john@gmail.com'
    JOHN_PASSWORD = 'John_123'

    @classmethod
    def setUpTestData(cls):
        cls.url = f'/{cls.JOHN_USERNAME}/'
        cls.name = 'user-profile'
        cls.template = 'profiles/user-profile.html'
        User.objects.create_user(
            username=cls.JOHN_USERNAME,
            email=cls.JOHN_EMAIL,
            password=cls.JOHN_PASSWORD
        )

    def test_view_url_exists_for_authenticated_users(self):
        self.client.login(username=self.JOHN_USERNAME, password=self.JOHN_PASSWORD)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_view_url_accessible_by_name_for_authenticated_users(self):
        self.client.login(username=self.JOHN_USERNAME, password=self.JOHN_PASSWORD)
        response = self.client.get(
            reverse('user-profile', args=[self.JOHN_USERNAME])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_renders_correct_template_for_authenticated_users(self):
        self.client.login(username=self.JOHN_USERNAME, password=self.JOHN_PASSWORD)
        self.assertTemplateUsed(self.client.get(self.url), self.template)

    def test_redirects_unauthenticated_user_to_login_page(self):
        self.assertRedirects(self.client.get(self.url), '/login/')

    def test_redirects_home_authenticated_user_trying_to_access_other_user_profile(self):
        self.client.login(username=self.JOHN_USERNAME, password=self.JOHN_PASSWORD)
        self.assertRedirects(self.client.get('/alice/'), '/')
