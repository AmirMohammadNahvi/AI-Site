from core.models import SiteSetting


def site_context(request):
    return {
        "site_settings": SiteSetting.get_solo(),
        "theme_choice": request.session.get("theme", "system"),
    }
