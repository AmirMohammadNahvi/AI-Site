from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.forms import PersonalizationForm
from billing.services import consume_tokens, get_active_subscription
from core.models import FAQItem, SiteSetting

from .forms import ChatMessageForm
from .models import AIModel, AIModelCapability, Conversation
from .services import AIAdapterError, AIAdapterService, build_attachment_payload, persist_exchange


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


def model_detail(request, slug):
    model = get_object_or_404(AIModel, slug=slug, is_active=True)
    return render(request, "ai_platform/model_detail.html", {"model_obj": model})


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
                    return redirect("dashboard:billing")
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
    active_conversations = conversation_queryset.filter(is_archived=False)[:50]
    archived_conversations = conversation_queryset.filter(is_archived=True)[:50]
    subscription = get_active_subscription(request.user) if request.user.is_authenticated else None
    personalization_form = PersonalizationForm(instance=request.user) if request.user.is_authenticated else None
    payment_history = request.user.orders.select_related("plan")[:10] if request.user.is_authenticated else []

    return render(
        request,
        "ai_platform/chat.html",
        {
            "hide_site_chrome": True,
            "form": form,
            "conversation": conversation,
            "conversations": active_conversations,
            "archived_conversations": archived_conversations,
            "active_models": active_models,
            "selected_model_id": str(
                form["model"].value()
                or (conversation.model.id if conversation else "")
                or (initial_model.id if initial_model else "")
            ),
            "subscription": subscription,
            "payment_history": payment_history,
            "personalization_form": personalization_form,
            "faq_items": FAQItem.objects.filter(is_active=True)[:8],
        },
    )


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
