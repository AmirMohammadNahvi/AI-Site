---
name: django-llm-feature-builder
description: build and extend django rest framework features for llm-based applications with multi-provider support configured from django admin. use when the user wants to add a new api endpoint, service, serializer, admin configuration, provider routing logic, conversation flow, usage logging, or a reusable backend pattern for an ai/chat application built with django and drf.
---

# Goal

Implement new backend features for a Django + DRF application that integrates with one or more LLM providers configured from Django admin.

Work as a senior Django backend engineer. Favor clean architecture, reusable service layers, explicit validation, and admin-driven configuration.

# Core behavior

When asked to add a feature:

1. Identify the feature boundary first:
   - model/admin only
   - api endpoint
   - service layer
   - provider integration
   - background task
   - logging/auditing
   - conversation state

2. Default to this architecture unless the user specifies otherwise:
   - `models.py` for persistent configuration and logs
   - `admin.py` for provider/model configuration
   - `serializers.py` for request/response validation
   - `views.py` or `viewsets.py` for HTTP layer
   - `services/` for llm orchestration and provider routing
   - `selectors/` for read-only query logic when useful
   - `tasks.py` for async work
   - `urls.py` for endpoint registration

3. Separate provider-specific logic from application logic.
   - provider clients must not leak into views
   - views should call services
   - services should call provider adapters

4. For multi-provider systems, prefer these entities:
   - `LLMProvider`
   - `LLMModelConfig`
   - `PromptTemplate`
   - `Conversation`
   - `Message`
   - `LLMRequestLog`

5. Always include:
   - validation rules
   - failure cases
   - timeout and retry notes
   - permission/auth assumptions
   - admin usability notes

# Output format

For implementation requests, produce output in this order:

1. short architecture note
2. file-by-file change plan
3. code for each file
4. migration note if needed
5. admin registration note
6. test checklist

# Coding rules

- use django and drf conventions
- use class-based apis unless the project clearly uses function-based views
- keep serializers explicit
- avoid putting llm client logic in serializers or views
- prefer dependency injection through service parameters or settings access wrappers
- if the project supports multiple providers, implement provider selection through a routing service
- include structured error handling
- avoid hardcoding secrets; assume they come from env vars or encrypted admin-managed references

# Provider integration rules

When building multi-provider support:
- define a stable internal interface for providers
- map provider-specific parameters into a normalized payload
- normalize response fields into a common schema
- preserve raw provider response optionally for audit/debug logs
- include model capability checks where relevant

# Admin rules

When admin-managed configuration is involved:
- optimize admin usability with search, filters, readonly fields where appropriate
- protect sensitive fields
- separate active/inactive configurations
- support priority or default selection for providers/models

# References

Read these when relevant:
- `references/architecture.md` for suggested layering
- `references/conventions.md` for naming and error-handling conventions

# Script usage

Use `scripts/scaffold_checklist.py` if you need to generate or verify a feature implementation checklist before writing code.