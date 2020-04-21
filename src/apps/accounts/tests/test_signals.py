from django.contrib.auth.models import User
from django.test import TestCase

from tests.data import USER1


class AccountsSignalsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = USER1.create_in_db()

    def test_on_successful_login_increment_login_count_is_called(self):
        before_login_count = self.user.profile.login_count
        self.client.login(username=USER1.username, password=USER1.password)
        self.user.refresh_from_db()
        self.assertEquals(before_login_count + 1, self.user.profile.login_count)

    def test_on_successful_login_initialize_session_entries_is_called(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertEquals(self.client.session['watched_tickets'], [])
