from django.test import Client, TestCase

from django.contrib.auth.models import User

class ProfilesTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username = 'emma', 
        email = 'hogwart@email.uk', password = 'knowledge2000')
        self.user2 = User.objects.create_user(username = 'john', 
        email = 'john@email.uk', password = 'knowledge')

    def test_unauthenticated_user_can_not_access_any_other_user_profiles(self):
        response = self.client.get(f'/{self.user1.username}')
        self.assertRedirects(response, '/')

    def test_authenticated_user_can_not_access_any_other_user_profiles(self):
        self.client.login(username = self.user1.username,
                          password = 'knowledge2000')
        response = self.client.get(f'/{self.user2.username}')
        self.assertRedirects(response, '/')

    def test_unauthenticated_user_can_not_delete_any_other_user_profiles(self):
        before_delete_user_count = len(User.objects.all())
        response = self.client.get(f'/{self.user1.username}/delete')
        self.assertEquals(before_delete_user_count, len(User.objects.all()))

    def test_authenticated_user_can_not_delete_any_other_user_profiles(self):
        before_delete_user_count = len(User.objects.all())
        login = self.client.login(username = self.user1.username,
                          password = 'knowledge2000')
        self.assertTrue(login)
        response = self.client.get(f'/{self.user2.username}/delete')
        self.assertEquals(before_delete_user_count, len(User.objects.all()))

    def test_user_can_delete_his_profile(self):
        before_delete_user_count = len(User.objects.all())
        login = self.client.login(username = self.user1.username,
                                  password = 'knowledge2000')
        self.assertTrue(login)
        response = self.client.get(f'/{self.user1.username}/delete')
        self.assertEquals(before_delete_user_count, len(User.objects.all())+1)