from django import forms

from .models import ContactMessage, SiteSetting, TextSnippet


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["full_name", "email", "phone", "subject", "message"]


class SiteSettingForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = [
            "site_name_fa",
            "site_name_en",
            "tagline",
            "hero_title",
            "hero_subtitle",
            "support_email",
            "support_phone",
            "address",
            "telegram_url",
            "instagram_url",
            "linkedin_url",
            "x_url",
            "light_logo",
            "dark_logo",
            "primary_color",
            "secondary_color",
            "otp_provider_name",
            "otp_provider_api_key",
            "otp_provider_sender",
            "zarinpal_merchant_id",
            "zarinpal_sandbox",
            "payment_guide_text",
            "payment_guide_url",
            "free_guest_message_limit",
        ]


class TextSnippetForm(forms.ModelForm):
    class Meta:
        model = TextSnippet
        fields = ["group", "key", "title", "text", "help_text", "is_active"]
