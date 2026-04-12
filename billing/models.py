from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from ai_platform.models import AIModel
from core.models import TimeStampedModel


class Plan(TimeStampedModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=0, default=Decimal("0"))
    duration_days = models.PositiveIntegerField(default=30)
    token_limit_per_window = models.PositiveIntegerField(default=100)
    reset_interval_hours = models.PositiveIntegerField(default=24)
    features = models.JSONField(default=dict, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    allowed_models = models.ManyToManyField(AIModel, blank=True, related_name="plans")

    class Meta:
        ordering = ["display_order", "price"]
        verbose_name = "پلن"
        verbose_name_plural = "پلن‌ها"

    def __str__(self):
        return self.name


class UserSubscription(TimeStampedModel):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELED = "canceled"
    STATUS_CHOICES = [
        (ACTIVE, "فعال"),
        (EXPIRED, "منقضی"),
        (CANCELED, "لغو شده"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="subscriptions")
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=ACTIVE)
    activated_from_order = models.ForeignKey("PurchaseOrder", on_delete=models.SET_NULL, null=True, blank=True, related_name="activated_subscriptions")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "اشتراک کاربر"
        verbose_name_plural = "اشتراک‌های کاربر"

    def __str__(self):
        return f"{self.user} - {self.plan}"

    @property
    def is_valid(self):
        return self.status == self.ACTIVE and self.ends_at >= timezone.now()


class QuotaWindow(TimeStampedModel):
    subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE, related_name="quota_windows")
    window_start = models.DateTimeField()
    window_end = models.DateTimeField()
    max_tokens = models.PositiveIntegerField()
    used_tokens = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-window_start"]
        verbose_name = "پنجره سهمیه"
        verbose_name_plural = "پنجره‌های سهمیه"

    def __str__(self):
        return f"{self.subscription} [{self.window_start:%Y-%m-%d %H:%M}]"

    @property
    def remaining_tokens(self):
        return max(self.max_tokens - self.used_tokens, 0)


class PurchaseOrder(TimeStampedModel):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    CANCELED = "canceled"
    STATUS_CHOICES = [
        (PENDING, "در انتظار پرداخت"),
        (PAID, "پرداخت شده"),
        (FAILED, "ناموفق"),
        (CANCELED, "لغو شده"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="orders")
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=PENDING)
    authority = models.CharField(max_length=120, blank=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "سفارش خرید"
        verbose_name_plural = "سفارش‌های خرید"

    def __str__(self):
        return f"{self.user} - {self.plan} - {self.status}"


class PaymentTransaction(TimeStampedModel):
    INITIATED = "initiated"
    VERIFIED = "verified"
    FAILED = "failed"
    STATUS_CHOICES = [
        (INITIATED, "شروع شده"),
        (VERIFIED, "تایید شده"),
        (FAILED, "ناموفق"),
    ]

    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="transactions")
    provider = models.CharField(max_length=50, default="zarinpal")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=INITIATED)
    authority = models.CharField(max_length=120, blank=True)
    reference_id = models.CharField(max_length=120, blank=True)
    payload = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"

    def __str__(self):
        return f"{self.provider} - {self.status}"
