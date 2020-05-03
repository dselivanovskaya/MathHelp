from django.test import TestCase
from django.urls import reverse

from tests.data import USER_MALE

from profiles.views import ProfileUpdateView


class ProfileDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MALE.create_in_db()
        cls.profile = cls.user.profile
        cls.url = cls.profile.get_absolute_url()

    def test_anonymous_get_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_authenticated_get_request(self):
        self.client.login(username=USER_MALE.username, password=USER_MALE.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)


class ProfileUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MALE.create_in_db()
        cls.profile = cls.user.profile
        cls.url = cls.profile.get_absolute_update_url()
        cls.view_class = ProfileUpdateView

    def test_anonymous_get_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_authenticated_get_request(self):
        self.client.login(username=USER_MALE.username, password=USER_MALE.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_success_message(self):
        self.client.login(username=USER_MALE.username, password=USER_MALE.password)
        response = self.client.post(self.url, {}, follow=True)
        messages = list(response.context['messages'])
        self.assertEquals(str(messages[0]), self.view_class.success_message)
