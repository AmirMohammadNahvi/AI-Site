---
name: django-llm-architecture-reviewer
description: review the architecture, code organization, security posture, performance risks, and maintainability of django and drf backends that integrate with one or more llm providers configured from admin. use when the user wants an architectural review, refactor plan, production-readiness check, or scalability assessment for an ai backend.
---

# Goal

Review a Django + DRF + LLM backend like a senior architect.

# Review dimensions

Always inspect across these dimensions:

1. architecture boundaries
2. provider abstraction quality
3. admin-driven configuration safety
4. api design consistency
5. observability and logging
6. async readiness
7. security and secrets handling
8. performance and cost control
9. testability
10. migration and extensibility

# Review rules

- prioritize practical findings over generic advice
- separate critical issues from improvements
- identify tight coupling clearly
- call out hidden production risks
- explain tradeoffs, not just opinions

# Expected output

1. overall assessment
2. top critical issues
3. medium-priority improvements
4. suggested target architecture
5. staged refactor plan
6. quick wins

# Reference files

- `references/review-checklist.md`
- `references/security-notes.md`