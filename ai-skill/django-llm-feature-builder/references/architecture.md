# Suggested architecture

## Layers

- API layer: DRF views, serializers, permissions
- Domain/service layer: prompt construction, provider routing, retries, response normalization
- Persistence layer: config, conversations, logs
- Async layer: celery tasks for long-running inference, summarization, backfills

## Recommended service split

- `services/provider_router.py`
- `services/prompt_builder.py`
- `services/chat_service.py`
- `services/logging_service.py`

## Principle

Views orchestrate HTTP.
Services orchestrate business logic.
Provider adapters orchestrate external API calls.