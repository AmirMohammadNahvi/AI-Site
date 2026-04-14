from django.urls import reverse
from django.utils import timezone

from billing.models import PaymentTransaction, Plan, PurchaseOrder
from billing.services import get_active_subscription, get_or_create_quota_window


def _initials(value, fallback="فا"):
    parts = [part for part in (value or "").split() if part]
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[1][0]}"
    if value:
        return value[:2]
    return fallback


def _format_dt(value):
    if not value:
        return ""
    return timezone.localtime(value).strftime("%Y/%m/%d %H:%M")


def _format_amount(value):
    if value in (None, ""):
        return "-"
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


def _with_defaults(payload, defaults):
    merged = defaults.copy()
    merged.update(payload)
    return merged


def get_subscription_and_window(request):
    if not request.user.is_authenticated:
        return None, None
    subscription = get_active_subscription(request.user)
    quota_window = get_or_create_quota_window(subscription) if subscription else None
    return subscription, quota_window


def build_current_workspace(request, subscription=None):
    if request.user.is_authenticated:
        subtitle = request.user.full_name or request.user.email
        meta = subscription.plan.name if subscription else "بدون پلن فعال"
        badge = "حساب شما" if subscription else "بدون پلن"
        name = "فضای شخصی"
    else:
        subtitle = "شروع سریع بدون ورود"
        meta = "برای ذخیره تاریخچه و خرید وارد شوید"
        badge = "مهمان"
        name = "حالت مهمان"

    workspace = {
        "id": "personal",
        "slug": "personal",
        "name": name,
        "subtitle": subtitle,
        "meta": meta,
        "badge": badge,
        "initials": _initials(subtitle or name),
        "url": reverse("ai_platform:chat"),
        "is_current": True,
    }
    return workspace


def build_current_plan_context(subscription, latest_order=None):
    if not subscription:
        return {
            "primary_cta_url": reverse("core:pricing"),
            "primary_cta_label": "مرور پلن‌ها",
            "secondary_cta_url": reverse("core:contact"),
            "secondary_cta_label": "تماس با تیم",
        }

    order_reference = ""
    if latest_order:
        order_reference = f"#{latest_order.id}"

    return {
        "name": subscription.plan.name,
        "title": subscription.plan.name,
        "description": subscription.plan.description or "جزئیات پلن فعال شما از همین بخش قابل مرور است.",
        "summary": subscription.plan.description or "این پلن برای استفاده روزمره همین حساب فعال است.",
        "price_label": f"{_format_amount(subscription.plan.price)} تومان",
        "cycle_label": f"{subscription.plan.duration_days} روز اعتبار",
        "status_label": "فعال",
        "started_at_label": _format_dt(subscription.starts_at),
        "expires_at_label": _format_dt(subscription.ends_at),
        "started_at_note": "شروع اعتبار پلن فعلی",
        "expires_at_note": "در صورت نداشتن سفارش جدید، پس از این زمان پایان می‌یابد.",
        "order_reference": order_reference or "از سفارش فعال فعلی",
        "renewal_label": "تمدید خودکار تعریف نشده",
        "renewal_note": "برای ادامه استفاده باید سفارش بعدی را خودتان ثبت کنید.",
        "helper_text": "مرجع اصلی مقایسه پلن‌ها صفحه قیمت‌گذاری عمومی است؛ وضعیت واقعی این حساب از همین کارت خوانده می‌شود.",
        "primary_cta_url": reverse("core:pricing"),
        "primary_cta_label": "مقایسه پلن‌ها",
        "secondary_cta_url": reverse("ai_platform:chat"),
        "secondary_cta_label": "بازگشت به گفتگو",
    }


def build_current_plan_context(subscription, latest_order=None):
    defaults = {
        "badge": "",
        "name": "",
        "title": "",
        "description": "",
        "summary": "",
        "price_label": "",
        "cycle_label": "",
        "status_label": "",
        "started_at_label": "",
        "started_at_note": "",
        "expires_at_label": "",
        "expires_at_note": "",
        "renews_at_label": "",
        "renews_at_note": "",
        "order_reference": "",
        "order_label": "",
        "invoice_note": "",
        "renewal_label": "",
        "renewal_note": "",
        "next_action_label": "",
        "helper_text": "",
        "primary_cta_url": "",
        "primary_cta_label": "",
        "secondary_cta_url": "",
        "secondary_cta_label": "",
    }
    if not subscription:
        return _with_defaults(
            {
                "primary_cta_url": reverse("core:pricing"),
                "primary_cta_label": "Ù…Ø±ÙˆØ± Ù¾Ù„Ù†â€ŒÙ‡Ø§",
                "secondary_cta_url": reverse("core:contact"),
                "secondary_cta_label": "ØªÙ…Ø§Ø³ Ø¨Ø§ ØªÛŒÙ…",
            },
            defaults,
        )

    order_reference = f"#{latest_order.id}" if latest_order else ""
    return _with_defaults(
        {
            "badge": "Ù¾Ù„Ù† ÙØ¹Ø§Ù„",
            "name": subscription.plan.name,
            "title": subscription.plan.name,
            "description": subscription.plan.description or "Ø¬Ø²Ø¦ÛŒØ§Øª Ù¾Ù„Ù† ÙØ¹Ø§Ù„ Ø´Ù…Ø§ Ø§Ø² Ù‡Ù…ÛŒÙ† Ø¨Ø®Ø´ Ù‚Ø§Ø¨Ù„ Ù…Ø±ÙˆØ± Ø§Ø³Øª.",
            "summary": subscription.plan.description or "Ø§ÛŒÙ† Ù¾Ù„Ù† Ø¨Ø±Ø§ÛŒ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø±ÙˆØ²Ù…Ø±Ù‡ Ù‡Ù…ÛŒÙ† Ø­Ø³Ø§Ø¨ ÙØ¹Ø§Ù„ Ø§Ø³Øª.",
            "price_label": f"{_format_amount(subscription.plan.price)} ØªÙˆÙ…Ø§Ù†",
            "cycle_label": f"{subscription.plan.duration_days} Ø±ÙˆØ² Ø§Ø¹ØªØ¨Ø§Ø±",
            "status_label": "ÙØ¹Ø§Ù„",
            "started_at_label": _format_dt(subscription.starts_at),
            "expires_at_label": _format_dt(subscription.ends_at),
            "started_at_note": "Ø´Ø±ÙˆØ¹ Ø§Ø¹ØªØ¨Ø§Ø± Ù¾Ù„Ù† ÙØ¹Ù„ÛŒ",
            "expires_at_note": "Ø¯Ø± ØµÙˆØ±Øª Ù†Ø¯Ø§Ø´ØªÙ† Ø³ÙØ§Ø±Ø´ Ø¬Ø¯ÛŒØ¯ØŒ Ù¾Ø³ Ø§Ø² Ø§ÛŒÙ† Ø²Ù…Ø§Ù† Ù¾Ø§ÛŒØ§Ù† Ù…ÛŒâ€ŒÛŒØ§Ø¨Ø¯.",
            "order_reference": order_reference or "Ø§Ø² Ø³ÙØ§Ø±Ø´ ÙØ¹Ø§Ù„ ÙØ¹Ù„ÛŒ",
            "renewal_label": "ØªÙ…Ø¯ÛŒØ¯ Ø®ÙˆØ¯Ú©Ø§Ø± ØªØ¹Ø±ÛŒÙ Ù†Ø´Ø¯Ù‡",
            "renewal_note": "Ø¨Ø±Ø§ÛŒ Ø§Ø¯Ø§Ù…Ù‡ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø¨Ø§ÛŒØ¯ Ø³ÙØ§Ø±Ø´ Ø¨Ø¹Ø¯ÛŒ Ø±Ø§ Ø®ÙˆØ¯ØªØ§Ù† Ø«Ø¨Øª Ú©Ù†ÛŒØ¯.",
            "helper_text": "Ù…Ø±Ø¬Ø¹ Ø§ØµÙ„ÛŒ Ù…Ù‚Ø§ÛŒØ³Ù‡ Ù¾Ù„Ù†â€ŒÙ‡Ø§ ØµÙØ­Ù‡ Ù‚ÛŒÙ…Øªâ€ŒÚ¯Ø°Ø§Ø±ÛŒ Ø¹Ù…ÙˆÙ…ÛŒ Ø§Ø³ØªØ› ÙˆØ¶Ø¹ÛŒØª ÙˆØ§Ù‚Ø¹ÛŒ Ø§ÛŒÙ† Ø­Ø³Ø§Ø¨ Ø§Ø² Ù‡Ù…ÛŒÙ† Ú©Ø§Ø±Øª Ø®ÙˆØ§Ù†Ø¯Ù‡ Ù…ÛŒâ€ŒØ´ÙˆØ¯.",
            "primary_cta_url": reverse("core:pricing"),
            "primary_cta_label": "Ù…Ù‚Ø§ÛŒØ³Ù‡ Ù¾Ù„Ù†â€ŒÙ‡Ø§",
            "secondary_cta_url": reverse("ai_platform:chat"),
            "secondary_cta_label": "Ø¨Ø§Ø²Ú¯Ø´Øª Ø¨Ù‡ Ú¯ÙØªÚ¯Ùˆ",
        },
        defaults,
    )


def build_app_shell_context(
    request,
    *,
    active_nav,
    page_title,
    page_description="",
    page_eyebrow="فضای کاری",
    page_notice="",
):
    subscription, quota_window = get_subscription_and_window(request)
    current_workspace = build_current_workspace(request, subscription=subscription)
    billing_url = reverse("ai_platform:billing") if request.user.is_authenticated else reverse("core:pricing")

    sidebar_items = [
        {
            "label": "گفتگو",
            "caption": "ورود به جریان گفت‌وگو",
            "url": reverse("ai_platform:chat"),
            "is_active": active_nav == "chat",
        },
        {
            "label": "مدل‌ها",
            "caption": "مرور مدل‌های فعال",
            "url": reverse("ai_platform:models"),
            "is_active": active_nav == "models",
        },
        {
            "label": "دستیارها",
            "caption": "پروفایل‌های کاری قابل استفاده",
            "url": reverse("ai_platform:assistants"),
            "is_active": active_nav == "assistants",
        },
        {
            "label": "حافظه",
            "caption": "مرکز کنترل حافظه",
            "url": reverse("ai_platform:memory"),
            "is_active": active_nav == "memory",
        },
        {
            "label": "اشتراک و پرداخت" if request.user.is_authenticated else "قیمت‌گذاری",
            "caption": "وضعیت فعلی حساب" if request.user.is_authenticated else "مرور پلن‌ها",
            "url": billing_url,
            "is_active": active_nav == "billing",
        },
    ]

    overflow_items = [
        {"label": "صفحه اصلی", "url": reverse("core:home")},
        {"label": "وبلاگ", "url": reverse("blog:list")},
    ]
    if request.user.is_authenticated:
        overflow_items.append({"label": "پروفایل", "url": reverse("accounts:profile")})
        if request.user.is_staff:
            overflow_items.append({"label": "مرکز کنترل", "url": reverse("dashboard:admin_home")})
        overflow_items.append({"label": "خروج", "url": reverse("accounts:logout"), "is_danger": True})
    else:
        overflow_items.extend(
            [
                {"label": "ورود", "url": reverse("accounts:login")},
                {"label": "ثبت‌نام", "url": reverse("accounts:signup")},
            ]
        )

    latest_order = None
    if request.user.is_authenticated:
        latest_order = request.user.orders.select_related("plan").first()

    return {
        "subscription": subscription,
        "quota_window": quota_window,
        "current_workspace": current_workspace,
        "workspace_list": [current_workspace],
        "conversation_entry_context": None,
        "state": "",
        "badge": "",
        "state_label": "",
        "reason": "",
        "new_cta_url": "",
        "new_cta_label": "",
        "new_note": "",
        "existing_cta_url": "",
        "existing_cta_label": "",
        "existing_note": "",
        "current_cta_url": "",
        "current_cta_label": "",
        "current_note": "",
        "helper": "",
        "assistant_chip": None,
        "assistant_label": "",
        "assistant_picker_groups": [],
        "conversation_is_migrated": False,
        "conversation_loading": False,
        "composer_disabled": False,
        "composer_disabled_reason": "",
        "composer_secondary_url": "",
        "composer_secondary_label": "",
        "composer_space_label": "",
        "composer_attachment_label": "",
        "archived_empty_title": "",
        "archived_empty_body": "",
        "archived_empty_hint": "",
        "conversation_storage_key": "",
        "app_sidebar_items": sidebar_items,
        "app_overflow_items": overflow_items,
        "app_page_title": page_title,
        "app_page_description": page_description,
        "app_page_eyebrow": page_eyebrow,
        "app_page_notice": page_notice,
        "app_mobile_footer_note": "این منو فقط مسیرهای فعال v1.5 را نگه می‌دارد تا بین سطوح قدیمی و جدید جابه‌جایی پراکنده نداشته باشیم.",
        "current_plan": build_current_plan_context(subscription, latest_order=latest_order),
    }


def build_memory_scope_inline(request, subscription=None):
    if not request.user.is_authenticated:
        return None
    subscription = subscription or get_active_subscription(request.user)
    if not subscription:
        label = "نیازمند پلن فعال"
    elif request.user.memory_enabled:
        label = "فعال در حساب شخصی"
    else:
        label = "خاموش در حساب"
    return {
        "label": label,
        "center_url": reverse("ai_platform:memory"),
        "center_label": "مرکز حافظه",
    }


def serialize_model(model):
    capabilities = [
        {
            "label": capability.get_capability_type_display(),
            "short_label": capability.get_capability_type_display(),
        }
        for capability in model.capabilities.filter(is_enabled=True)
    ]
    summary = model.summary or model.description or "برای استفاده روزمره در گفت‌وگوهای FaralYar آماده شده است."
    return {
        "name": model.name,
        "initials": _initials(model.name, fallback="AI"),
        "family_label": model.provider_label,
        "summary": summary,
        "fit_statement": model.description or summary,
        "availability_state": "available",
        "availability_label": "آماده استفاده",
        "availability_note": "در مسیر گفت‌وگوی فعلی می‌توانید این مدل را انتخاب کنید.",
        "availability_headline": "در گفت‌وگوی فعلی قابل انتخاب است",
        "workspace_label": "فضای شخصی",
        "capabilities": capabilities,
        "badges": capabilities,
        "detail_url": reverse("ai_platform:model_detail", args=[model.slug]),
        "detail_label": "جزئیات مدل",
        "primary_cta_url": reverse("ai_platform:chat"),
        "primary_cta_label": "شروع گفتگو",
        "secondary_cta_url": reverse("ai_platform:chat"),
        "secondary_cta_label": "بازگشت به گفتگو",
        "model_use_context": {
            "state": "available",
            "primary_cta_url": reverse("ai_platform:chat"),
            "primary_cta_label": "شروع گفتگو با این مدل",
            "secondary_cta_url": reverse("ai_platform:models"),
            "secondary_cta_label": "بازگشت به فهرست مدل‌ها",
            "reason": "انتخاب نهایی مدل هنگام ارسال پیام انجام می‌شود.",
        },
    }


def serialize_model(model):
    capability_defaults = {
        "label": "",
        "short_label": "",
        "name": "",
        "summary": "",
        "state": "supported",
        "availability_state": "supported",
        "state_label": "",
        "note": "",
        "reason": "",
    }
    capabilities = [
        _with_defaults(
            {
                "label": capability.get_capability_type_display(),
                "short_label": capability.get_capability_type_display(),
            },
            capability_defaults,
        )
        for capability in model.capabilities.filter(is_enabled=True)
    ]
    summary = model.summary or model.description or "Ø¨Ø±Ø§ÛŒ Ø§Ø³ØªÙØ§Ø¯Ù‡ Ø±ÙˆØ²Ù…Ø±Ù‡ Ø¯Ø± Ú¯ÙØªâ€ŒÙˆÚ¯ÙˆÙ‡Ø§ÛŒ FaralYar Ø¢Ù…Ø§Ø¯Ù‡ Ø´Ø¯Ù‡ Ø§Ø³Øª."
    model_defaults = {
        "name": "",
        "initials": "AI",
        "family_label": "",
        "speed_label": "",
        "summary": "",
        "long_summary": "",
        "fit_statement": "",
        "meta_description": "",
        "category_label": "",
        "availability_state": "available",
        "availability_label": "",
        "availability_note": "",
        "availability_headline": "",
        "workspace_label": "",
        "workspace_note": "",
        "plan_note": "",
        "blocked_title": "",
        "hero_note": "",
        "use_summary": "",
        "use_helper": "",
        "upgrade_title": "",
        "upgrade_body": "",
        "replacement_label": "",
        "detail_url": "",
        "detail_label": "",
        "detail_back_url": reverse("ai_platform:models"),
        "detail_back_label": "Ø¨Ø§Ø²Ú¯Ø´Øª Ø¨Ù‡ Ú©Ø§ØªØ§Ù„ÙˆÚ¯ Ù…Ø¯Ù„â€ŒÙ‡Ø§",
        "primary_cta_url": "",
        "primary_cta_label": "",
        "secondary_cta_url": "",
        "secondary_cta_label": "",
        "capabilities": [],
        "badges": [],
        "strengths": [],
        "strengths_summary": "",
        "limitations": [],
        "limitations_summary": "",
        "is_recommended": False,
        "is_deprecated": False,
        "model_use_context": {
            "badge": "",
            "title": "",
            "body": "",
            "helper": "",
            "note": "",
            "state": "available",
            "state_label": "",
            "reason": "",
            "primary_cta_url": "",
            "primary_cta_label": "",
            "secondary_cta_url": "",
            "secondary_cta_label": "",
        },
    }
    return _with_defaults(
        {
            "name": model.name,
            "initials": _initials(model.name, fallback="AI"),
            "family_label": model.provider_label,
            "summary": summary,
            "fit_statement": model.description or summary,
            "availability_state": "available",
            "availability_label": "Ø¢Ù…Ø§Ø¯Ù‡ Ø§Ø³ØªÙØ§Ø¯Ù‡",
            "availability_note": "Ø¯Ø± Ù…Ø³ÛŒØ± Ú¯ÙØªâ€ŒÙˆÚ¯ÙˆÛŒ ÙØ¹Ù„ÛŒ Ù…ÛŒâ€ŒØªÙˆØ§Ù†ÛŒØ¯ Ø§ÛŒÙ† Ù…Ø¯Ù„ Ø±Ø§ Ø§Ù†ØªØ®Ø§Ø¨ Ú©Ù†ÛŒØ¯.",
            "availability_headline": "Ø¯Ø± Ú¯ÙØªâ€ŒÙˆÚ¯ÙˆÛŒ ÙØ¹Ù„ÛŒ Ù‚Ø§Ø¨Ù„ Ø§Ù†ØªØ®Ø§Ø¨ Ø§Ø³Øª",
            "workspace_label": "ÙØ¶Ø§ÛŒ Ø´Ø®ØµÛŒ",
            "capabilities": capabilities,
            "badges": capabilities,
            "detail_url": reverse("ai_platform:model_detail", args=[model.slug]),
            "detail_label": "Ø¬Ø²Ø¦ÛŒØ§Øª Ù…Ø¯Ù„",
            "primary_cta_url": reverse("ai_platform:chat"),
            "primary_cta_label": "Ø´Ø±ÙˆØ¹ Ú¯ÙØªÚ¯Ùˆ",
            "secondary_cta_url": reverse("ai_platform:chat"),
            "secondary_cta_label": "Ø¨Ø§Ø²Ú¯Ø´Øª Ø¨Ù‡ Ú¯ÙØªÚ¯Ùˆ",
            "model_use_context": {
                "state": "available",
                "primary_cta_url": reverse("ai_platform:chat"),
                "primary_cta_label": "Ø´Ø±ÙˆØ¹ Ú¯ÙØªÚ¯Ùˆ Ø¨Ø§ Ø§ÛŒÙ† Ù…Ø¯Ù„",
                "secondary_cta_url": reverse("ai_platform:models"),
                "secondary_cta_label": "Ø¨Ø§Ø²Ú¯Ø´Øª Ø¨Ù‡ ÙÙ‡Ø±Ø³Øª Ù…Ø¯Ù„â€ŒÙ‡Ø§",
                "reason": "Ø§Ù†ØªØ®Ø§Ø¨ Ù†Ù‡Ø§ÛŒÛŒ Ù…Ø¯Ù„ Ù‡Ù†Ú¯Ø§Ù… Ø§Ø±Ø³Ø§Ù„ Ù¾ÛŒØ§Ù… Ø§Ù†Ø¬Ø§Ù… Ù…ÛŒâ€ŒØ´ÙˆØ¯.",
            },
        },
        model_defaults,
    )


def build_billing_usage_context(subscription, quota_window):
    if not subscription or not quota_window:
        return {
            "title": "وضعیت مصرف دوره فعلی",
            "description": "وقتی اشتراک فعالی وجود نداشته باشد، سهمیه‌ای برای نمایش یا مصرف ثبت نمی‌شود.",
            "status_label": "بدون سهمیه فعال",
            "tone": "neutral",
            "used_label": "0",
            "total_label": "-",
            "remaining_label": "-",
            "progress_percent": 0,
            "reset_label": "ثبت نشده",
            "window_label": "بدون بازه فعال",
            "helper_text": "پس از فعال شدن پلن، مصرف و زمان ریست از همین بخش قابل پیگیری خواهد بود.",
            "primary_cta_url": reverse("core:pricing"),
            "primary_cta_label": "مرور پلن‌ها",
        }

    total = quota_window.max_tokens or 0
    used = quota_window.used_tokens
    remaining = quota_window.remaining_tokens
    progress_percent = int((used / total) * 100) if total else 0
    tone = "good"
    status_label = "در محدوده عادی"
    if progress_percent >= 90:
        tone = "critical"
        status_label = "نزدیک به سقف بازه"
    elif progress_percent >= 70:
        tone = "warning"
        status_label = "مصرف بالاتر از معمول"

    return {
        "title": "وضعیت مصرف دوره فعلی",
        "description": "سهمیه و مصرف بر اساس بازه فعال همین اشتراک نشان داده می‌شود.",
        "status_label": status_label,
        "tone": tone,
        "used_label": str(used),
        "total_label": str(total),
        "remaining_label": str(remaining),
        "progress_percent": progress_percent,
        "progress_caption": f"{progress_percent}% از سقف این بازه مصرف شده است." if total else "",
        "reset_label": _format_dt(quota_window.window_end),
        "reset_note": "در پایان این بازه، سهمیه دوره بعدی محاسبه می‌شود.",
        "window_label": f"{_format_dt(quota_window.window_start)} تا {_format_dt(quota_window.window_end)}",
        "window_note": f"سقف هر بازه برای پلن {subscription.plan.name} برابر با {total} پیام است.",
        "helper_text": "مصرف فقط روی اشتراک فعال محاسبه می‌شود و برای سفارش‌های ناموفق یا لغوشده تغییری اعمال نمی‌گردد.",
        "primary_cta_url": reverse("ai_platform:chat"),
        "primary_cta_label": "بازگشت به گفتگو",
        "secondary_cta_url": reverse("core:pricing"),
        "secondary_cta_label": "مرور پلن‌ها",
    }


def build_billing_activity_items(orders):
    tone_map = {
        PurchaseOrder.PAID: "success",
        PurchaseOrder.FAILED: "danger",
        PurchaseOrder.CANCELED: "warning",
        PurchaseOrder.PENDING: "neutral",
    }
    items = []
    for order in orders:
        items.append(
            {
                "title": order.plan.name,
                "subtitle": order.description or "سفارش خرید پلن",
                "status_label": order.get_status_display(),
                "status_tone": tone_map.get(order.status, "neutral"),
                "created_at_label": _format_dt(order.created_at),
                "reference_label": f"سفارش #{order.id}",
                "type_label": "خرید پلن",
                "amount_label": f"{_format_amount(order.amount)} تومان",
                "detail_url": reverse("billing:order_status", args=[order.id]),
                "detail_label": "وضعیت سفارش",
            }
        )
    return items


def build_billing_recommendation_context(request, subscription, quota_window):
    if not subscription:
        return {
            "badge": "بدون پلن فعال",
            "tone": "warning",
            "title": "اولین اقدام بعدی، انتخاب پلن مناسب است",
            "body": "چون برای این حساب اشتراک فعالی ثبت نشده، مسیر بعدی از صفحه قیمت‌گذاری عمومی شروع می‌شود.",
            "summary": "اول ساختار و تفاوت پلن‌ها را ببینید، بعد خرید را از همان مسیر شروع کنید.",
            "items": [
                "صفحه قیمت‌گذاری مرجع مقایسه عمومی پلن‌هاست.",
                "وضعیت واقعی سفارش‌های شما بعد از خرید از صفحه اشتراک و وضعیت سفارش خوانده می‌شود.",
            ],
            "primary_cta_url": reverse("core:pricing"),
            "primary_cta_label": "مرور پلن‌ها",
            "secondary_cta_url": reverse("core:contact"),
            "secondary_cta_label": "پرسیدن سوال",
        }

    if quota_window and quota_window.remaining_tokens <= max(quota_window.max_tokens // 5, 1):
        return {
            "badge": "مصرف بالا",
            "tone": "warning",
            "title": "مصرف این بازه به سقف نزدیک شده است",
            "body": "اگر استفاده شما در همین ریتم ادامه پیدا کند، بهتر است زمان ریست بعدی و گزینه‌های پلن را از همین حالا مرور کنید.",
            "summary": "برای تغییرات بعدی عجله لازم نیست، اما بهتر است وضعیت ریست و گزینه‌های موجود را زودتر ببینید.",
            "items": [
                "تا قبل از پایان بازه فعلی، سهمیه همین اشتراک معتبر می‌ماند.",
                "در صورت نیاز به ظرفیت متفاوت، مقایسه پلن‌ها از صفحه قیمت‌گذاری انجام می‌شود.",
            ],
            "primary_cta_url": reverse("core:pricing"),
            "primary_cta_label": "مرور پلن‌ها",
            "secondary_cta_url": reverse("ai_platform:chat"),
            "secondary_cta_label": "ادامه گفتگو",
        }

    return {
        "badge": "وضعیت پایدار",
        "tone": "good",
        "title": "در حال حاضر مسیر اصلی، ادامه استفاده از همین اشتراک است",
        "body": "پلن فعال و بازه مصرف فعلی هر دو مشخص‌اند و اقدام فوری دیگری لازم نیست.",
        "summary": "اگر نیاز شما تغییر نکرده، همین صفحه فقط برای پایش وضعیت و سفارش‌های اخیر کافی است.",
        "items": [
            "برای استفاده روزمره به جریان گفت‌وگو برگردید.",
            "برای مقایسه پلن‌های دیگر هر زمان خواستید می‌توانید به صفحه قیمت‌گذاری بروید.",
        ],
        "primary_cta_url": reverse("ai_platform:chat"),
        "primary_cta_label": "بازگشت به گفتگو",
        "secondary_cta_url": reverse("core:pricing"),
        "secondary_cta_label": "مرور پلن‌ها",
    }


def build_checkout_plan_context(plan, current_plan_label=None):
    snapshot_items = [
        {"label": "مدت اعتبار", "value": f"{plan.duration_days} روز"},
        {"label": "سقف هر بازه", "value": str(plan.token_limit_per_window)},
        {"label": "ریست بازه", "value": f"هر {plan.reset_interval_hours} ساعت"},
        {"label": "مدل‌های مجاز", "value": str(plan.allowed_models.count())},
    ]
    return {
        "checkout_plan": {
            "name": plan.name,
            "summary": plan.description or "این پلن برای استفاده روشن و قابل‌پیش‌بینی آماده شده است.",
            "fit_statement": plan.description or "قبل از پرداخت، فقط مرور نهایی همین پلن انجام می‌شود.",
            "snapshot_label": "مرور نهایی",
            "snapshot_items": snapshot_items,
            "price_label": f"{_format_amount(plan.price)} تومان",
            "badge": "پلن انتخاب‌شده",
        },
        "checkout_current_plan_label": current_plan_label,
        "checkout_change_items": [
            f"در صورت تایید موفق، پلن {plan.name} برای حساب شما فعال می‌شود.",
            f"بازه اعتبار این سفارش از زمان فعال‌سازی به مدت {plan.duration_days} روز محاسبه می‌شود.",
            f"سهمیه هر بازه بر اساس سقف {plan.token_limit_per_window} پیام و ریست هر {plan.reset_interval_hours} ساعت اعمال می‌شود.",
        ],
        "checkout_unchanged_items": [
            "خود گفت‌وگوها، تاریخچه و پیام‌های قبلی با این خرید حذف یا جابه‌جا نمی‌شوند.",
            "محدودیت‌های خارج از پلن، صرفا با ثبت این سفارش به‌تنهایی تغییر نمی‌کنند.",
        ],
        "checkout_next_step_items": [
            "به درگاه پرداخت هدایت می‌شوید.",
            "پس از بازگشت، نتیجه نهایی در صفحه وضعیت سفارش ثبت می‌شود.",
            "تغییر پلن و سهمیه فقط بعد از تایید نهایی همین سفارش اعمال می‌شود.",
        ],
        "checkout_support_cta_url": reverse("core:contact"),
        "checkout_support_cta_label": "تماس با تیم",
    }


def build_order_status_context(order):
    status_map = {
        PurchaseOrder.PAID: ("success", "پرداخت موفق"),
        PurchaseOrder.FAILED: ("failed", "پرداخت ناموفق"),
        PurchaseOrder.CANCELED: ("canceled", "پرداخت لغوشده"),
        PurchaseOrder.PENDING: ("pending", "در انتظار نتیجه"),
    }
    status_key, short_label = status_map.get(order.status, ("pending", order.get_status_display()))
    latest_transaction = order.transactions.order_by("-created_at").first()
    reference_label = f"کد رهگیری {latest_transaction.reference_id}" if latest_transaction and latest_transaction.reference_id else ""

    payment_next_actions = []
    if status_key == "success":
        payment_next_actions.append(
            {
                "title": "وضعیت اشتراک را از مرکز اشتراک بررسی کنید",
                "body": "اگر این سفارش برای فعال‌سازی یا تمدید بوده، مرجع نهایی حساب شما صفحه اشتراک و پرداخت است.",
                "cta_url": reverse("ai_platform:billing"),
                "cta_label": "مرکز اشتراک",
                "tone": "primary",
            }
        )
        payment_next_actions.append(
            {
                "title": "به استفاده روزمره برگردید",
                "body": "بعد از ثبت موفق سفارش می‌توانید از مسیر گفت‌وگو ادامه دهید.",
                "cta_url": reverse("ai_platform:chat"),
                "cta_label": "بازگشت به گفتگو",
            }
        )
    else:
        payment_next_actions.append(
            {
                "title": "برای اقدام دوباره از مسیر رسمی خرید شروع کنید",
                "body": "اگر هنوز همان پلن را می‌خواهید، بهتر است سفارش جدید را از صفحه قیمت‌گذاری یا مرکز اشتراک آغاز کنید.",
                "cta_url": reverse("core:pricing"),
                "cta_label": "مرور پلن‌ها",
                "tone": "primary",
            }
        )
        payment_next_actions.append(
            {
                "title": "اگر نیاز به پیگیری دارید، همین شناسه سفارش را نگه دارید",
                "body": "مرجع پیگیری این نتیجه خود همین صفحه و شماره سفارش آن است.",
                "cta_url": reverse("core:contact"),
                "cta_label": "تماس با تیم",
            }
        )

    timeline_items = []
    for transaction in order.transactions.order_by("created_at"):
        accent = "neutral"
        if transaction.status == PaymentTransaction.VERIFIED:
            accent = "success"
        elif transaction.status == PaymentTransaction.FAILED:
            accent = "failed"
        timeline_items.append(
            {
                "title": f"{transaction.get_status_display()} - {transaction.provider}",
                "description": f"Authority: {transaction.authority or '-'}",
                "state_label": transaction.get_status_display(),
                "accent": accent,
                "at": _format_dt(transaction.created_at),
                "meta": f"Ref: {transaction.reference_id}" if transaction.reference_id else "",
            }
        )

    return {
        "payment_status_key": status_key,
        "payment_status_short_label": short_label,
        "payment_status_secondary_badge": order.plan.name,
        "payment_status_meta_items": [
            {"label": "شماره سفارش", "value": f"#{order.id}"},
            {"label": "تاریخ ثبت", "value": _format_dt(order.created_at)},
            {"label": "وضعیت", "value": order.get_status_display()},
            {"label": "مرجع", "value": reference_label or "ثبت نشده"},
        ],
        "payment_order_context_label": f"سفارش #{order.id}",
        "payment_order_plan_name": order.plan.name,
        "payment_order_description": order.description,
        "payment_order_summary_items": [
            {"label": "پلن", "value": order.plan.name},
            {"label": "مبلغ", "value": f"{_format_amount(order.amount)} تومان"},
            {"label": "وضعیت فعلی", "value": order.get_status_display()},
            {"label": "آخرین مرجع", "value": reference_label or "ثبت نشده"},
        ],
        "payment_order_snapshot_label": "مرور سفارش",
        "payment_order_amount": _format_amount(order.amount),
        "payment_order_currency_label": "تومان",
        "payment_timeline_items": timeline_items,
        "payment_next_actions": payment_next_actions,
        "payment_support_cta_url": reverse("core:contact"),
        "payment_support_cta_label": "تماس با تیم",
        "payment_help_cta_url": reverse("ai_platform:billing"),
        "payment_help_cta_label": "مرکز اشتراک",
    }


def build_assistant_sections():
    return [
        {
            "key": "all",
            "label": "دستیارها",
            "title": "فهرست دستیارها",
            "caption": "سطح v1.5 برای دستیارها فعال شده است، اما در این پروژه هنوز منبع داده‌ای برای پروفایل‌های دستیار تعریف نشده.",
            "count": 0,
            "assistants": [],
            "empty_title": "هنوز دستیار قابل‌نمایشی در بک‌اند این پروژه وجود ندارد",
            "empty_body": "قالب زنده شده است، اما مدل داده دستیارها هنوز به این پروژه وصل نشده و برای همین فهرست فعلاً خالی می‌ماند.",
            "empty_hint": "وقتی منبع داده دستیارها اضافه شود، همین مسیر بدون ساخت UI موازی آماده استفاده است.",
        }
    ]


def build_memory_page_context(request, subscription):
    current_plan_label = subscription.plan.name if subscription else ""
    if not subscription:
        state = "locked"
        blocked = {
            "title": "حافظه برای این حساب هنوز به پلن فعال متصل نیست",
            "body": "در این پروژه حافظه از سطح اشتراک خوانده می‌شود. تا قبل از داشتن پلن فعال، چیزی در این مرکز ذخیره یا نمایش داده نمی‌شود.",
            "primary_url": reverse("core:pricing"),
            "primary_label": "مرور پلن‌ها",
            "secondary_url": reverse("accounts:profile"),
            "secondary_label": "پروفایل",
        }
    elif not request.user.memory_enabled:
        state = "disabled"
        blocked = {
            "title": "حافظه در سطح حساب خاموش است",
            "body": "قالب v1.5 فعال است، اما چون خود گزینه حافظه در حساب شما خاموش مانده، مرکز حافظه چیزی برای نمایش ندارد.",
            "primary_url": reverse("accounts:profile"),
            "primary_label": "مدیریت ترجیحات",
            "secondary_url": reverse("ai_platform:chat"),
            "secondary_label": "بازگشت به گفتگو",
        }
    else:
        state = "active"
        blocked = {}

    return {
        "memory_state": state,
        "memory_blocked": blocked,
        "memory_groups": [],
        "memory_can_clear": False,
        "memory_scope_label": "حساب شخصی",
        "memory_scope": {
            "title": "حافظه حساب شخصی",
            "summary": "این مرکز فقط حافظه‌های صریح و قابل‌مدیریت را نمایش می‌دهد. در این پروژه هنوز آیتم ذخیره‌شده‌ای برای نمایش وجود ندارد.",
            "state": "active" if state == "active" else state,
            "scope_label": "حساب شخصی",
            "workspace_label": "فضای شخصی",
            "plan_label": current_plan_label,
            "visibility_note": "هر چیزی که بعداً در این مرکز ذخیره شود باید از همین‌جا قابل مشاهده و حذف باشد.",
            "control_note": "فعلاً فقط وضعیت فعال‌بودن و آمادگی این سطح به‌صورت زنده سیم‌کشی شده است.",
            "privacy_note": "تا وقتی چیزی صریحاً در حافظه ثبت نشده باشد، این مرکز خالی می‌ماند.",
        },
    }
