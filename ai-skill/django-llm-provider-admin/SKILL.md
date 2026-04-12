---
name: django-llm-provider-admin
description: design and implement django admin workflows for managing multiple llm providers, model configurations, credentials references, default routing, and provider activation in a django application. use when the user wants to build or improve admin panels that control ai provider settings, active models, fallbacks, priorities, and operational safety.
---

# Goal

Build robust Django admin interfaces for managing multiple LLM providers and model configurations safely and clearly.

# Core behavior

When working on admin features:

1. Assume non-technical admins may manage:
   - active provider selection
   - model enable/disable
   - default temperature/token limits
   - fallback order
   - provider priority
   - prompt templates
   - system prompts
   - feature flags for chat endpoints

2. Recommend these model concepts when relevant:
   - `LLMProvider`
   - `LLMModelConfig`
   - `ProviderCredentialReference`
   - `PromptTemplate`
   - `RoutingRule`

3. Design admin for safety:
   - avoid exposing raw secrets in plain text
   - mark sensitive fields carefully
   - use readonly fields for generated metadata
   - add validation to prevent invalid active states
   - prevent multiple conflicting defaults unless explicitly allowed

4. Improve usability:
   - search fields
   - list filters
   - bulk actions for activate/deactivate
   - inline related configs where helpful
   - help text for provider-specific fields

# Output expectations

When asked to build or improve admin:
1. propose model fields if missing
2. provide `admin.py` changes
3. provide model validation
4. explain safeguards
5. include example admin workflow

# Validation rules

Always check:
- only one default model per routing group unless multi-default is intended
- inactive provider cannot be chosen as global default
- fallback chain does not point to inactive configs
- token and timeout limits are within sensible bounds

# Script usage

Use `scripts/validate_provider_config.py` to validate a provider configuration payload shape when designing model/admin validation logic.

# Reference

See `references/admin-patterns.md` for recommended admin UX patterns.