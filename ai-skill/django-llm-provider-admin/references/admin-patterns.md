# Admin patterns for LLM configuration

## Recommended list display
- name
- provider_type
- model_name
- is_active
- is_default
- priority
- updated_at

## Useful filters
- provider_type
- is_active
- is_default

## Good readonly fields
- created_at
- updated_at
- last_healthcheck_at
- last_error_message

## Safety recommendations
- use model `clean()` for cross-field validation
- use admin actions for bulk activation carefully
- store credentials as references, not raw secrets, when possible