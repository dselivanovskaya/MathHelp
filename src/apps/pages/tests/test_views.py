from django.test import TestCase
from django.urls import reverse

from tests.data import USER1, ADMIN

from pages.apps import PagesConfig


class IndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(PagesConfig.INDEX_URL)
        cls.auth_header = 'pages/includes/auth-header.html'
        cls.anon_header = 'pages/includes/anon-header.html'
        USER1.create_in_db()
        ADMIN.create_in_db()

    def test_anonymous_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_authenticated_request(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_anonymous_request_header(self):
        self.assertTemplateUsed(self.client.get(self.url), self.anon_header)

    def test_authenticated_request_header(self):
        self.client.login(username=USER1.username, password=USER1.password)
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, self.auth_header)
        self.assertNotContains(response, 'Администрация')

    def test_superuser_request_header(self):
        self.client.login(username=ADMIN.username, password=ADMIN.password)
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, self.auth_header)
        self.assertContains(response, 'Администрация')


class ReferenceViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(PagesConfig.REFERENCES_URL)
        USER1.create_in_db()

    def test_anonymous_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_authenticated_request(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)
