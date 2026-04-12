from django.test import TestCase
from django.urls import reverse

from .models import User


class AccountsTests(TestCase):
    def test_signup_creates_user(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "full_name": "کاربر تست",
                "email": "test@example.com",
                "mobile": "09120000000",
                "password1": "S3curePass123",
                "password2": "S3curePass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_personalization_view_updates_user(self):
        user = User.objects.create_user(email="person@example.com", password="Secret123!", full_name="کاربر تست")
        self.client.force_login(user)
        response = self.client.post(
            reverse("accounts:personalization"),
            {
                "persona_choice": User.PERSONA_ANALYST,
                "custom_instructions": "مختصر جواب بده",
                "preferred_name": "امیر",
                "job_title": "برنامه‌نویس",
                "interests": "محصول و طراحی",
                "memory_enabled": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.preferred_name, "امیر")
        self.assertFalse(user.memory_enabled)
