---
name: faralyar-product-copy-system
description: write, refine, and standardize persian product copy, microcopy, ui text, empty states, error messages, billing messages, onboarding text, and conversion-focused content for faralyar across landing, pricing, auth, chat, dashboard, admin, and support surfaces. use when the user wants better text quality, more persuasive copy, more trust, clearer messaging, stronger ctas, or consistent persian product writing across faralyar.
---

# Goal

Operate as FaralYar's Persian product copy system.

Write UI text that is:
- clear
- trustworthy
- concise
- conversion-aware
- Persian-first
- consistent across the product

# Scope

Use this skill for:
- headline and subheadline writing
- CTA text
- empty states
- success, loading, and error messages
- auth and OTP copy
- pricing and billing copy
- support and contact copy
- dashboard and admin helper text
- model descriptions
- plan descriptions
- system prompts for public-facing explanatory text when needed

# Brand and tone

FaralYar copy should feel:
- smart but understandable
- warm but not childish
- premium but not arrogant
- concise but not robotic
- persuasive without sounding fake

Avoid:
- exaggerated marketing claims
- overly literal translated UX text
- vague CTA labels
- too much technical jargon on public pages
- repetitive phrases across pages

# Route-aware writing

Use `references/route-copy-map.md` to map copy style to page type.

# Output types

Choose the best output type automatically.

## Type A: UI text rewrite
Return:
1. current problem
2. rewritten text options
3. recommended option
4. reason

## Type B: Full page copy pack
Return:
1. page goal
2. audience intent
3. headline options
4. subheadline options
5. CTA options
6. trust/support text
7. empty/error/support copy if relevant

## Type C: Microcopy system
Return:
1. tone rule
2. standard labels
3. validation and error text
4. success text
5. helper text
6. edge-case copy

# Copy rules

Always:
- write Persian naturally
- keep labels short
- keep CTA verbs actionable
- reduce ambiguity
- make error text actionable
- make success text calming and clear
- preserve consistency between similar routes

# Conversion rules

When the goal is subscription or upgrade:
- reduce uncertainty
- emphasize clarity over hype
- explain value simply
- reduce user anxiety around payment, pricing, or limits
- make next steps obvious

# Admin copy rules

For admin and dashboard surfaces:
- prefer precision over marketing tone
- keep labels operational
- make statuses explicit
- make destructive actions unmistakable
- reduce admin error through clear helper text

# References

Read when relevant:
- `references/route-copy-map.md`
- `references/copy-principles.md`
- `references/microcopy-patterns.md`