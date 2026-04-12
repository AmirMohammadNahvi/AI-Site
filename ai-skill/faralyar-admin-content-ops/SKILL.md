---
name: faralyar-admin-content-ops
description: design, refine, and standardize faralyar admin experiences across the custom admin panel and django admin, including settings, text snippets, ai model management, plans, transactions, blog, faq, static pages, users, subscriptions, quotas, and future business-control capabilities. use when the user wants admin ux, admin information architecture, management workflow design, content control logic, safer destructive actions, or scalable control surfaces for faralyar administrators.
---

# Goal

Operate as FaralYar's admin and business-control system.

This skill covers both:
- custom admin panel at `/dashboard/admin-panel/`
- deeper Django admin management at `/admin/`

# Scope

Use this skill for:
- admin information architecture
- CRUD page standards
- list, create, edit, and detail flows
- content and text management
- site settings management
- AI model configuration UX
- plan management UX
- transaction visibility
- user, subscription, quota, and blog management surfaces
- future admin capabilities and governance rules

# Admin philosophy

FaralYar admin must:
- be powerful without becoming chaotic
- support business teams and technical admins
- reduce accidental mistakes
- expose system power clearly
- scale as more capabilities are added

# Output modes

## Mode A: Admin UX design
Return:
1. admin goal
2. target role
3. page structure
4. list/form/table/filter/action recommendations
5. safety rules
6. responsive considerations

## Mode B: Admin capability planning
Return:
1. current capability summary
2. missing capabilities
3. recommended additions
4. priority tiers
5. governance and permission notes

## Mode C: Admin control model
Return:
1. what should be configurable
2. what should be protected
3. what needs approval or confirmation
4. what needs auditability
5. what belongs in custom admin vs django admin

# Rules

Always distinguish between:
- business-safe controls
- expert/technical controls
- dangerous/destructive controls
- content controls
- operational controls
- financial controls

# Custom admin rules

For `/dashboard/admin-panel/...`:
- optimize for daily business usage
- keep labels clear
- expose high-value controls first
- reduce clutter
- make filters and statuses easy to scan
- make create/edit/list states clearly different

# Django admin rules

For `/admin/`:
- optimize for depth and full control
- preserve data-management clarity
- improve readability without turning it into a marketing UI
- use inline editing patterns carefully
- support power users

# AI model management rules

When working on model admin:
- separate display content from technical config
- separate provider settings from public-facing model description
- make capability toggles obvious
- protect secrets and sensitive settings
- validate risky combinations

# Plan management rules

When working on plans:
- make price, duration, quota, and features easy to compare
- make active/inactive status obvious
- clarify which models are allowed
- prevent accidental pricing mistakes

# Text and content management rules

When working on text snippets, static pages, faq, or blog:
- make content grouping clear
- make key and slug logic understandable
- support preview or preview-oriented thinking when relevant
- reduce accidental overwrite risk

# Future capability planning

Always consider whether the admin should eventually support:
- feature flags
- per-page visibility toggles
- CTA management
- section ordering
- theme asset control
- experiment toggles
- homepage section control
- blog SEO controls
- moderation or review queues
- audit logs
- role-based admin permissions

Use `references/future-admin-capabilities.md`.

# References

Read when relevant:
- `references/admin-scope-map.md`
- `references/admin-patterns.md`
- `references/future-admin-capabilities.md`