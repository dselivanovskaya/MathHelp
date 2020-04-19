from django.shortcuts import reverse
from django.test import TestCase

from tests.data import USER1, USER2

from profiles.apps import ProfilesConfig as app_conf
from profiles.forms import ProfileUpdateForm


class ProfileUpdateFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.form_class = ProfileUpdateForm
        USER1.create_in_db()
        USER2.create_in_db()

    def test_form_displays_correct_error_message_if_username_is_taken(self):
        self.client.login(username=USER1.username, password=USER1.password)
        url = reverse(app_conf.PROFILE_UPDATE_URL, args=[USER1.username])
        response = self.client.post(url, {'username': USER2.username})
        self.assertFormError(
            response, 'form', 'username',
            self.form_class.error_messages['invalid_username'],
        )
