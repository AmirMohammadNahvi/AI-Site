from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from ai_platform.models import Conversation
from billing.services import get_active_subscription

from .forms import LoginForm, OTPRequestForm, OTPVerifyForm, PersonalizationForm, ProfileForm, SignUpForm
from .models import OTPRequest, User
from .services import OTPService


def _make_mobile_email(mobile):
    return f"{slugify(mobile)}@otp.faralyar.local"


def _get_safe_next_url(request):
    next_url = request.POST.get("next") or request.GET.get("next") or ""
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return next_url
    return ""


def _mask_mobile(mobile):
    if not mobile:
        return ""
    raw_mobile = str(mobile).strip()
    if len(raw_mobile) < 6:
        return raw_mobile
    if len(raw_mobile) < 10:
        return f"{raw_mobile[:3]} *** {raw_mobile[-2:]}"
    return f"{raw_mobile[:4]} *** ** {raw_mobile[-2:]}"


def _build_otp_context(mobile=""):
    return {
        "otp_code_length": settings.OTP_CODE_LENGTH,
        "otp_expiry_minutes": settings.OTP_EXPIRY_MINUTES,
        "otp_phone_masked": _mask_mobile(mobile),
    }


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("ai_platform:chat")

    next_url = _get_safe_next_url(request)
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            OTPService.send_email_welcome(user)
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(request, "حساب شما با موفقیت ساخته شد.")
            return redirect(next_url or "ai_platform:chat")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form, "next_url": next_url})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("ai_platform:chat")

    next_url = _get_safe_next_url(request)
    form = LoginForm(request=request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.user, backend="faralyar_project.auth_backends.EmailOrMobileBackend")
        messages.success(request, "با موفقیت وارد شدید.")
        return redirect(next_url or "ai_platform:chat")

    return render(request, "accounts/login.html", {"form": form, "next_url": next_url})


def otp_request_view(request):
    if request.user.is_authenticated:
        return redirect("ai_platform:chat")

    next_url = _get_safe_next_url(request)
    form = OTPRequestForm(request.POST or None)
    provider_ready = OTPService.is_provider_configured() or settings.DEBUG

    if request.method == "POST":
        if not provider_ready:
            messages.error(request, "ورود با موبایل در حال حاضر فعال نیست.")
            return redirect("accounts:login")
        if form.is_valid():
            mobile = form.cleaned_data["mobile"]
            otp_request, code = OTPService.send_code(mobile)
            request.session["otp_mobile"] = mobile
            if next_url:
                request.session["otp_next_url"] = next_url
            if settings.DEBUG:
                messages.info(request, f"کد تست: {code}")
            messages.success(request, "کد تایید ارسال شد.")
            return redirect("accounts:otp_verify")

    context = {"form": form, "provider_ready": provider_ready, "next_url": next_url, "otp_error_note": ""}
    context.update(_build_otp_context())
    return render(request, "accounts/otp_request.html", context)


def otp_verify_view(request):
    mobile = request.session.get("otp_mobile", "")
    next_url = request.session.get("otp_next_url", "")
    otp_error_note = ""
    if not mobile:
        return redirect("accounts:otp_request")

    form = OTPVerifyForm(request.POST or None, initial={"mobile": mobile})
    if request.method == "POST" and form.is_valid():
        mobile = form.cleaned_data["mobile"]
        code = form.cleaned_data["code"]
        otp_request = OTPRequest.objects.filter(mobile=mobile, is_used=False).order_by("-created_at").first()
        if otp_request and otp_request.verify(code):
            user, created = User.objects.get_or_create(
                mobile=mobile,
                defaults={
                    "email": _make_mobile_email(mobile),
                    "full_name": f"کاربر {mobile[-4:]}",
                },
            )
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            request.session.pop("otp_mobile", None)
            request.session.pop("otp_next_url", None)
            if created:
                messages.success(request, "حساب شما از طریق موبایل ساخته شد.")
            else:
                messages.success(request, "با موفقیت وارد شدید.")
            return redirect(next_url or "ai_platform:chat")
        otp_error_note = "کد واردشده معتبر نیست یا زمان اعتبار آن گذشته است. آخرین کد دریافتی را بررسی کنید یا دوباره کد تازه بگیرید."
        messages.error(request, "کد واردشده معتبر نیست یا منقضی شده است.")

    context = {"form": form, "mobile": mobile, "next_url": next_url, "otp_error_note": otp_error_note}
    context.update(_build_otp_context(mobile))
    return render(request, "accounts/otp_verify.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "از حساب خود خارج شدید.")
    return redirect("core:home")


@login_required
def profile_view(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        if not get_active_subscription(request.user):
            form.instance.memory_enabled = False
        form.save()
        messages.success(request, "اطلاعات حساب شما به روزرسانی شد.")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {"form": form})


@login_required
@require_POST
def personalization_view(request):
    form = PersonalizationForm(request.POST, instance=request.user)
    if form.is_valid():
        if not get_active_subscription(request.user):
            form.instance.memory_enabled = False
        form.save()
        messages.success(request, "شخصی سازی حساب شما ذخیره شد.")
    else:
        messages.error(request, "ذخیره شخصی سازی انجام نشد. لطفاً فیلدها را بررسی کنید.")
    return redirect(request.POST.get("next") or "ai_platform:chat")


@login_required
@require_POST
def settings_action_view(request):
    action = request.POST.get("action")
    next_url = request.POST.get("next") or "ai_platform:chat"

    if action == "delete_all_conversations":
        Conversation.objects.filter(user=request.user).delete()
        messages.success(request, "تمام گفتگوهای شما حذف شد.")
        return redirect(next_url)

    if action == "logout_all_devices":
        request.user.invalidate_all_sessions()
        logout(request)
        messages.success(request, "از تمام دستگاه ها خارج شدید.")
        return redirect("core:home")

    messages.error(request, "درخواست نامعتبر بود.")
    return redirect(next_url)
