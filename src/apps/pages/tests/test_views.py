from django.test import TestCase
from django.urls import reverse

from tests.data import MALE_USER, SUPER_USER

from pages.apps import PagesConfig


class IndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        MALE_USER.create()
        SUPER_USER.create()
        cls.url = reverse(PagesConfig.INDEX_URL)
        cls.auth_header = 'pages/includes/auth-header.html'
        cls.anon_header = 'pages/includes/anon-header.html'

    def test_anonymous_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_authenticated_request(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_anonymous_request_header(self):
        self.assertTemplateUsed(self.client.get(self.url), self.anon_header)

    def test_authenticated_request_header(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, self.auth_header)
        self.assertNotContains(response, 'Администрация')

    def test_superuser_request_header(self):
        self.client.login(username=SUPER_USER.username, password=SUPER_USER.password)
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, self.auth_header)
        self.assertContains(response, 'Администрация')


class ReferencesViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(PagesConfig.REFERENCES_URL)
        MALE_USER.create()

    def test_anonymous_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_authenticated_request(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)
