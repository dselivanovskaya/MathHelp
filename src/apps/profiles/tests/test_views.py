from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from tests.data import USER1, USER2

from profiles.apps import ProfilesConfig as profiles_config
from profiles.views import ProfileDetailView, ProfileUpdateView


class ProfileDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(profiles_config.PROFILE_DETAIL_URL, args=[USER1.username])
        cls.view_class = ProfileDetailView
        cls.template_name = cls.view_class.template_name
        USER1.create_in_db()

    def test_view_url_exists_for_authenticated_user(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_view_renders_correct_template_for_authenticated_user(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertTemplateUsed(self.client.get(self.url), self.template_name)

    def test_redirects_anonymous_user_to_login_page(self):
        self.assertRedirects(
            self.client.get(self.url), reverse(settings.LOGIN_URL)
        )


class ProfileUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(profiles_config.PROFILE_UPDATE_URL, args=[USER1.username])
        cls.view_class = ProfileUpdateView
        cls.form_class = cls.view_class.form_class
        cls.template_name = cls.view_class.template_name
        USER1.create_in_db()

    def test_view_url_exists_for_authenticated_user(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_view_renders_correct_form_for_authneticated_user(self):
        self.client.login(username=USER1.username, password=USER1.password)
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], self.form_class)

    def test_view_renders_correct_template_for_authenticated_user(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertTemplateUsed(self.client.get(self.url), self.template_name)

    def test_redirects_anonymous_user_to_login_page(self):
        self.assertRedirects(
            self.client.get(self.url), reverse(settings.LOGIN_URL)
        )

    def test_on_successful_update_sends_corrent_message(self):
        self.client.login(username=USER1.username, password=USER1.password)
        response = self.client.post(self.url, {
            'first_name': USER2.first_name,
            'last_name':  USER2.last_name,
            'email':      USER2.email,
            'username':   USER2.username,
         }, follow=True)
        messages = list(response.context['messages'])
        self.assertEquals(str(messages[0]), self.view_class.messages['success'])
