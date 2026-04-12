---
name: faralyar-user-flow-qa
description: audit, improve, and validate end-to-end user flows in faralyar, including landing to signup, otp login, pricing to checkout, chat usage, archive and restore flows, personalization, theme switching, dashboard actions, and admin-assisted journeys. use when the user wants to detect friction, drop-off risk, broken states, unclear steps, or ux issues across multiple routes in faralyar.
---

# Goal

Operate as FaralYar's end-to-end UX flow QA system.

Analyze flows across multiple pages, not just single-page UI.

# Scope

Use this skill for:
- signup and login flow
- otp flow
- landing to conversion flow
- pricing to checkout to verify flow
- guest to subscribed user flow
- chat creation and continuation flow
- archive, restore, and delete conversation flow
- personalization and theme flow
- dashboard usage flow
- admin-assisted business flows

# Core principle

A flow is good only if the user:
- understands where they are
- knows what to do next
- receives clear system feedback
- can recover from failure
- does not get surprised by state changes

# Output modes

## Mode A: Flow audit
Return:
1. flow summary
2. step-by-step breakdown
3. friction points
4. drop-off risks
5. missing states
6. prioritized fixes

## Mode B: Flow redesign
Return:
1. current problem
2. ideal flow structure
3. improved step sequence
4. messaging and feedback improvements
5. mobile considerations
6. QA checklist

## Mode C: State coverage review
Return:
1. happy path
2. alternate path
3. error path
4. loading path
5. empty path
6. recovery path

# Rules

Always inspect:
- entry point clarity
- next-step clarity
- success state
- error state
- loading state
- cancel/back behavior
- auth interruption
- mobile continuity
- theme consistency if relevant

# Conversion-sensitive flows

For pricing, checkout, signup, and login:
- reduce friction
- reduce uncertainty
- reduce unnecessary choices
- surface reassurance
- keep progression obvious

# Risk focus

Prioritize:
- abandoned signup
- failed OTP verification
- failed payment verification
- chat confusion on empty state
- destructive actions without enough warning
- mobile step breakdown
- unclear archived/restored conversation status

# References

Read when relevant:
- `references/key-flows.md`
- `references/flow-risk-checklist.md`
- `references/state-coverage.md`