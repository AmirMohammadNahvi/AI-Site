import random
import string
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.crypto import salted_hmac

from core.models import TimeStampedModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    PERSONA_DEFAULT = "default"
    PERSONA_PROFESSIONAL = "professional"
    PERSONA_CREATIVE = "creative"
    PERSONA_ANALYST = "analyst"
    PERSONA_SUPPORTIVE = "supportive"
    THEME_SYSTEM = "system"
    THEME_LIGHT = "light"
    THEME_DARK = "dark"

    PERSONA_CHOICES = [
        (PERSONA_DEFAULT, "پیش‌فرض"),
        (PERSONA_PROFESSIONAL, "حرفه‌ای"),
        (PERSONA_CREATIVE, "خلاق"),
        (PERSONA_ANALYST, "تحلیل‌گر"),
        (PERSONA_SUPPORTIVE, "همراه و دوستانه"),
    ]
    THEME_CHOICES = [
        (THEME_SYSTEM, "سیستمی"),
        (THEME_LIGHT, "روشن"),
        (THEME_DARK, "تیره"),
    ]

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=120)
    mobile = models.CharField(max_length=16, unique=True, null=True, blank=True)
    theme_preference = models.CharField(max_length=12, choices=THEME_CHOICES, default=THEME_SYSTEM)
    persona_choice = models.CharField(max_length=20, choices=PERSONA_CHOICES, default=PERSONA_DEFAULT)
    custom_instructions = models.TextField(blank=True)
    preferred_name = models.CharField(max_length=120, blank=True)
    job_title = models.CharField(max_length=120, blank=True)
    interests = models.TextField(blank=True)
    memory_enabled = models.BooleanField(default=False)
    auth_session_version = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.full_name or self.email

    def get_session_auth_hash(self):
        key_salt = "accounts.models.User.get_session_auth_hash"
        value = f"{self.password}{self.auth_session_version}"
        return salted_hmac(key_salt, value).hexdigest()

    def invalidate_all_sessions(self):
        self.auth_session_version += 1
        self.save(update_fields=["auth_session_version", "updated_at"])

    def build_personalization_prompt(self):
        lines = []
        if self.persona_choice and self.persona_choice != self.PERSONA_DEFAULT:
            lines.append(f"شخصیت ترجیحی کاربر: {self.get_persona_choice_display()}")
        if self.preferred_name:
            lines.append(f"کاربر ترجیح می‌دهد با این نام خطاب شود: {self.preferred_name}")
        if self.job_title:
            lines.append(f"شغل کاربر: {self.job_title}")
        if self.interests:
            lines.append(f"علایق، ارزش‌ها و سلیقه‌های کاربر: {self.interests}")
        if self.custom_instructions:
            lines.append(f"دستورات بیشتر برای لحن و رفتار: {self.custom_instructions}")
        return "\n".join(lines)


class OTPRequest(TimeStampedModel):
    mobile = models.CharField(max_length=16)
    code_hash = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "درخواست OTP"
        verbose_name_plural = "درخواست‌های OTP"

    def __str__(self):
        return self.mobile

    @classmethod
    def generate_code(cls):
        return "".join(random.choices(string.digits, k=settings.OTP_CODE_LENGTH))

    @classmethod
    def create_for_mobile(cls, mobile):
        code = cls.generate_code()
        instance = cls.objects.create(
            mobile=mobile,
            code_hash=make_password(code),
            expires_at=timezone.now() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES),
        )
        return instance, code

    def verify(self, code):
        if self.is_used or timezone.now() > self.expires_at:
            return False
        if check_password(code, self.code_hash):
            self.is_used = True
            self.save(update_fields=["is_used", "updated_at"])
            return True
        return False
