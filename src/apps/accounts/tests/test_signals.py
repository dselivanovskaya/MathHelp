from django.test import TestCase

from tests.data import MALE_USER


class AccountsSignalsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = MALE_USER.create()

    def setUp(self):
        self.before_login_count = self.user.profile.login_count
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)

    def test_on_successful_login_increment_login_count_is_called(self):
        self.user.refresh_from_db()
        self.assertEquals(self.before_login_count + 1, self.user.profile.login_count)

    def test_on_successful_login_initialize_session_entries_is_called(self):
        self.assertEquals(self.client.session['read_tickets'], [])
        self.assertEquals(self.client.session['taken_quizzes'], {})
