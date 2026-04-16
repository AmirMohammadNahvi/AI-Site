from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.forms import ProfileForm
from ai_platform.forms import AIModelForm
from ai_platform.models import AIModel, AIModelCapability
from billing.forms import PlanForm
from billing.models import PaymentTransaction, Plan
from core.forms import SiteSettingForm, TextSnippetForm
from core.models import ContactMessage, SiteSetting, TextSnippet


@login_required
def home(request):
    return redirect("ai_platform:chat")


@login_required
def billing_overview(request):
    return redirect("ai_platform:billing")


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "پروفایل شما ذخیره شد.")
        return redirect("dashboard:profile")
    return render(request, "dashboard/profile.html", {"form": form})


@staff_member_required
def admin_home(request):
    return render(
        request,
        "dashboard/admin_home.html",
        {
            "user_count": request.user.__class__.objects.count(),
            "model_count": AIModel.objects.count(),
            "plan_count": Plan.objects.count(),
            "transaction_count": PaymentTransaction.objects.count(),
            "contact_count": ContactMessage.objects.filter(is_reviewed=False).count(),
        },
    )


@staff_member_required
def settings_edit(request):
    settings_obj = SiteSetting.get_solo()
    form = SiteSettingForm(request.POST or None, request.FILES or None, instance=settings_obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "تنظیمات سایت ذخیره شد.")
        return redirect("dashboard:admin_settings")
    return render(request, "dashboard/settings_form.html", {"form": form})


@staff_member_required
def text_list(request):
    snippets = TextSnippet.objects.all()
    query = request.GET.get("q", "").strip()
    if query:
        snippets = snippets.filter(Q(title__icontains=query) | Q(key__icontains=query) | Q(text__icontains=query))
    return render(request, "dashboard/text_list.html", {"snippets": snippets, "query": query})


@staff_member_required
def text_edit(request, pk=None):
    instance = get_object_or_404(TextSnippet, pk=pk) if pk else None
    form = TextSnippetForm(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "متن سایت با موفقیت ذخیره شد.")
        return redirect("dashboard:admin_texts")
    return render(request, "dashboard/text_form.html", {"form": form, "instance": instance})


def _save_capabilities(model, form):
    capability_map = {
        AIModelCapability.TEXT: form.cleaned_data.get("text_enabled"),
        AIModelCapability.IMAGE_INPUT: form.cleaned_data.get("image_enabled"),
        AIModelCapability.FILE_INPUT: form.cleaned_data.get("file_enabled"),
    }
    for capability, enabled in capability_map.items():
        obj, _ = AIModelCapability.objects.get_or_create(model=model, capability_type=capability)
        obj.is_enabled = bool(enabled)
        obj.save(update_fields=["is_enabled", "updated_at"])


@staff_member_required
def model_list(request):
    return render(request, "dashboard/model_list.html", {"models": AIModel.objects.all()})


@staff_member_required
def model_edit(request, pk=None):
    instance = get_object_or_404(AIModel, pk=pk) if pk else None
    initial = {}
    if instance:
        initial = {
            "text_enabled": instance.has_capability(AIModelCapability.TEXT),
            "image_enabled": instance.has_capability(AIModelCapability.IMAGE_INPUT),
            "file_enabled": instance.has_capability(AIModelCapability.FILE_INPUT),
        }
    form = AIModelForm(request.POST or None, instance=instance, initial=initial)
    if request.method == "POST" and form.is_valid():
        model = form.save()
        _save_capabilities(model, form)
        messages.success(request, "مدل با موفقیت ذخیره شد.")
        return redirect("dashboard:admin_models")
    return render(request, "dashboard/model_form.html", {"form": form, "instance": instance})


@staff_member_required
def plan_list(request):
    return render(request, "dashboard/plan_list.html", {"plans": Plan.objects.all()})


@staff_member_required
def plan_edit(request, pk=None):
    instance = get_object_or_404(Plan, pk=pk) if pk else None
    form = PlanForm(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "پلن با موفقیت ذخیره شد.")
        return redirect("dashboard:admin_plans")
    return render(request, "dashboard/plan_form.html", {"form": form, "instance": instance})


@staff_member_required
def transactions(request):
    return render(
        request,
        "dashboard/transactions.html",
        {"transactions": PaymentTransaction.objects.select_related("order", "order__user", "order__plan")[:50]},
    )
