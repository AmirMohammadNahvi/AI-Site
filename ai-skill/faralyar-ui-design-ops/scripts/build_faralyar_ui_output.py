import argparse

AUDIT_TEMPLATE = """MODE: visual_audit

TARGET:
{target}

PRIMARY ISSUES:
{issues}

CONSTRAINTS:
- Preserve FaralYar brand identity
- Use #28ab88 and #013366 as brand anchors
- Persian RTL first
- Design both light and dark mode
- Dark mode must be layered and calm
- Mobile-safe responsive behavior required
- Prevent overflow, clipping, hierarchy issues, and native-looking file controls

RETURN:
1. visual diagnosis
2. strengths to preserve
3. redesign direction
4. light mode direction
5. dark mode direction
6. responsive risks
7. qa checklist
"""

PROMPT_TEMPLATE = """MODE: redesign_prompt

TARGET:
{target}

PRIMARY ISSUES:
{issues}

WRITE A COPY-PASTE REDESIGN PROMPT FOR FARALYAR THAT:
- preserves brand identity
- uses #28ab88 and #013366
- designs for Persian RTL
- supports light mode and dark mode
- avoids heavy, gloomy dark mode
- fixes hierarchy and spacing issues
- keeps upload UI fully custom if relevant
- defines mobile, tablet, and desktop behavior
- prevents overflow, clipping, weak contrast, and native-looking controls

RETURN:
1. prompt title
2. prompt type
3. final prompt
4. shorter version
5. expected improvements checklist
"""

SPEC_TEMPLATE = """MODE: frontend_ui_spec

TARGET:
{target}

PRIMARY ISSUES:
{issues}

WRITE A FRONTEND-READY UI SPEC FOR FARALYAR THAT INCLUDES:
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

CONSTRAINTS:
- realistic and buildable
- Persian RTL first
- brand anchors: #28ab88 and #013366
- no native-looking upload control
- no heavy dark mode
- no mobile overflow
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["audit", "prompt", "spec"])
    parser.add_argument("--target", required=True)
    parser.add_argument("--issues", default="improve hierarchy, polish, and responsiveness")
    args = parser.parse_args()

    if args.mode == "audit":
        print(AUDIT_TEMPLATE.format(target=args.target, issues=args.issues))
    elif args.mode == "prompt":
        print(PROMPT_TEMPLATE.format(target=args.target, issues=args.issues))
    else:
        print(SPEC_TEMPLATE.format(target=args.target, issues=args.issues))

if __name__ == "__main__":
    main()