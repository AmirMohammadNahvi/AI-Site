import base64
import json

import requests
from django.utils import timezone

from ai_platform.models import AIModel, Conversation, Message


class AIAdapterError(Exception):
    pass


def _extract_path(payload, path):
    current = payload
    for part in path.split("."):
        if isinstance(current, list):
            current = current[int(part)]
        else:
            current = current.get(part)
        if current is None:
            return ""
    return current


def build_attachment_payload(uploaded_file):
    if not uploaded_file:
        return {}
    content = uploaded_file.read()
    uploaded_file.seek(0)
    return {
        "name": uploaded_file.name,
        "content_type": getattr(uploaded_file, "content_type", ""),
        "content_base64": base64.b64encode(content).decode("utf-8"),
    }


class AIAdapterService:
    @staticmethod
    def build_headers(model: AIModel):
        headers = {"Content-Type": "application/json"}
        headers.update(model.headers or {})
        if model.api_key and "Authorization" not in headers:
            headers["Authorization"] = f"Bearer {model.api_key}"
        return headers

    @staticmethod
    def build_payload(conversation: Conversation, prompt: str, attachment_payload=None):
        messages = []
        if conversation.model.system_prompt:
            messages.append({"role": "system", "content": conversation.model.system_prompt})
        if conversation.user:
            personalization = conversation.user.build_personalization_prompt()
            if personalization:
                messages.append({"role": "system", "content": personalization})
        for msg in conversation.messages.all():
            entry = {"role": msg.role, "content": msg.content}
            if msg.attachment:
                entry["attachment_url"] = msg.attachment.url
                entry["attachment_type"] = msg.attachment_type
            messages.append(entry)
        user_message = {"role": "user", "content": prompt}
        if attachment_payload:
            user_message["attachment"] = attachment_payload
        messages.append(user_message)
        return {
            "model": conversation.model.model_identifier,
            "messages": messages,
            "timestamp": timezone.now().isoformat(),
        }

    @classmethod
    def run(cls, conversation: Conversation, prompt: str, attachment_payload=None):
        model = conversation.model
        payload = cls.build_payload(conversation, prompt, attachment_payload)
        response = requests.request(
            method=model.http_method.upper(),
            url=model.endpoint_url,
            headers=cls.build_headers(model),
            data=json.dumps(payload),
            timeout=model.timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        content = _extract_path(data, model.response_text_path)
        if not content:
            raise AIAdapterError("No usable response content returned by provider.")
        return str(content), data


def persist_exchange(conversation, user_prompt, assistant_reply, attachment=None):
    user_message = Message.objects.create(
        conversation=conversation,
        role=Message.USER,
        content=user_prompt,
        attachment=attachment,
        attachment_type=getattr(attachment, "content_type", "") if attachment else "",
    )
    assistant_message = Message.objects.create(
        conversation=conversation,
        role=Message.ASSISTANT,
        content=assistant_reply,
    )
    if not conversation.title:
        conversation.title = user_prompt[:60]
        conversation.save(update_fields=["title", "updated_at"])
    return user_message, assistant_message
