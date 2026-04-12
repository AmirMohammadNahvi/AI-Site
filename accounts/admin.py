from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import OTPRequest, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "full_name", "mobile", "is_staff", "is_active")
    search_fields = ("email", "full_name", "mobile")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("اطلاعات", {"fields": ("full_name", "mobile", "theme_preference")}),
        ("دسترسی", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("تاریخ‌ها", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "full_name", "mobile", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )


admin.site.register(OTPRequest)
