from django.conf import settings
from django.db import models
from django.utils.text import slugify

from core.models import TimeStampedModel


class AIModel(TimeStampedModel):
    OPENAI = "openai"
    GENERIC = "generic"
    REQUEST_FORMAT_CHOICES = [
        (OPENAI, "OpenAI Compatible"),
        (GENERIC, "Generic JSON"),
    ]

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    provider_label = models.CharField(max_length=120)
    endpoint_url = models.URLField()
    http_method = models.CharField(max_length=10, default="POST")
    headers = models.JSONField(default=dict, blank=True)
    api_key = models.CharField(max_length=255, blank=True)
    model_identifier = models.CharField(max_length=255)
    timeout_seconds = models.PositiveIntegerField(default=60)
    display_order = models.PositiveIntegerField(default=0)
    request_format = models.CharField(max_length=20, choices=REQUEST_FORMAT_CHOICES, default=OPENAI)
    response_text_path = models.CharField(max_length=160, default="choices.0.message.content")
    system_prompt = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    limitations = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "مدل هوش مصنوعی"
        verbose_name_plural = "مدل‌های هوش مصنوعی"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def has_capability(self, capability_type):
        return self.capabilities.filter(capability_type=capability_type, is_enabled=True).exists()


class AIModelCapability(TimeStampedModel):
    TEXT = "text"
    IMAGE_INPUT = "image_input"
    FILE_INPUT = "file_input"
    CAPABILITY_CHOICES = [
        (TEXT, "متن"),
        (IMAGE_INPUT, "ورودی تصویر"),
        (FILE_INPUT, "ورودی فایل"),
    ]

    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name="capabilities")
    capability_type = models.CharField(max_length=20, choices=CAPABILITY_CHOICES)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ("model", "capability_type")
        verbose_name = "قابلیت مدل"
        verbose_name_plural = "قابلیت‌های مدل"

    def __str__(self):
        return f"{self.model.name} - {self.get_capability_type_display()}"


class Conversation(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations", null=True, blank=True)
    guest_session_key = models.CharField(max_length=40, blank=True)
    model = models.ForeignKey(AIModel, on_delete=models.PROTECT, related_name="conversations")
    title = models.CharField(max_length=180, blank=True)
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "گفتگو"
        verbose_name_plural = "گفتگوها"

    def __str__(self):
        return self.title or f"گفتگو با {self.model.name}"


class Message(TimeStampedModel):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    ROLE_CHOICES = [
        (USER, "کاربر"),
        (ASSISTANT, "دستیار"),
        (SYSTEM, "سیستم"),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)
    content = models.TextField()
    attachment = models.FileField(upload_to="user_uploads/%Y/%m/%d/", blank=True, null=True)
    attachment_type = models.CharField(max_length=20, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "پیام"
        verbose_name_plural = "پیام‌ها"

    def __str__(self):
        return f"{self.get_role_display()} - {self.created_at:%Y-%m-%d %H:%M}"
