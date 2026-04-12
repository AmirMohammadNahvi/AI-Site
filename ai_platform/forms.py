from django import forms

from .models import AIModel, Conversation


class ChatMessageForm(forms.Form):
    prompt = forms.CharField(
        label="پیام",
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "x-ref": "promptField",
                "placeholder": "درخواستت را دقیق و روشن بنویس...",
                "class": "min-h-[7.5rem] resize-none border-0 bg-transparent px-0 py-0 text-sm leading-8 focus:border-0 focus:ring-0",
            }
        ),
    )
    attachment = forms.FileField(
        required=False,
        label="فایل یا تصویر",
        widget=forms.ClearableFileInput(attrs={"class": "text-sm"}),
    )
    model = forms.ModelChoiceField(
        queryset=AIModel.objects.filter(is_active=True),
        label="مدل",
        widget=forms.Select(attrs={"x-ref": "modelSelect", "class": "hidden"}),
    )
    conversation_id = forms.IntegerField(required=False, widget=forms.HiddenInput)


class AIModelForm(forms.ModelForm):
    text_enabled = forms.BooleanField(required=False, initial=True, label="پشتیبانی متن")
    image_enabled = forms.BooleanField(required=False, label="پشتیبانی تصویر ورودی")
    file_enabled = forms.BooleanField(required=False, label="پشتیبانی فایل ورودی")

    class Meta:
        model = AIModel
        fields = [
            "name",
            "slug",
            "provider_label",
            "endpoint_url",
            "http_method",
            "headers",
            "api_key",
            "model_identifier",
            "timeout_seconds",
            "display_order",
            "request_format",
            "response_text_path",
            "system_prompt",
            "summary",
            "description",
            "limitations",
            "is_active",
            "is_featured",
        ]


class ConversationTitleForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ["title"]
