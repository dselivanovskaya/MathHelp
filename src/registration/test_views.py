from django.test import TestCase
from django.urls import reverse


class RegisterUserViewTest(TestCase):
    ''' Tests for 'register_user' view. '''

    def setUp(self):
        self.view_url  = '/register/'
        self.view_name = 'register'
        self.template_name = 'registration/register.html'

    def test_view_url_exists(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse(self.view_name))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(self.view_name))
        self.assertTemplateUsed(response, self.template_name)

    def test_user_successful_registration_redirects_to_his_profile(self):
        response = self.client.post(self.view_url,
                    {'username' : 'john',
                     'email'    : 'john@mail.com',
                     'password1': 'johnIsCool12',
                     'password2': 'johnIsCool12',
                     })
        self.assertRedirects(response, '/john')

    def test_user_successful_registration_returns_user_profile_template(self):
        response = self.client.post(self.view_url,
                    {'username' : 'john',
                     'email'    : 'john@mail.com',
                     'password1': 'johnIsCool12',
                     'password2': 'johnIsCool12',
                     }, follow=True)
        self.assertTemplateUsed(response, 'profiles/user-profile.html')
