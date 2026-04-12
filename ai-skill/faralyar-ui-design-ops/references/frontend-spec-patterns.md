# Frontend spec patterns

## Required structure
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
12. accessibility and visual qa
13. implementation notes

## Component spec minimum
For each important component specify:
- purpose
- hierarchy level
- visual anatomy
- spacing
- typography role
- color usage
- border, radius, and shadow behavior
- states
- mobile behavior
- rtl behavior
- implementation cautions

## Minimum state set
For interactive components define:
- default
- hover
- focus
- active
- disabled

If relevant also define:
- loading
- error
- success
- selected
- empty
- populated
- expanded
- collapsed

## Critical components
Always expand carefully for:
- hero CTA block
- chat sidebar
- model picker
- composer
- upload UI
- file preview
- pricing card
- settings tabs
- form sections
- empty states
- table and list rows
- admin actions

## Upload component requirements
Always define:
- idle
- file selected
- invalid file
- uploading
- uploaded
- remove
- replace
- error

Never allow:
- native browser file input visuals
- disconnected file preview
- mismatched button heights

## Model picker requirements
Always define:
- default closed
- open
- hovered option
- selected option
- disabled option
- loading options
- no model available

## Chat composer requirements
Always define:
- empty
- typing
- file attached
- submitting
- disabled
- multiline expanded
- send error state

## Settings control requirements
Always define:
- untouched
- modified
- saving
- saved
- validation error
- destructive confirm state

## Full page spec pattern
Use when the whole page needs implementation-ready detail.

Required sections:
- objective
- structure
- key components
- theme behavior
- responsive behavior
- qa notes
- implementation cautions

## Component deep spec pattern
Use when a single component needs full implementation detail.

Examples:
- upload box
- pricing card
- model picker
- composer
- settings tab nav
- chat history item
- empty-state block

## Flow spec pattern
Use for multi-step surfaces:
- upload flow
- onboarding flow
- plan upgrade flow
- settings save flow

Required sections:
- steps
- screen states
- interaction rules
- error handling
- success feedback
- responsiveness
- implementation notes

## Frontend polish pass
Use when the UI exists but needs refinement.

Required sections:
- current weaknesses
- preserve list
- visual cleanup rules
- component consistency rules
- responsive fixes
- qa checklist