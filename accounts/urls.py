from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("otp/", views.otp_request_view, name="otp_request"),
    path("otp/verify/", views.otp_verify_view, name="otp_verify"),
    path("profile/", views.profile_view, name="profile"),
    path("personalization/", views.personalization_view, name="personalization"),
    path("settings/action/", views.settings_action_view, name="settings_action"),
]
