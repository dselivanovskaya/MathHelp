from django.test import TestCase
from django.urls import reverse

from tests.data import USER1

from pages.apps import PagesConfig as pages_config
from pages.views import IndexView, ReferenceView


class IndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(pages_config.INDEX_URL)
        cls.view_class = IndexView
        cls.template_name = cls.view_class.template_name
        USER1.create_in_db()

    def test_url_exists(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_renders_correct_template(self):
        self.assertTemplateUsed(self.client.get(self.url), self.template_name)

    def test_renders_correct_header_for_authenticated_user(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertTemplateUsed(
            self.client.get(self.url), 'includes/auth-header.html'
        )

    def test_renders_correct_header_for_anonymous_user(self):
        self.assertTemplateUsed(
            self.client.get(self.url), 'includes/anon-header.html'
        )

    def test_renders_create_account_href_for_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Создать аккаунт')

    def test_doesnt_render_create_account_href_for_authenticated_user(self):
        self.client.login(username=USER1.username, password=USER1.password)
        response = self.client.get(self.url)
        self.assertNotContains(response, 'Создать аккаунт')


class ReferenceViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(pages_config.REFERENCE_URL)
        cls.view_class = ReferenceView
        cls.template_name = cls.view_class.template_name

    def test_view_url_exists(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_view_renders_correct_template(self):
        self.assertTemplateUsed(self.client.get(self.url), self.template_name)
