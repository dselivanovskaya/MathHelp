from django.test import TestCase
from django.contrib.auth.models import User


class IncrementLoginCountTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='john', email='john@mail.com', password='johny123'
        )

    def test_on_successful_login_increment_login_count_is_called(self):
        user = User.objects.get(username='john')
        before_login_count = user.profile.login_count
        self.client.login(username='john', password='johny123')
        user.refresh_from_db()
        self.assertEquals(before_login_count + 1, user.profile.login_count)
