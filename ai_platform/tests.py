from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from billing.models import Plan, PurchaseOrder
from billing.services import activate_plan_for_order

from .models import AIModel, AIModelCapability, Conversation


class ChatTests(TestCase):
    def setUp(self):
        self.model = AIModel.objects.create(
            name="Test Model",
            slug="test-model",
            provider_label="Provider",
            endpoint_url="https://example.com",
            model_identifier="test-model",
        )
        AIModelCapability.objects.create(model=self.model, capability_type=AIModelCapability.TEXT, is_enabled=True)

    @patch("ai_platform.views.AIAdapterService.run", return_value=("پاسخ تست", {"ok": True}))
    def test_guest_can_send_message(self, mocked_run):
        response = self.client.post(
            reverse("ai_platform:chat"),
            {"prompt": "سلام", "model": self.model.id},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Conversation.objects.exists())
        self.assertContains(response, "پاسخ تست")
        mocked_run.assert_called_once()

    @patch("ai_platform.views.AIAdapterService.run", return_value=("پاسخ تست", {"ok": True}))
    def test_guest_limit_redirects_after_five_messages(self, mocked_run):
        for _ in range(5):
            self.client.post(reverse("ai_platform:chat"), {"prompt": "سلام", "model": self.model.id})
        response = self.client.post(reverse("ai_platform:chat"), {"prompt": "سلام", "model": self.model.id}, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:signup"), response.url)

    def test_authenticated_user_can_archive_conversation(self):
        user = User.objects.create_user(email="chat@example.com", password="Secret123!", full_name="چت تست")
        conversation = Conversation.objects.create(user=user, model=self.model, title="نمونه گفتگو")
        self.client.force_login(user)
        response = self.client.post(reverse("ai_platform:chat_archive", args=[conversation.id]))
        self.assertEqual(response.status_code, 302)
        conversation.refresh_from_db()
        self.assertTrue(conversation.is_archived)

    def test_model_routes_render_without_optional_context_crashes(self):
        list_response = self.client.get(reverse("ai_platform:models"))
        detail_response = self.client.get(reverse("ai_platform:model_detail", args=[self.model.slug]))

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(list_response, self.model.name)
        self.assertContains(detail_response, self.model.name)

    def test_billing_page_renders_for_user_with_active_subscription(self):
        user = User.objects.create_user(email="billing@example.com", password="Secret123!", full_name="Billing User")
        plan = Plan.objects.create(
            name="Billing Plan",
            slug="billing-test-plan",
            price=250000,
            duration_days=30,
            token_limit_per_window=5,
            reset_interval_hours=24,
        )
        order = PurchaseOrder.objects.create(user=user, plan=plan, amount=plan.price, status=PurchaseOrder.PAID)
        activate_plan_for_order(order)

        self.client.force_login(user)
        response = self.client.get(reverse("ai_platform:billing"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, plan.name)
