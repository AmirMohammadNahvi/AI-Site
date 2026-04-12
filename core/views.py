from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from ai_platform.models import AIModel
from billing.models import Plan
from blog.models import BlogPost

from .forms import ContactForm
from .models import FAQItem, SiteSetting, StaticPage


DEFAULT_PAGE_CONTENT = {
    "about": "فارال یار دستیار هوش مصنوعی تیم فارال است؛ یک تجربه فارسی‌محور برای گفتگو با مدل‌های متنوع، مدیریت اشتراک و محتوای آموزشی.",
    "terms": "استفاده از خدمات FaralYar به معنای پذیرش قوانین، حفظ امنیت حساب کاربری و رعایت استفاده مسئولانه از ابزارهای هوش مصنوعی است.",
    "privacy": "FaralYar داده‌های لازم برای ارائه خدمات را نگهداری می‌کند و از اطلاعات کاربران برای اجرای سرویس، مدیریت حساب و امنیت استفاده می‌شود.",
    "faq": "در این بخش می‌توانید سوالات پرتکرار درباره پلن‌ها، محدودیت پیام، روش پرداخت و استفاده از مدل‌ها را ببینید.",
}


def home(request):
    context = {
        "featured_models": AIModel.objects.filter(is_active=True, is_featured=True)[:6],
        "plans": Plan.objects.filter(is_active=True)[:3],
        "featured_posts": BlogPost.objects.filter(status=BlogPost.PUBLISHED)[:3],
        "faqs": FAQItem.objects.filter(is_active=True)[:6],
    }
    return render(request, "core/home.html", context)


def pricing(request):
    return render(
        request,
        "core/pricing.html",
        {"plans": Plan.objects.filter(is_active=True).prefetch_related("allowed_models")},
    )


def static_page(request, page_key):
    page, _ = StaticPage.objects.get_or_create(
        page_key=page_key,
        defaults={
            "title": dict(StaticPage.PAGE_CHOICES).get(page_key, page_key),
            "body": DEFAULT_PAGE_CONTENT.get(page_key, ""),
        },
    )
    if page_key == StaticPage.FAQ:
        return render(request, "core/faq.html", {"page": page, "faqs": FAQItem.objects.filter(is_active=True)})
    return render(request, "core/static_page.html", {"page": page})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "پیام شما ثبت شد. به زودی با شما تماس می‌گیریم.")
            return redirect("core:contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})


@require_POST
def set_theme(request):
    theme = request.POST.get("theme", "system")
    if theme in {"light", "dark", "system"}:
        request.session["theme"] = theme
        if request.user.is_authenticated:
            request.user.theme_preference = theme
            request.user.save(update_fields=["theme_preference", "updated_at"])
    return redirect(request.META.get("HTTP_REFERER", "core:home"))
