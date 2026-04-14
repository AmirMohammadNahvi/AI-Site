from django.urls import reverse

from . import app_ui as legacy_app_ui


def _with_defaults(payload, defaults):
    merged = defaults.copy()
    merged.update(payload)
    return merged


def _format_amount(value):
    if value in (None, ""):
        return "-"
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


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
                "primary_cta_label": "View plans",
                "secondary_cta_url": reverse("core:contact"),
                "secondary_cta_label": "Contact team",
            },
            defaults,
        )

    order_reference = f"#{latest_order.id}" if latest_order else ""
    return _with_defaults(
        {
            "badge": "Active plan",
            "name": subscription.plan.name,
            "title": subscription.plan.name,
            "description": subscription.plan.description or "Review the active plan details from this card.",
            "summary": subscription.plan.description or "This plan is active for the current account.",
            "price_label": f"{_format_amount(subscription.plan.price)} Toman",
            "cycle_label": f"{subscription.plan.duration_days} days",
            "status_label": "Active",
            "started_at_label": legacy_app_ui._format_dt(subscription.starts_at),
            "expires_at_label": legacy_app_ui._format_dt(subscription.ends_at),
            "started_at_note": "Current plan start time",
            "expires_at_note": "If no new order is created, the plan ends at this time.",
            "order_reference": order_reference or "Current active order",
            "renewal_label": "Manual renewal",
            "renewal_note": "A new order is required to continue after expiry.",
            "helper_text": "Public pricing is for comparison; this card reflects the current account state.",
            "primary_cta_url": reverse("core:pricing"),
            "primary_cta_label": "Compare plans",
            "secondary_cta_url": reverse("ai_platform:chat"),
            "secondary_cta_label": "Back to chat",
        },
        defaults,
    )


def build_app_shell_context(request, *args, **kwargs):
    context = legacy_app_ui.build_app_shell_context(request, *args, **kwargs)
    latest_order = None
    if request.user.is_authenticated:
        latest_order = request.user.orders.select_related("plan").first()
    context["current_plan"] = build_current_plan_context(context.get("subscription"), latest_order=latest_order)
    return context


def build_billing_activity_items(orders):
    defaults = {
        "title": "",
        "plan_name": "",
        "subtitle": "",
        "description": "",
        "status_label": "",
        "status_tone": "",
        "created_at_label": "",
        "reference_label": "",
        "type_label": "",
        "amount_label": "",
        "detail_url": "",
        "detail_label": "",
    }
    items = legacy_app_ui.build_billing_activity_items(orders)
    normalized = []
    for item in items:
        plan_name = item.get("plan_name") or item.get("title", "")
        normalized.append(_with_defaults({"plan_name": plan_name}, _with_defaults(item, defaults)))
    return normalized


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
    summary = model.summary or model.description or "Ready for everyday use in FaralYar conversations."
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
        "detail_back_label": "Back to model catalog",
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
            "initials": legacy_app_ui._initials(model.name, fallback="AI"),
            "family_label": model.provider_label,
            "summary": summary,
            "fit_statement": model.description or summary,
            "availability_state": "available",
            "availability_label": "Available",
            "availability_note": "You can select this model from the current chat flow.",
            "availability_headline": "Available in the current chat flow",
            "workspace_label": "Personal space",
            "capabilities": capabilities,
            "badges": capabilities,
            "detail_url": reverse("ai_platform:model_detail", args=[model.slug]),
            "detail_label": "Model details",
            "primary_cta_url": reverse("ai_platform:chat"),
            "primary_cta_label": "Start chat",
            "secondary_cta_url": reverse("ai_platform:chat"),
            "secondary_cta_label": "Back to chat",
            "model_use_context": {
                "state": "available",
                "primary_cta_url": reverse("ai_platform:chat"),
                "primary_cta_label": "Start chat with this model",
                "secondary_cta_url": reverse("ai_platform:models"),
                "secondary_cta_label": "Back to model list",
                "reason": "The final model choice is still made when sending a chat message.",
            },
        },
        model_defaults,
    )
