# API patterns

## Chat endpoint
POST /api/v1/chat/

Request:
- conversation_id optional
- message required
- model optional
- provider optional

Response:
- reply
- conversation_id
- usage
- provider
- model

## Async generation endpoint
POST /api/v1/generations/
GET /api/v1/generations/{id}/

Use when provider latency is unpredictable or output is large.