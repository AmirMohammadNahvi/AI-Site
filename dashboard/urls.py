from django.urls import path

from . import views


app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("billing/", views.billing_overview, name="billing"),
    path("profile/", views.profile, name="profile"),
    path("admin-panel/", views.admin_home, name="admin_home"),
    path("admin-panel/settings/", views.settings_edit, name="admin_settings"),
    path("admin-panel/texts/", views.text_list, name="admin_texts"),
    path("admin-panel/texts/new/", views.text_edit, name="admin_text_create"),
    path("admin-panel/texts/<int:pk>/", views.text_edit, name="admin_text_edit"),
    path("admin-panel/models/", views.model_list, name="admin_models"),
    path("admin-panel/models/new/", views.model_edit, name="admin_model_create"),
    path("admin-panel/models/<int:pk>/", views.model_edit, name="admin_model_edit"),
    path("admin-panel/plans/", views.plan_list, name="admin_plans"),
    path("admin-panel/plans/new/", views.plan_edit, name="admin_plan_create"),
    path("admin-panel/plans/<int:pk>/", views.plan_edit, name="admin_plan_edit"),
    path("admin-panel/transactions/", views.transactions, name="admin_transactions"),
]
