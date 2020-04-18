from django.contrib.auth.models import User
from django.test import TestCase

from .test_data import USER1


class AccountsSignalsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username=USER1.username, email=USER1.email, password=USER1.password
        )

    def test_on_successful_login_increment_login_count_is_called(self):
        user = User.objects.get(username=USER1.username)
        before_login_count = user.profile.login_count
        self.client.login(username=USER1.username, password=USER1.password)
        user.refresh_from_db()
        self.assertEquals(before_login_count + 1, user.profile.login_count)

    def test_on_successful_login_initializes_session_entries_is_called(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertEquals(self.client.session['watched_tickets'], [])
