# Redesign prompt templates

## Full-page redesign prompt

You are redesigning the `{page_name}` page for FaralYar, a Persian rtl AI product.
Preserve FaralYar brand identity using `#28ab88` and `#013366`.
Take inspiration from ChatGPT for low-friction clarity, Perplexity for trust and continuity, AvalAI for clear product communication, and Houshan for capability discoverability, without copying any layout.
Design both light mode and dark mode.
Dark mode must be layered and calm, not heavy or gloomy.
Light mode must feel premium and readable, not washed out.
Design for mobile, tablet, desktop, and wide screens.
Prevent visual bugs such as overflow, clipped controls, weak hierarchy, native-looking file inputs, rtl misalignment, and inconsistent spacing.
Return:
1. visual diagnosis
2. redesign direction
3. section structure
4. component rules
5. responsive behavior
6. qa checklist

## Component redesign prompt

You are redesigning the `{component_name}` component in FaralYar.
This is a Persian rtl interface.
Preserve the FaralYar brand with `#28ab88` and `#013366`.
Fix the current issues: `{issue_list}`.
Define visual structure, states, spacing, dark mode behavior, light mode behavior, mobile behavior, rtl behavior, and anti-bug rules.
Return:
1. diagnosis
2. redesign direction
3. anatomy
4. states
5. responsive notes
6. qa checklist

## Audit-to-redesign prompt

Audit the current `{target}` surface in FaralYar first.
Identify strengths to preserve and weaknesses to fix.
Then propose a redesign that remains realistic for production frontend implementation.
Support both light mode and dark mode.
Design for Persian rtl and mobile-first safety.
Return:
1. audit
2. preserve list
3. redesign strategy
4. component recommendations
5. responsive fixes
6. qa checklist

## Frontend handoff prompt

Write a frontend-ready UI specification for `{target}` in FaralYar.
Include:
- layout
- components
- states
- light and dark theme rules
- responsive behavior
- rtl behavior
- accessibility and visual qa checks

Keep the output implementation-oriented and buildable.

## Chat page prompt template

Generate a redesign for the FaralYar chat page.
This is the core product experience and must feel focused, premium, light to use, and ready for long Persian rtl conversations.
Preserve the FaralYar brand using `#28ab88` and `#013366`.
Improve the chat sidebar, model picker, empty state, message list, composer, and file upload flow.
The file upload must not look like a native browser control.
Design a custom upload trigger, file preview, remove and replace action, and loading and error states.
Make the dark mode layered and readable rather than overly dark and emotionally heavy.
Make the light mode clean and calm rather than flat.
Specify mobile behavior for drawer/sidebar, sticky composer, keyboard-safe spacing, and top controls.
Prevent visual bugs such as overflow, mismatched control heights, low-contrast placeholders, rtl misalignment, and fixed element collisions.
Return:
1. visual diagnosis
2. strengths to preserve
3. redesign direction
4. composer and upload redesign
5. sidebar redesign
6. empty-state redesign
7. responsive behavior
8. qa checklist

## Landing page prompt template

Generate a redesign for the FaralYar landing page.
The page is a Persian rtl AI product landing page and must communicate what the product does, why it is useful, and what the user should do next in the first screen.
Preserve the FaralYar brand using `#28ab88` and `#013366`.
Take inspiration from the low-friction clarity of ChatGPT, the trust-oriented structure of Perplexity, the explicit product communication of AvalAI, and the capability discoverability of Houshan, without copying any layout directly.
Improve hero hierarchy, CTA prominence, use-case surfacing, model and capability visibility, section rhythm, trust cues, and visual polish.
Design both light mode and dark mode.
In dark mode, avoid a heavy, sad, overly dense look.
In light mode, avoid washed-out surfaces and weak contrast.
Make the design fully responsive for mobile and tablet.
Ensure Persian typography, rtl spacing, and icon direction feel intentional.
Prevent visual bugs such as low contrast, poor hierarchy, overflow, inconsistent spacing, or weak empty states.
Return:
1. visual diagnosis
2. redesign direction
3. page structure
4. section-by-section recommendations
5. component styling rules
6. responsive behavior
7. qa checklist

## Pricing page prompt template

Generate a redesign for the FaralYar pricing page.
This page must explain plan differences clearly and make the recommended plan obvious.
Preserve the FaralYar brand using `#28ab88` and `#013366`.
Improve plan card hierarchy, billing explanation, CTA prominence, comparison clarity, and trust-building details.
Design both dark mode and light mode.
Ensure mobile stacking is clean and comparison information remains readable.
Prevent visual bugs such as undifferentiated cards, weak CTA hierarchy, cramped features, and confusing recommendation badges.
Return:
1. page diagnosis
2. pricing structure proposal
3. plan-card redesign rules
4. theme behavior
5. responsive behavior
6. qa checklist

## Settings modal prompt template

Generate a redesign for the FaralYar settings and account modal.
This is a Persian rtl product settings surface and must feel compact, calm, organized, and polished.
Preserve the FaralYar brand using `#28ab88` and `#013366`.
Improve section grouping, tab clarity, field layout, destructive actions, form control polish, and modal spacing.
Design both dark mode and light mode.
Define mobile behavior explicitly, including full-screen sheet behavior, tab collapse behavior, and overflow handling.
Prevent visual bugs such as clipped modal sections, inconsistent control sizing, poor tab emphasis, or hard-to-scan settings groups.
Return:
1. diagnosis
2. redesign direction
3. layout and tab rules
4. form and action rules
5. responsive behavior
6. qa checklist