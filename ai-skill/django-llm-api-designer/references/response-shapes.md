# Response shapes

## Success
{
  "reply": "...",
  "conversation_id": "uuid",
  "provider": "openai",
  "model": "gpt-4.1",
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 250,
    "total_tokens": 350
  },
  "latency_ms": 1200,
  "finish_reason": "stop"
}

## Error
{
  "error": {
    "code": "provider_timeout",
    "message": "provider request timed out",
    "details": {}
  }
}