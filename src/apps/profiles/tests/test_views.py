from django.test import TestCase
from django.urls import reverse

from tests.data import MALE_USER

from profiles.views import ProfileUpdateView


class ProfileDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = MALE_USER.create()
        cls.profile = cls.user.profile
        cls.url = cls.profile.get_absolute_url()

    def test_anonymous_get_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_authenticated_get_request(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)


class ProfileUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = MALE_USER.create()
        cls.profile = cls.user.profile
        cls.url = cls.profile.get_absolute_update_url()
        cls.view_class = ProfileUpdateView

    def test_anonymous_get_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_authenticated_get_request(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_success_message(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        response = self.client.post(self.url, {}, follow=True)
        messages = list(response.context['messages'])
        self.assertEquals(str(messages[0]), self.view_class.success_message)
