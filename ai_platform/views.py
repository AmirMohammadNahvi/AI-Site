from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from accounts.forms import PersonalizationForm
from billing.services import consume_tokens, get_active_subscription
from core.models import FAQItem, SiteSetting

from .app_ui import (
    build_assistant_sections,
    build_billing_recommendation_context,
    build_billing_usage_context,
    build_memory_page_context,
    build_memory_scope_inline,
)
from .forms import ChatMessageForm
from .models import AIModel, AIModelCapability, Conversation
from .services import AIAdapterError, AIAdapterService, build_attachment_payload, persist_exchange
from .stable_app_ui import build_app_shell_context, build_billing_activity_items, build_current_plan_context, serialize_model


def _ensure_session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


def _can_guest_continue(request):
    settings_obj = SiteSetting.get_solo()
    used = request.session.get("guest_messages_used", 0)
    return used < settings_obj.free_guest_message_limit


def _increment_guest_usage(request):
    request.session["guest_messages_used"] = request.session.get("guest_messages_used", 0) + 1


def _conversation_queryset(request):
    if request.user.is_authenticated:
        return Conversation.objects.filter(user=request.user).select_related("model")
    return Conversation.objects.filter(guest_session_key=_ensure_session_key(request)).select_related("model")


def _get_conversation_for_request(request, conversation_id):
    queryset = _conversation_queryset(request)
    return get_object_or_404(queryset, id=conversation_id)


def _conversation_template_context(
    request,
    *,
    form,
    conversation,
    archived_conversations,
    subscription,
    payment_history,
):
    latest_order = payment_history.first() if hasattr(payment_history, "first") else None
    context = build_app_shell_context(
        request,
        active_nav="chat",
        page_title=conversation.title if conversation and conversation.title else "گفتگو",
        page_description="جریان زنده گفت‌وگو در سطح v1.5.",
        page_eyebrow="گفت‌وگوی زنده",
    )
    context.update(
        {
            "conversation": conversation,
            "conversation_title": conversation.title if conversation and conversation.title else "گفت‌وگوی جدید",
            "conversation_space_name": "گفت‌وگوی شخصی",
            "conversation_messages": [
                {
                    "role": message.role,
                    "label": message.get_role_display(),
                    "role_label": message.get_role_display(),
                    "content": message.content,
                    "html": "",
                    "is_user": message.role == "user",
                    "attachment": message.attachment,
                    "attachment_url": message.attachment.url if message.attachment else "",
                    "attachment_label": message.attachment.name if message.attachment else "",
                }
                for message in (conversation.messages.all() if conversation else [])
            ],
            "conversation_is_archived": bool(conversation and conversation.is_archived),
            "conversation_archive_url": reverse("ai_platform:chat_archive", args=[conversation.id])
            if conversation and request.user.is_authenticated and not conversation.is_archived
            else "",
            "conversation_restore_url": reverse("ai_platform:chat_restore", args=[conversation.id])
            if conversation and request.user.is_authenticated and conversation.is_archived
            else "",
            "conversation_next_url": request.get_full_path(),
            "conversation_updated_label": conversation.updated_at.strftime("%Y/%m/%d %H:%M") if conversation else "",
            "conversation_entry_context": {
                "state": "available",
                "title": "اگر می‌خواهید موضوع تازه‌ای را جدا نگه دارید",
                "body": "برای ادامه همین گفتگو از همین صفحه استفاده کنید. اگر موضوع تازه‌ای دارید، گفت‌وگوی جدید را از مسیر اصلی شروع کنید.",
                "current_cta_url": reverse("ai_platform:chat_detail", args=[conversation.id]),
                "current_cta_label": "ادامه همین گفتگو",
                "current_note": "برای ادامه همان رشته فعال",
                "new_cta_url": reverse("ai_platform:chat"),
                "new_cta_label": "گفت‌وگوی جدید",
                "new_note": "برای موضوع تازه",
            }
            if conversation
            else None,
            "space": {"name": "گفت‌وگوی شخصی"},
            "composer_action": request.get_full_path(),
            "composer_hidden_fields": [form["conversation_id"], form["model"]],
            "composer_prompt_name": form["prompt"].name,
            "composer_prompt_value": form["prompt"].value() or "",
            "composer_prompt_errors": form.errors.get("prompt", []),
            "composer_attachment_name": form["attachment"].name,
            "composer_submit_label": "ارسال پیام",
            "composer_memory_scope_inline": build_memory_scope_inline(request, subscription=subscription),
            "memory_scope_inline": build_memory_scope_inline(request, subscription=subscription),
            "memory_save_prompt": {
                "scope_label": "حساب شخصی",
                "title": "مدیریت حافظه از مرکز حافظه انجام می‌شود",
                "body": "در این pass، سطح v1.5 حافظه زنده شده است و وضعیت آن از مرکز حافظه و تنظیمات حساب شما خوانده می‌شود.",
                "primary_url": reverse("ai_platform:memory"),
                "primary_label": "مرکز حافظه",
            }
            if request.user.is_authenticated
            else None,
            "archived_conversation_items": [
                {
                    "id": item.id,
                    "title": item.title or "گفت‌وگوی بدون عنوان",
                    "url": reverse("ai_platform:chat_detail", args=[item.id]),
                    "restore_url": reverse("ai_platform:chat_restore", args=[item.id]),
                    "archived_label": item.updated_at.strftime("%Y/%m/%d %H:%M"),
                    "space_name": "گفت‌وگوی شخصی",
                    "assistant_label": item.model.name if item.model_id else "",
                }
                for item in archived_conversations
            ],
            "archived_list_next_url": request.get_full_path(),
            "active_archived_conversation_id": conversation.id if conversation and conversation.is_archived else None,
            "subscription": subscription,
            "payment_history": payment_history,
            "personalization_form": PersonalizationForm(instance=request.user) if request.user.is_authenticated else None,
            "faq_items": FAQItem.objects.filter(is_active=True)[:8],
            "current_plan": build_current_plan_context(subscription, latest_order=latest_order),
        }
    )
    return context


def model_index(request):
    active_models = list(AIModel.objects.filter(is_active=True).prefetch_related("capabilities"))
    featured_models = [serialize_model(model) for model in active_models if model.is_featured]
    remaining_models = [serialize_model(model) for model in active_models if not model.is_featured]
    context = build_app_shell_context(
        request,
        active_nav="models",
        page_title="مدل‌ها",
        page_description="کاتالوگ زنده مدل‌های فعال FaralYar.",
        page_eyebrow="کاتالوگ مدل‌ها",
    )
    context["models"] = [serialize_model(model) for model in active_models]
    context["model_groups"] = [
        {
            "key": "featured",
            "title": "مدل‌های پیشنهادی",
            "eyebrow": "شروع سریع",
            "caption": "مدل‌هایی که در خود محصول برای شروع و مقایسه اولیه زودتر دیده می‌شوند.",
            "models": featured_models,
        },
        {
            "key": "all",
            "title": "سایر مدل‌های فعال",
            "eyebrow": "فهرست کامل",
            "caption": "سایر مدل‌های فعالی که در همین پروژه قابل استفاده هستند.",
            "models": remaining_models,
        },
    ]
    return render(request, "app/models/index.html", context)


def model_detail(request, slug):
    model = get_object_or_404(AIModel.objects.prefetch_related("capabilities"), slug=slug, is_active=True)
    subscription = get_active_subscription(request.user) if request.user.is_authenticated else None
    serialized_model = serialize_model(model)
    context = build_app_shell_context(
        request,
        active_nav="models",
        page_title="جزئیات مدل",
        page_description="مرور تناسب، قابلیت‌ها و وضعیت استفاده مدل در سطح v1.5.",
        page_eyebrow="کاتالوگ مدل‌ها",
    )
    context["model"] = serialized_model
    context["model_use_context"] = serialized_model.get("model_use_context")
    context["current_plan"] = build_current_plan_context(subscription)
    context["conversation_entry_context"] = {
        "state": "available",
        "current_cta_url": reverse("ai_platform:chat"),
        "current_cta_label": "بازگشت به گفتگو",
        "current_note": "برای انتخاب مدل هنگام ارسال پیام",
    }
    return render(request, "app/models/detail.html", context)


@login_required
def assistants_index(request):
    context = build_app_shell_context(
        request,
        active_nav="assistants",
        page_title="دستیارها",
        page_description="سطح v1.5 دستیارها فعال شده است.",
        page_eyebrow="پروفایل‌های کاری",
        page_notice="صفحه v1.5 دستیارها اکنون زنده است، اما این پروژه هنوز منبع داده‌ای برای موجودیت دستیار ندارد؛ بنابراین سطح زنده‌شده به‌صورت شفاف در حالت خالی رندر می‌شود.",
    )
    context["assistant_sections"] = build_assistant_sections()
    context["assistants_total_count"] = 0
    context["assistants_active_tab"] = "all"
    context["assistants_can_create"] = False
    return render(request, "app/assistants/index.html", context)


@login_required
def memory_index(request):
    subscription = get_active_subscription(request.user)
    context = build_app_shell_context(
        request,
        active_nav="memory",
        page_title="مرکز حافظه",
        page_description="مرور وضعیت حافظه در سطح v1.5.",
        page_eyebrow="کنترل حافظه",
    )
    context.update(build_memory_page_context(request, subscription))
    return render(request, "app/memory/index.html", context)


@login_required
def billing_index(request):
    subscription = get_active_subscription(request.user)
    quota_window = None
    if subscription:
        from billing.services import get_or_create_quota_window

        quota_window = get_or_create_quota_window(subscription)
    orders = request.user.orders.select_related("plan")
    context = build_app_shell_context(
        request,
        active_nav="billing",
        page_title="اشتراک و پرداخت",
        page_description="مرجع زنده وضعیت اشتراک، سهمیه و سفارش‌های اخیر.",
        page_eyebrow="مرکز اشتراک",
    )
    context["current_plan"] = build_current_plan_context(subscription, latest_order=orders.first())
    context["billing_usage"] = build_billing_usage_context(subscription, quota_window)
    context["billing_activity_items"] = build_billing_activity_items(orders[:20])
    context["billing_recommendation"] = build_billing_recommendation_context(request, subscription, quota_window)
    return render(request, "app/billing/index.html", context)


def chat_view(request, conversation_id=None):
    active_models = AIModel.objects.filter(is_active=True).prefetch_related("capabilities")
    initial_model = active_models.first()
    conversation = None

    if conversation_id:
        conversation = _get_conversation_for_request(request, conversation_id)

    form = ChatMessageForm(request.POST or None, request.FILES or None)
    form.fields["model"].queryset = active_models
    if conversation and request.method != "POST":
        form.fields["model"].initial = conversation.model
        form.fields["conversation_id"].initial = conversation.id
    elif initial_model and request.method != "POST":
        form.fields["model"].initial = initial_model

    if request.method == "POST" and form.is_valid():
        model = form.cleaned_data["model"]
        prompt = form.cleaned_data["prompt"]
        attachment = form.cleaned_data.get("attachment")
        form_conversation_id = form.cleaned_data.get("conversation_id")

        if form_conversation_id:
            conversation = _get_conversation_for_request(request, form_conversation_id)
            if conversation.is_archived:
                conversation.is_archived = False
                conversation.save(update_fields=["is_archived", "updated_at"])
        else:
            conversation = Conversation.objects.create(
                user=request.user if request.user.is_authenticated else None,
                guest_session_key="" if request.user.is_authenticated else _ensure_session_key(request),
                model=model,
            )

        if attachment:
            is_image = attachment.content_type.startswith("image/") if getattr(attachment, "content_type", "") else False
            needed_capability = AIModelCapability.IMAGE_INPUT if is_image else AIModelCapability.FILE_INPUT
            if not model.has_capability(needed_capability):
                messages.error(request, "این مدل از این نوع فایل پشتیبانی نمی‌کند.")
                return redirect("ai_platform:chat_detail", conversation_id=conversation.id)

        if request.user.is_authenticated:
            subscription = get_active_subscription(request.user)
            if subscription:
                success, window = consume_tokens(subscription, amount=1)
                if not success:
                    messages.error(request, "سهمیه این بازه زمانی شما تمام شده است.")
                    return redirect("ai_platform:billing")
            else:
                if not _can_guest_continue(request):
                    messages.error(request, "برای ادامه استفاده لطفاً پلن تهیه کنید.")
                    return redirect("core:pricing")
                _increment_guest_usage(request)
        else:
            if not _can_guest_continue(request):
                messages.error(request, "پیام‌های رایگان شما تمام شده است. لطفاً ثبت‌نام کنید یا پلن بخرید.")
                return redirect("accounts:signup")
            _increment_guest_usage(request)

        try:
            reply, raw_data = AIAdapterService.run(
                conversation,
                prompt,
                attachment_payload=build_attachment_payload(attachment),
            )
            _, assistant_message = persist_exchange(conversation, prompt, reply, attachment=attachment)
            assistant_message.metadata = raw_data
            assistant_message.save(update_fields=["metadata", "updated_at"])
        except Exception as exc:
            if isinstance(exc, AIAdapterError):
                messages.error(request, str(exc))
            else:
                messages.error(request, f"خطا در ارتباط با مدل: {exc}")
        return redirect("ai_platform:chat_detail", conversation_id=conversation.id)

    conversation_queryset = _conversation_queryset(request)
    archived_conversations = conversation_queryset.filter(is_archived=True)[:50]
    subscription = get_active_subscription(request.user) if request.user.is_authenticated else None
    payment_history = request.user.orders.select_related("plan")[:10] if request.user.is_authenticated else []

    context = _conversation_template_context(
        request,
        form=form,
        conversation=conversation,
        archived_conversations=archived_conversations,
        subscription=subscription,
        payment_history=payment_history,
    )
    return render(request, "app/conversations/detail.html", context)


@login_required
@require_POST
def conversation_archive(request, conversation_id):
    conversation = _get_conversation_for_request(request, conversation_id)
    conversation.is_archived = True
    conversation.save(update_fields=["is_archived", "updated_at"])
    messages.success(request, "گفتگو آرشیو شد.")
    return redirect(request.POST.get("next") or "ai_platform:chat")


@login_required
@require_POST
def conversation_restore(request, conversation_id):
    conversation = _get_conversation_for_request(request, conversation_id)
    conversation.is_archived = False
    conversation.save(update_fields=["is_archived", "updated_at"])
    messages.success(request, "گفتگو از آرشیو خارج شد.")
    return redirect(request.POST.get("next") or "ai_platform:chat")


@login_required
@require_POST
def conversation_delete(request, conversation_id):
    conversation = _get_conversation_for_request(request, conversation_id)
    conversation.delete()
    messages.success(request, "گفتگو حذف شد.")
    return redirect(request.POST.get("next") or "ai_platform:chat")
