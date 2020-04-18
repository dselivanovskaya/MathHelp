from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

JOHN_USERNAME = 'john'
JOHN_EMAIL = 'john@gmail.com'
JOHN_PASSWORD = 'John_123'


class GetProfileViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = '/profile'
        cls.name = 'profile'
        cls.template = 'profile/profile.html'
        User.objects.create_user(
            username=JOHN_USERNAME, email=JOHN_EMAIL, password=JOHN_PASSWORD
        )

    def test_view_url_exists_for_authenticated_users(self):
        self.client.login(username=JOHN_USERNAME, password=JOHN_PASSWORD)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_view_url_accessible_by_name_for_authenticated_users(self):
        self.client.login(username=JOHN_USERNAME, password=JOHN_PASSWORD)
        response = self.client.get(reverse(self.name))
        self.assertEqual(response.status_code, 200)

    def test_view_renders_correct_template_for_authenticated_users(self):
        self.client.login(username=JOHN_USERNAME, password=JOHN_PASSWORD)
        self.assertTemplateUsed(self.client.get(self.url), self.template)

    def test_redirects_unauthenticated_user_to_login_page(self):
        self.assertRedirects(self.client.get(self.url), '/sign-in')


class UpdateProfileViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = '/profile/edit'
        cls.name = 'edit-profile'
        cls.template = 'profile/edit-profile.html'
        User.objects.create_user(
            username=JOHN_USERNAME, email=JOHN_EMAIL, password=JOHN_PASSWORD
        )

    def test_view_url_exists_for_authenticated_users(self):
        self.client.login(username=JOHN_USERNAME, password=JOHN_PASSWORD)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_view_url_accessible_by_name_for_authenticated_users(self):
        self.client.login(username=JOHN_USERNAME, password=JOHN_PASSWORD)
        response = self.client.get(reverse(self.name))
        self.assertEqual(response.status_code, 200)

    def test_view_renders_correct_template_for_authenticated_users(self):
        self.client.login(username=JOHN_USERNAME, password=JOHN_PASSWORD)
        self.assertTemplateUsed(self.client.get(self.url), self.template)

    def test_redirects_unauthenticated_user_to_login_page(self):
        self.assertRedirects(self.client.get(self.url), '/sign-in')


class DeleteProfileViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = '/profile/delete'
        cls.name = 'delete-profile'
        User.objects.create_user(
            username=JOHN_USERNAME, email=JOHN_EMAIL, password=JOHN_PASSWORD
        )

    def test_redirects_unauthenticated_user_to_login_page(self):
        self.assertRedirects(self.client.get(self.url), '/sign-in')
