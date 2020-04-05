from django.test import TestCase
from django.urls import reverse


class ListTicketsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url  = '/tickets/'
        cls.name = 'tickets'
        cls.template = 'tickets/tickets.html'

    def test_view_url_exists(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse(self.name))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(self.name))
        self.assertTemplateUsed(response, self.template)
