from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from tests.data import USER1

from tickets.apps import TicketsConfig as tickets_config
from tickets.views import TicketListView


class TicketListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(tickets_config.TICKET_LIST_URL)
        cls.view_class = TicketListView
        cls.template = cls.view_class.template_name
        USER1.create_in_db()

    def test_url_exists_for_authenticated_user(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_redirects_anonymous_user_to_login_page(self):
        self.assertRedirects(
            self.client.get(self.url), reverse(settings.LOGIN_URL)
        )

    def test_renders_correct_template(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertTemplateUsed(self.client.get(self.url), self.template)
