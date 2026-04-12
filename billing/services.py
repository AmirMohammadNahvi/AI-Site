from datetime import timedelta

import requests
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from core.models import SiteSetting

from .models import PaymentTransaction, PurchaseOrder, QuotaWindow, UserSubscription


class BillingError(Exception):
    pass


def get_active_subscription(user):
    now = timezone.now()
    return (
        UserSubscription.objects.filter(user=user, status=UserSubscription.ACTIVE, ends_at__gte=now)
        .select_related("plan")
        .first()
    )


def get_or_create_quota_window(subscription: UserSubscription):
    now = timezone.now()
    current = subscription.quota_windows.filter(window_start__lte=now, window_end__gte=now).first()
    if current:
        return current
    last_window = subscription.quota_windows.order_by("-window_end").first()
    start = last_window.window_end if last_window and last_window.window_end > subscription.starts_at else now
    end = start + timedelta(hours=subscription.plan.reset_interval_hours)
    return QuotaWindow.objects.create(
        subscription=subscription,
        window_start=start,
        window_end=end,
        max_tokens=subscription.plan.token_limit_per_window,
    )


def consume_tokens(subscription: UserSubscription, amount=1):
    window = get_or_create_quota_window(subscription)
    if window.remaining_tokens < amount:
        return False, window
    window.used_tokens += amount
    window.save(update_fields=["used_tokens", "updated_at"])
    return True, window


def activate_plan_for_order(order: PurchaseOrder):
    UserSubscription.objects.filter(user=order.user, status=UserSubscription.ACTIVE).update(
        status=UserSubscription.EXPIRED
    )
    starts_at = timezone.now()
    ends_at = starts_at + timedelta(days=order.plan.duration_days)
    subscription = UserSubscription.objects.create(
        user=order.user,
        plan=order.plan,
        starts_at=starts_at,
        ends_at=ends_at,
        status=UserSubscription.ACTIVE,
        activated_from_order=order,
    )
    get_or_create_quota_window(subscription)
    return subscription


class ZarinpalService:
    provider_name = "zarinpal"

    @staticmethod
    def get_merchant_id():
        site_settings = SiteSetting.get_solo()
        return site_settings.zarinpal_merchant_id or settings.ZARINPAL_MERCHANT_ID

    @classmethod
    def is_configured(cls):
        return bool(cls.get_merchant_id())

    @classmethod
    def create_payment_request(cls, request, order: PurchaseOrder):
        if not cls.is_configured():
            raise BillingError("Zarinpal merchant id is not configured.")
        callback_url = request.build_absolute_uri(reverse("billing:verify"))
        payload = {
            "merchant_id": cls.get_merchant_id(),
            "amount": int(order.amount),
            "description": order.description or f"خرید پلن {order.plan.name}",
            "callback_url": callback_url,
            "metadata": {
                "email": order.user.email,
                "mobile": order.user.mobile or "",
            },
        }
        response = requests.post(settings.ZARINPAL_REQUEST_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json().get("data", {})
        authority = data.get("authority")
        if not authority:
            raise BillingError("Could not create payment authority.")
        order.authority = authority
        order.save(update_fields=["authority", "updated_at"])
        PaymentTransaction.objects.create(
            order=order,
            provider=cls.provider_name,
            status=PaymentTransaction.INITIATED,
            authority=authority,
            payload=data,
        )
        return f"{settings.ZARINPAL_START_URL}{authority}"

    @classmethod
    def verify_payment(cls, order: PurchaseOrder, authority: str):
        payload = {
            "merchant_id": cls.get_merchant_id(),
            "amount": int(order.amount),
            "authority": authority,
        }
        response = requests.post(settings.ZARINPAL_VERIFY_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json().get("data", {})
        code = data.get("code")
        if code not in (100, 101):
            PaymentTransaction.objects.create(
                order=order,
                provider=cls.provider_name,
                status=PaymentTransaction.FAILED,
                authority=authority,
                payload=data,
            )
            raise BillingError("Payment verification failed.")
        ref_id = str(data.get("ref_id", ""))
        PaymentTransaction.objects.create(
            order=order,
            provider=cls.provider_name,
            status=PaymentTransaction.VERIFIED,
            authority=authority,
            reference_id=ref_id,
            payload=data,
        )
        order.status = PurchaseOrder.PAID
        order.save(update_fields=["status", "updated_at"])
        return ref_id
