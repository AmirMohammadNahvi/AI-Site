from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSetting(TimeStampedModel):
    site_name_fa = models.CharField(max_length=120, default="فارال یار")
    site_name_en = models.CharField(max_length=120, default="FaralYar")
    tagline = models.CharField(max_length=240, default="دستیار هوش مصنوعی تیم فارال")
    hero_title = models.CharField(max_length=240, default="دستیار هوش مصنوعی فارسی برای تیم‌ها و کاربران حرفه‌ای")
    hero_subtitle = models.TextField(
        default="FaralYar محیطی مدرن برای گفتگو با مدل‌های مختلف هوش مصنوعی، مدیریت اشتراک، محتوای آموزشی و تجربه‌ای روان روی موبایل و دسکتاپ است."
    )
    support_email = models.EmailField(blank=True)
    support_phone = models.CharField(max_length=32, blank=True)
    address = models.CharField(max_length=255, blank=True)
    telegram_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    x_url = models.URLField(blank=True)
    light_logo = models.CharField(max_length=255, default="branding/faralyar-main.png")
    dark_logo = models.CharField(max_length=255, default="branding/farayarl-white.png")
    mono_dark_logo = models.CharField(max_length=255, default="branding/faralyar-black.png")
    mono_light_logo = models.CharField(max_length=255, default="branding/farayarl-white.png")
    green_logo = models.CharField(max_length=255, default="branding/faralyar-green.png")
    blue_logo = models.CharField(max_length=255, default="branding/faralyar-blue.png")
    primary_color = models.CharField(max_length=7, default="#28ab88")
    secondary_color = models.CharField(max_length=7, default="#013366")
    otp_provider_name = models.CharField(max_length=80, blank=True)
    otp_provider_api_key = models.CharField(max_length=255, blank=True)
    otp_provider_sender = models.CharField(max_length=120, blank=True)
    zarinpal_merchant_id = models.CharField(max_length=255, blank=True)
    zarinpal_sandbox = models.BooleanField(default=True)
    payment_guide_text = models.TextField(blank=True)
    payment_guide_url = models.URLField(blank=True)
    free_guest_message_limit = models.PositiveSmallIntegerField(default=5)

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def __str__(self):
        return self.site_name_fa

    @classmethod
    def get_solo(cls):
        setting, _ = cls.objects.get_or_create(pk=1)
        return setting


class ThemeAsset(TimeStampedModel):
    LIGHT = "light"
    DARK = "dark"
    MONO = "mono"
    ACCENT = "accent"
    VARIANT_CHOICES = [
        (LIGHT, "روشن"),
        (DARK, "تیره"),
        (MONO, "تک رنگ"),
        (ACCENT, "اکسنت"),
    ]

    title = models.CharField(max_length=120)
    variant = models.CharField(max_length=16, choices=VARIANT_CHOICES, default=LIGHT)
    file_path = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "دارایی تم"
        verbose_name_plural = "دارایی‌های تم"

    def __str__(self):
        return self.title


class TextSnippet(TimeStampedModel):
    group = models.CharField(max_length=80, default="general")
    key = models.SlugField(max_length=160, unique=True)
    title = models.CharField(max_length=160)
    text = models.TextField()
    help_text = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["group", "title"]
        verbose_name = "متن سایت"
        verbose_name_plural = "متن‌های سایت"

    def __str__(self):
        return f"{self.group} / {self.title}"


class FAQItem(TimeStampedModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "سوال پرتکرار"
        verbose_name_plural = "سوالات پرتکرار"

    def __str__(self):
        return self.question


class ContactMessage(TimeStampedModel):
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=32, blank=True)
    subject = models.CharField(max_length=160)
    message = models.TextField()
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"

    def __str__(self):
        return f"{self.full_name} - {self.subject}"


class StaticPage(TimeStampedModel):
    HOME = "home"
    ABOUT = "about"
    CONTACT = "contact"
    TERMS = "terms"
    PRIVACY = "privacy"
    FAQ = "faq"
    PAGE_CHOICES = [
        (HOME, "خانه"),
        (ABOUT, "درباره ما"),
        (CONTACT, "تماس"),
        (TERMS, "قوانین"),
        (PRIVACY, "حریم خصوصی"),
        (FAQ, "سوالات متداول"),
    ]

    page_key = models.CharField(max_length=24, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    seo_description = models.CharField(max_length=320, blank=True)

    class Meta:
        verbose_name = "صفحه استاتیک"
        verbose_name_plural = "صفحات استاتیک"

    def __str__(self):
        return self.get_page_key_display()

    @property
    def slug(self):
        return slugify(self.page_key)
