from django.urls import path

from . import views


app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("pricing/", views.pricing, name="pricing"),
    path("about/", views.static_page, {"page_key": "about"}, name="about"),
    path("terms/", views.static_page, {"page_key": "terms"}, name="terms"),
    path("privacy/", views.static_page, {"page_key": "privacy"}, name="privacy"),
    path("faq/", views.static_page, {"page_key": "faq"}, name="faq"),
    path("contact/", views.contact, name="contact"),
    path("theme/", views.set_theme, name="set_theme"),
]
