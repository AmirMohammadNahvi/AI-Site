from django.contrib import admin

from .models import AIModel, AIModelCapability, Conversation, Message


class AIModelCapabilityInline(admin.TabularInline):
    model = AIModelCapability
    extra = 0


@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ("name", "provider_label", "is_active", "is_featured", "display_order")
    list_filter = ("is_active", "is_featured", "provider_label")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [AIModelCapabilityInline]


admin.site.register(Conversation)
admin.site.register(Message)
