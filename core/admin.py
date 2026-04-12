from django.contrib import admin

from .models import ContactMessage, FAQItem, SiteSetting, StaticPage, TextSnippet, ThemeAsset


admin.site.register(SiteSetting)
admin.site.register(ThemeAsset)
admin.site.register(FAQItem)
admin.site.register(ContactMessage)
admin.site.register(StaticPage)
admin.site.register(TextSnippet)
