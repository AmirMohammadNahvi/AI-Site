# FaralYar brand and theme system

## Brand anchors
- green: `#28ab88`
- navy: `#013366`

## Product mood
- smart
- trustworthy
- Persian-first
- premium but practical
- calm, not flashy

## Light mode direction
Use:
- pale cool or softly tinted background
- visible surfaces
- strong navy text
- restrained shadows
- clear card separation
- readable muted text

Avoid:
- blank white emptiness
- washed-out cards
- low-contrast body text
- giant dead areas with no rhythm

## Dark mode direction
Use:
- layered navy surfaces
- distinct page, panel, card, and elevated levels
- restrained accent usage
- soft borders for separation
- readable text contrast
- calmer tonality than the current dark mode

Avoid:
- near-black walls
- neon-heavy glow
- emotionally dull heaviness
- panels blending into background
- weak hierarchy between shell, panel, card, and input

## Suggested semantic tokens

### Light
- bg: `#f7faf9`
- bg-tint: `#eef7f4`
- surface: `#ffffff`
- surface-2: `#f3f7f8`
- border: `#d8e5e4`
- border-strong: `#bdd4d0`
- text: `#0c1b33`
- text-muted: `#5b6b82`
- primary: `#28ab88`
- primary-hover: `#219676`
- focus-ring: `rgba(40, 171, 136, 0.28)`

### Dark
- bg: `#06162c`
- bg-alt: `#0a1d36`
- surface: `#0d223f`
- surface-2: `#132b4d`
- surface-3: `#18345b`
- border: `rgba(201, 223, 234, 0.10)`
- border-strong: `rgba(201, 223, 234, 0.18)`
- text: `#eef6ff`
- text-muted: `#b7c7db`
- primary: `#28ab88`
- primary-hover: `#2fc59d`
- focus-ring: `rgba(40, 171, 136, 0.32)`

## Radius system
- sm: 10px
- md: 14px
- lg: 18px
- xl: 24px

## Shadow guidance

### Light mode
Use soft depth.
Avoid muddy gray shadows.

### Dark mode
Prefer tone separation and borders over giant blur.

## Typography guidance
Persian headings should feel strong and confident.
Body text should remain readable, not too faint or too condensed.

Maintain distinction between:
- display headline
- section title
- card title
- body text
- helper text
- badge text

## Interaction guidance
Use green primarily for:
- primary CTA
- active state
- selected controls
- focus states
- success cues
- live indicators

Use navy and dark-blue tones for:
- content structure
- text gravity
- secondary actions
- surface layering

## Consistency rules
- keep radius values consistent
- align control heights
- do not mix unrelated shadow styles
- do not overuse gradients
- do not use green everywhere