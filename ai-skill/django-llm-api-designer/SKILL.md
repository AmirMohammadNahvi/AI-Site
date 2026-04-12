---
name: django-llm-api-designer
description: design and implement drf api endpoints for llm-powered applications, including chat, completion, conversation history, streaming-compatible response plans, token usage reporting, and provider-agnostic request handling. use when the user wants to create or refine ai endpoints in a django rest framework backend.
---

# Goal

Design clean, production-oriented DRF APIs for LLM applications.

# Core behavior

For every API design task:

1. Clarify the endpoint type:
   - single prompt completion
   - chat turn
   - conversation history retrieval
   - regenerate response
   - prompt template execution
   - async inference job
   - usage/log reporting

2. Prefer explicit request/response serializers.

3. Normalize input fields where possible:
   - `message`
   - `conversation_id`
   - `provider`
   - `model`
   - `temperature`
   - `max_tokens`
   - `metadata`

4. Normalize response fields where possible:
   - `reply`
   - `conversation_id`
   - `provider`
   - `model`
   - `usage`
   - `finish_reason`
   - `latency_ms`

5. Always address:
   - permissions
   - throttling
   - validation
   - timeout behavior
   - error schema
   - logging/auditing
   - idempotency concerns for retries

# Design rules

- use DRF serializers for input and output contracts
- avoid provider-specific response formats at the API boundary
- put business logic in services
- propose async task-based designs when response time may be long
- mention streaming as a design option even if not implemented

# Output format

1. endpoint summary
2. url pattern
3. request serializer
4. response serializer
5. view/service outline
6. error response examples
7. test scenarios

# References

- `references/api-patterns.md`
- `references/response-shapes.md`