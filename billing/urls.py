from django.urls import path

from . import views


app_name = "billing"

urlpatterns = [
    path("", views.index, name="index"),
    path("checkout/<slug:slug>/", views.checkout, name="checkout"),
    path("orders/<int:order_id>/status/", views.order_status, name="order_status"),
    path("verify/", views.verify, name="verify"),
]
