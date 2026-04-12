from django.urls import path

from . import views


app_name = "billing"

urlpatterns = [
    path("checkout/<slug:slug>/", views.checkout, name="checkout"),
    path("verify/", views.verify, name="verify"),
]
