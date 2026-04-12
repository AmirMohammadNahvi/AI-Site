from django.urls import path

from . import views


app_name = "ai_platform"

urlpatterns = [
    path("", views.chat_view, name="chat"),
    path("<int:conversation_id>/", views.chat_view, name="chat_detail"),
    path("<int:conversation_id>/archive/", views.conversation_archive, name="chat_archive"),
    path("<int:conversation_id>/restore/", views.conversation_restore, name="chat_restore"),
    path("<int:conversation_id>/delete/", views.conversation_delete, name="chat_delete"),
    path("models/<slug:slug>/", views.model_detail, name="model_detail"),
]
