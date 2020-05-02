from django.test import TestCase

from tests.data import USER_MALE


class AccountsSignalsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MALE.create_in_db()

    def test_on_successful_login_increment_login_count_is_called(self):
        before_login_count = self.user.profile.login_count
        self.client.login(username=USER_MALE.username, password=USER_MALE.password)
        self.user.refresh_from_db()
        self.assertEquals(before_login_count + 1, self.user.profile.login_count)

    def test_on_successful_login_initialize_session_entries_is_called(self):
        self.client.login(username=USER_MALE.username, password=USER_MALE.password)
        self.assertEquals(self.client.session['read_tickets'], [])
        self.assertEquals(self.client.session['taken_quizzes'], {})
