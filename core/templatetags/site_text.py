from django import template
from django.utils.safestring import mark_safe

from core.models import TextSnippet


register = template.Library()


@register.simple_tag
def site_text(key, default_text="", title="", group="general", help_text=""):
    snippet, _ = TextSnippet.objects.get_or_create(
        key=key,
        defaults={
            "group": group,
            "title": title or key,
            "text": default_text,
            "help_text": help_text,
        },
    )
    if not snippet.text and default_text:
        snippet.text = default_text
        snippet.save(update_fields=["text", "updated_at"])
    return snippet.text if snippet.is_active else default_text


@register.simple_tag
def site_html(key, default_html="", title="", group="general", help_text=""):
    return mark_safe(site_text(key, default_html, title=title, group=group, help_text=help_text))
