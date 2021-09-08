""" test for app action functionality """
from unittest.mock import patch
from django.template.response import TemplateResponse
from django.test import TestCase
from django.test.client import RequestFactory

from bookwyrm import models, views


class EmailBlocklistViews(TestCase):
    """every response to a get request, html or json"""

    def setUp(self):
        """we need basic test data and mocks"""
        self.factory = RequestFactory()
        with patch("bookwyrm.suggested_users.rerank_suggestions_task.delay"), patch(
            "bookwyrm.activitystreams.populate_stream_task.delay"
        ):
            self.local_user = models.User.objects.create_user(
                "mouse@local.com",
                "mouse@mouse.mouse",
                "password",
                local=True,
                localname="mouse",
            )

        models.SiteSettings.objects.create()

    def test_blocklist_page_get(self):
        """there are so many views, this just makes sure it LOADS"""
        view = views.EmailBlocklist.as_view()
        request = self.factory.get("")
        request.user = self.local_user
        request.user.is_superuser = True

        result = view(request)

        self.assertIsInstance(result, TemplateResponse)
        result.render()
        self.assertEqual(result.status_code, 200)

    def test_blocklist_page_post(self):
        """there are so many views, this just makes sure it LOADS"""
        view = views.EmailBlocklist.as_view()
        request = self.factory.post("", {"domain": "gmail.com"})
        request.user = self.local_user
        request.user.is_superuser = True

        result = view(request)

        self.assertIsInstance(result, TemplateResponse)
        result.render()
        self.assertEqual(result.status_code, 200)

        self.assertTrue(
            models.EmailBlocklist.objects.filter(domain="gmail.com").exists()
        )

    def test_blocklist_page_delete(self):
        """there are so many views, this just makes sure it LOADS"""
        domain = models.EmailBlocklist.objects.create(domain="gmail.com")

        view = views.EmailBlocklist.as_view()
        request = self.factory.post(f"/settings/email-blocklist/{domain.id}/delete")
        request.user = self.local_user
        request.user.is_superuser = True

        result = view(request)

        self.assertIsInstance(result, TemplateResponse)
        self.assertEqual(result.status_code, 302)

        self.assertFalse(
            models.EmailBlocklist.objects.filter(domain="gmail.com").exists()
        )
