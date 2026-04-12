---
name: django-llm-bug-fixer
description: debug and fix backend issues in django and django rest framework applications that integrate with multiple llm providers. use when the user shares tracebacks, failing endpoints, admin issues, serializer errors, provider routing bugs, invalid config behavior, timeout problems, celery issues, or inconsistent ai responses.
---

# Goal

Diagnose and fix bugs in a Django + DRF + LLM integration stack.

# Debugging workflow

1. Classify the bug:
   - django model/admin bug
   - serializer/view bug
   - routing/config selection bug
   - provider api bug
   - async task bug
   - persistence/logging bug
   - permission/throttling bug

2. Reconstruct the execution path:
   - request entry point
   - serializer validation
   - service layer
   - provider selection
   - external api call
   - response normalization
   - database write/logging

3. Identify the most likely failure boundary before proposing changes.

4. When given traceback or logs:
   - summarize root cause in plain language
   - point to the exact file/function likely responsible
   - provide minimal safe fix first
   - then suggest refactor if needed

# Rules

- do not suggest broad rewrites when a small fix is possible
- distinguish symptom from root cause
- explain whether the issue is deterministic or intermittent
- for intermittent provider failures, include retry/idempotency analysis
- for admin-driven config bugs, inspect validation and active/default selection logic first

# Output format

1. probable root cause
2. evidence chain
3. minimal fix
4. optional hardening improvements
5. regression test checklist

# Script usage

Use `scripts/traceback_summarizer.py` when a long traceback needs to be condensed into likely root-cause sections.

# Reference

Read `references/debugging-playbook.md` when the issue spans multiple layers.