# Security notes

- never hardcode provider secrets
- do not expose raw provider errors directly to clients
- redact sensitive payload fragments in logs where appropriate
- validate prompt template editing permissions
- limit who can change default provider/model routing