from django.test import TestCase
from django.urls import reverse

from billing.models import Plan


class CoreViewsTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FaralYar")

    def test_pricing_page_renders_plan(self):
        Plan.objects.create(
            name="پایه",
            slug="basic",
            price=100000,
            duration_days=30,
            token_limit_per_window=20,
            reset_interval_hours=24,
        )
        response = self.client.get(reverse("core:pricing"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "پایه")
