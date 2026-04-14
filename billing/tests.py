from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User

from .models import Plan, PurchaseOrder
from .services import activate_plan_for_order, consume_tokens, get_or_create_quota_window


class BillingServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="bill@example.com", password="Pass123456", full_name="Bill User")
        self.plan = Plan.objects.create(
            name="حرفه‌ای",
            slug="pro",
            price=250000,
            duration_days=30,
            token_limit_per_window=3,
            reset_interval_hours=24,
        )

    def test_activate_order_creates_subscription_and_window(self):
        order = PurchaseOrder.objects.create(user=self.user, plan=self.plan, amount=self.plan.price, status=PurchaseOrder.PAID)
        subscription = activate_plan_for_order(order)
        window = get_or_create_quota_window(subscription)
        self.assertEqual(window.remaining_tokens, 3)
        self.assertGreaterEqual(subscription.ends_at, timezone.now())

    def test_consume_tokens_reduces_remaining(self):
        order = PurchaseOrder.objects.create(user=self.user, plan=self.plan, amount=self.plan.price, status=PurchaseOrder.PAID)
        subscription = activate_plan_for_order(order)
        success, window = consume_tokens(subscription, 1)
        self.assertTrue(success)
        self.assertEqual(window.remaining_tokens, 2)

    def test_billing_root_redirects_to_safe_destination(self):
        guest_response = self.client.get(reverse("billing:index"))
        self.assertRedirects(guest_response, reverse("core:pricing"))

        self.client.force_login(self.user)
        auth_response = self.client.get(reverse("billing:index"))
        self.assertRedirects(auth_response, reverse("ai_platform:billing"))
