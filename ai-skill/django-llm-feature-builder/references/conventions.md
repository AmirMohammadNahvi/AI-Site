# Conventions

- service classes end with `Service`
- provider adapters end with `Client`
- config models use `is_active`
- logs should include latency, provider, model name, status, request id if available
- all external call failures should be translated into application-level exceptions