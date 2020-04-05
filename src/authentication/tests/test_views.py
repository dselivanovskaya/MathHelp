from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LoginUserViewTest(TestCase):
    ''' Tests for 'login_user' view. '''

    @classmethod
    def setUpTestData(cls):
        cls.url  = '/login/'
        cls.name = 'login'
        cls.template = 'authentication/login.html'
        User.objects.create_user(
            username='john', email='john@mail.com', password='johny123'
        )

    def test_view_url_exists(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse(self.name))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(self.name))
        self.assertTemplateUsed(response, self.template)

    def test_existing_user_can_log_in(self):
        login = self.client.login(username='john', password='johny123')
        self.assertTrue(login)

    def test_successful_login_redirects_user_to_his_profile(self):
        response = self.client.post(self.url,
            {'username': 'john', 'password': 'johny123'},
        )
        self.assertRedirects(response, '/john')

    def test_successful_login_returns_user_profile_page(self):
        response = self.client.post(self.url,
            {'username': 'john', 'password': 'johny123'}, follow=True
        )
        self.assertTemplateUsed(response, 'profiles/user-profile.html')

    def test_fail_login_returns_login_page_again(self):
        response = self.client.post(self.url,
            {'username': 'alice', 'password': 'alice123'}
        )
        self.assertTemplateUsed(response, self.template)

    def test_already_logged_in_user_redirected_to_his_profile(self):
        self.client.login(username='john', password='johny123')
        response = self.client.get(self.url)
        self.assertRedirects(response, '/john')

    # Doesn't work
    # def test_successful_login_increments_user_profile_login_count(self):
    #     user = User.objects.get(username='john')
    #     login_count_before = user.profile.login_count
    #     response = self.client.post(self.url,
    #         {'username': 'john', 'password': 'johny123'}
    #     )
    #     self.assertEquals(login_count_before + 1, user.profile.login_count)


class LogoutUserViewTest(TestCase):
    ''' Tests for 'logout_user' view. '''

    @classmethod
    def setUpTestData(cls):
        cls.url  = '/logout/'
        cls.name = 'logout'

    def test_view_url_exists(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse(self.name), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_redirects_to_home_page(self):
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, '/')
