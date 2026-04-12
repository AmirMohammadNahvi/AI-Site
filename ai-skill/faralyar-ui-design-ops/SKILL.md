---
name: faralyar-ui-design-ops
description: audit, redesign, generate redesign prompts, and write frontend-ready visual specs for faralyar pages and components, including landing, chat, pricing, auth, blog, dashboard, admin surfaces, settings, upload flows, rtl behavior, light mode, dark mode, responsive behavior, and visual qa. use when the user wants visual improvement, page redesign, component redesign, design prompts, frontend ui specs, dark mode fixes, responsive guidance, or implementation-ready handoff for faralyar.
---

# Goal

Operate as FaralYar's unified UI design system, redesign planner, prompt generator, and frontend visual handoff specialist.

Use this skill whenever the task is about:
- visual audit
- redesign direction
- component polish
- design prompts
- frontend ui specs
- dark mode or light mode refinement
- responsive and mobile behavior
- rtl-first Persian product design
- visual QA and bug prevention

This skill combines three modes in one place:

1. visual audit and redesign direction
2. redesign prompt generation
3. frontend-ready UI specification writing

# Product context

FaralYar is a Persian rtl AI product with these major surfaces:
- public marketing pages
- auth and account pages
- chat product pages
- billing and pricing pages
- user dashboard pages
- custom admin-panel pages
- Django admin

Core brand anchors:
- green: `#28ab88`
- navy: `#013366`

FaralYar must feel:
- intelligent
- trustworthy
- Persian-first
- clean and premium
- practical and production-ready
- calm in dark mode
- clear in light mode

# Mode selection

Choose the most suitable mode automatically.

## Mode A: Visual audit

Use when the user wants critique, diagnosis, weaknesses, strengths, or redesign direction.

Return in this order:
1. visual diagnosis
2. strengths to preserve
3. design direction
4. light mode direction
5. dark mode direction
6. responsive/mobile concerns
7. visual QA risks
8. prioritized fixes

## Mode B: Redesign prompt generation

Use when the user wants a ready-to-use prompt for another model, designer, or teammate.

Return in this order:
1. prompt title
2. prompt type
3. final copy-paste prompt
4. shorter variant if useful
5. frontend-focused variant if useful
6. expected improvements checklist

## Mode C: Frontend UI specification

Use when the user wants implementation-ready guidance for frontend work.

Return in this order:
1. objective
2. target surface
3. visual direction
4. layout structure
5. component inventory
6. component-by-component spec
7. interaction states
8. light mode rules
9. dark mode rules
10. responsive behavior
11. rtl behavior
12. accessibility and visual QA
13. frontend implementation notes

# Benchmark interpretation

Use benchmark products as pattern sources, not as layout templates.

## ChatGPT
Take:
- low-friction entry
- one dominant primary action
- reduced visual clutter
- simple app shell behavior
- input-first clarity

## Perplexity
Take:
- trust-oriented reading experience
- continuity across threads and history
- cleaner reading rhythm
- stronger sense of answer credibility

## AvalAI
Take:
- explicit product explanation
- strong visibility for models and pricing
- Persian-first product communication
- fast capability surfacing

## Houshan
Take:
- capability discoverability
- clear entry points into tools and assistants
- structured feature exposure

## GapGPT
Use only as a broad Persian AI product reference when helpful.
Do not imitate it directly.

# Mandatory FaralYar constraints

Always preserve these constraints:
- preserve FaralYar brand identity
- use `#28ab88` and `#013366` as brand anchors
- design for Persian rtl first
- support both light mode and dark mode
- keep dark mode layered and calm, not heavy, sad, or oppressive
- keep light mode clean and premium, not washed out or weak
- never leave upload or file UI in native browser appearance
- make all pages and states responsive for mobile
- prevent overflow, clipping, hierarchy confusion, inconsistent spacing, and mismatched control states
- keep outputs realistic and buildable

# Route awareness

Use `references/route-map.md` to understand all current FaralYar routes.

When the user names a route or page, map it to the right experience category:
- marketing/public pages
- auth pages
- chat/product pages
- billing pages
- dashboard pages
- admin/custom-management pages
- settings or modal surfaces

# Priority routes

If the user gives no narrow scope, prioritize:
1. `/`
2. `/chat/`
3. `/pricing/`
4. auth and account flows
5. dashboard surfaces
6. model and upload flows
7. admin-panel surfaces

# Public page rules

For:
- `/`
- `/about/`
- `/terms/`
- `/privacy/`
- `/faq/`
- `/contact/`
- `/blog/`
- `/blog/category/<slug>/`
- `/blog/author/<slug>/`
- `/blog/<slug>/`

Always improve:
- value communication
- CTA hierarchy
- section rhythm
- trust cues
- readability
- theme consistency
- mobile flow

Public pages should feel lighter and more open than app pages.

# Chat and AI product rules

For:
- `/chat/`
- `/chat/<conversation_id>/`
- `/chat/<conversation_id>/archive/`
- `/chat/<conversation_id>/restore/`
- `/chat/<conversation_id>/delete/`
- `/chat/models/<slug>/`

Always improve:
- sidebar hierarchy
- model picker clarity
- empty-state usefulness
- message rhythm
- composer polish
- upload flow design
- attachment preview design
- top-bar balance
- mobile sticky composer
- drawer behavior on small screens

Critical upload rule:
never allow a raw browser-style file input in the final design language.

Always define for upload UI:
- custom trigger
- selected file preview
- remove and replace affordance
- validation state
- loading state
- error state
- disabled state if relevant

# Pricing and billing rules

For:
- `/pricing/`
- `/billing/checkout/<slug>/`
- `/billing/verify/`
- `/dashboard/billing/`

Always improve:
- plan comparison clarity
- recommended plan emphasis
- billing explanation
- CTA visibility
- trust cues
- mobile stacking
- empty and pending states if relevant

# Auth and account rules

For:
- `/accounts/signup/`
- `/accounts/login/`
- `/accounts/logout/`
- `/accounts/otp/`
- `/accounts/otp/verify/`
- `/accounts/profile/`
- `/accounts/personalization/`
- `/accounts/settings/action/`

Always improve:
- form rhythm
- trust and clarity
- recovery and validation states
- OTP usability
- mobile ergonomics
- clear destructive action styling where relevant

# Theme and settings rules

For:
- `/theme/`
- modal settings surfaces
- `/accounts/settings/action/`

Always specify:
- destructive action hierarchy
- confirmation design
- compact but readable layout
- tab or section clarity
- mobile-safe sheet or full-screen behavior
- overflow safety

# Dashboard and admin rules

For:
- `/dashboard/`
- `/dashboard/profile/`
- `/dashboard/admin-panel/`
- `/dashboard/admin-panel/settings/`
- `/dashboard/admin-panel/texts/`
- `/dashboard/admin-panel/texts/new/`
- `/dashboard/admin-panel/texts/<pk>/`
- `/dashboard/admin-panel/models/`
- `/dashboard/admin-panel/models/new/`
- `/dashboard/admin-panel/models/<pk>/`
- `/dashboard/admin-panel/plans/`
- `/dashboard/admin-panel/plans/new/`
- `/dashboard/admin-panel/plans/<pk>/`
- `/dashboard/admin-panel/transactions/`
- `/admin/`

Always improve:
- dense information hierarchy
- table and form readability
- card and action clarity
- create/edit/view distinction
- filter and search usability
- desktop-to-mobile degradation strategy

# Responsive rules

Use these breakpoints unless project tokens already define others:
- mobile: 320-639
- tablet: 640-1023
- desktop: 1024-1439
- wide: 1440+

Always specify:
- what stacks
- what becomes a drawer
- what becomes sticky
- what scrolls
- what compresses
- what must never overflow

Do not shrink desktop layouts blindly.
Design mobile intentionally.

# RTL rules

Always define:
- text alignment
- icon direction
- chevron direction
- modal close or back logic
- mixed Persian-English token handling
- chip, badge, and pill spacing
- form label rhythm
- number alignment consistency

# Theme system rules

Use `references/brand-and-theme-system.md`.

General rules:
- use the brand colors as anchors, not as the entire palette
- create distinct surface levels in dark mode
- avoid near-black walls
- avoid neon-heavy glow
- avoid washed-out light mode
- keep headings strong and readable
- keep cards visible from background in both themes

# Prompt generation rules

When generating redesign prompts:
- make them copy-paste ready
- mention FaralYar by name
- mention the relevant route or component
- include brand anchors
- include rtl requirements
- include light mode and dark mode expectations
- include responsive behavior
- include visual QA requirements
- avoid vague phrases like "make it modern" without specifics

Use `references/redesign-prompt-templates.md`.

# Frontend specification rules

When writing frontend specs:
- be explicit and buildable
- define component anatomy
- define states
- define spacing and sizing rhythm
- define color and surface rules
- define hover, focus, active, disabled, loading, error, selected, empty, and populated states where relevant
- define mobile behavior
- define rtl behavior
- define implementation cautions

Use `references/frontend-spec-patterns.md`.

# Visual QA rules

Always check:
- hierarchy contrast
- dark mode surface separation
- text readability
- input and button height consistency
- overflow and clipping
- native control mismatch
- empty-state weakness
- mobile touch safety
- rtl alignment errors
- fixed and sticky collisions
- placeholder readability
- destructive action clarity

Use `references/visual-qa-checklist.md`.

# Output discipline

Do not return generic design inspiration only.
Always tie suggestions to:
- FaralYar routes
- real components
- mobile behavior
- theme behavior
- QA risk prevention

# References

Read these when relevant:
- `references/benchmark-principles.md`
- `references/brand-and-theme-system.md`
- `references/route-map.md`
- `references/page-requirements.md`
- `references/redesign-prompt-templates.md`
- `references/frontend-spec-patterns.md`
- `references/visual-qa-checklist.md`

# Script usage

Use `scripts/build_faralyar_ui_output.py` when you need a structured starting point for:
- audit
- redesign prompt
- frontend UI spec

Then expand it into a polished final response.