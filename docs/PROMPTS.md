# Prompts for Claude Code — one per module

**How to use this file**

1. Open the **Claude Code** panel in VS Code (not "Chat").
2. Start a **new conversation** for each module.
3. Switch to **Plan mode**, paste the module's prompt, and read the plan for the first task.
4. Approve, let Claude Code build and test, check the task's *Done when* in `docs/SPEC.md`, then say **"commit this"**.
5. Say **"next task"** to move on. Repeat until the module is done.
6. At the end, say **"module check"** (see the bottom of this file).

---

## M1 — Foundation

```
We are starting Module M1 (Foundation) from docs/SPEC.md, section 7. Read CLAUDE.md and docs/SPEC.md first, then summarise in 5 plain-English bullet points what we are building and the rules you must follow. Then work through tasks M1-T1 to M1-T7 in order. For each task: show me your plan, wait for my approval, build it, run the tests, show the output, explain it in plain English, and wait for me to say "commit this" before moving on. For M1-T3, explain every data format with a Dolo 650 example.
```

## M2 — Medicine Library

```
We are starting Module M2 (Medicine Library) from docs/SPEC.md, section 7. Work through tasks M2-T1 to M2-T6 in order, one at a time, with my approval at each step. Use only real published values with source links and quoted excerpts; mark anything unsourced as "estimate — not sourced". After M2-T2, show me a table of every value with its source and confidence for review. In M2-T4, build the Medicine screen so I can search and see sources, and tell me exactly how to open it in my browser.
```

## M3 — Simulation Engine & Digital Twin

```
We are starting Module M3 (Simulation Engine & Digital Twin) from docs/SPEC.md, section 7. Work through tasks M3-T1 to M3-T7 in order, one at a time, with my approval at each step. Validate the model against the analytical solution before using it. Every person-level adjustment must use a published relationship with its source. At the end, show me the profile screen and the drug-level chart, and demonstrate that lowering kidney function raises the curve.
```

## M4 — Population Groups & Group Testing

```
We are starting Module M4 (Population Groups & Group Testing) from docs/SPEC.md, section 7. Work through tasks M4-T1 to M4-T8 in order, one at a time, with my approval at each step. Use a fixed random seed for the virtual population and prove that two runs give identical results. Save every run with its full inputs, and never change an old run. At the end, show me the groups screen and the results screen with a full run of Dolo 650.
```

## M5 — Safety, Side Effects & Uncertainty

```
We are starting Module M5 (Safety, Side Effects & Uncertainty) from docs/SPEC.md, section 7. Work through tasks M5-T1 to M5-T7 in order, one at a time, with my approval at each step. Effective and toxic levels must have sources. Any ingredient pair without interaction data must say "not modelled — needs review". Every ranking must come from the numbers, not fixed text. At the end, show me the full results screen for a test medicine.
```

## M6 — Search Any Medicine & Review

```
We are starting Module M6 (Search Any Medicine & Review) from docs/SPEC.md, section 7 (see also sections 2.2 and 4.6). No paid API may be used. Work through tasks M6-T1 to M6-T7 in order, one at a time, with my approval at each step. Build the prepare-medicine command so I can run it with you, and make the extraction step swappable so a free local model can be added later. At the end, demonstrate the whole flow with a medicine that is not yet in the database.
```

## M7 — Users, Organisations & File Uploads

```
We are starting Module M7 (Users, Organisations & File Uploads) from docs/SPEC.md, section 7 (see also sections 2.7 and 5.1). Work through tasks M7-T1 to M7-T8 in order, one at a time, with my approval at each step. Store passwords only as secure hashes. At the end, help me create the first admin, add a test user, show that the test user is forced to change their password, and show that one organisation cannot see another's data.
```

## M8 — Reports & Run Comparison

```
We are starting Module M8 (Reports & Run Comparison) from docs/SPEC.md, section 7 (see also section 2.8). Work through tasks M8-T1 to M8-T4 in order, one at a time, with my approval at each step. Every report must carry the "Research use only — not for clinical decisions" label. At the end, show me a comparison of two runs and give me a PDF and an Excel report to open.
```

## M9 — New Medicines

```
We are starting Module M9 (New Medicines) from docs/SPEC.md, section 7 (see also section 2.4). Work through tasks M9-T1 to M9-T4 in order, one at a time, with my approval at each step. At the end, demonstrate all three cases (new mix of known ingredients, new compound with lab values, structure only) and show that each gets the correct reliability label.
```

## M10 — Go Live & Pilot

```
We are starting Module M10 (Go Live & Pilot) from docs/SPEC.md, section 7. Work through tasks M10-T1 to M10-T6 in order, one at a time, with my approval at each step. Write every server instruction step by step for someone who is not a programmer. Set up nightly backups and prove that a restore works on a test copy.
```

---

## Prompts for any time

**Next task**
```
Next task. Show me your plan first.
```

**Module check (end of every module)**
```
Module check: run all tests, start the app, and give me a short list of what to click to check every task in this module against its "Done when" in docs/SPEC.md.
```

**Demo preparation (before a client demo)**
```
Prepare the client demo for this module: make sure the demo medicines and runs are ready, then give me a step-by-step demo script in plain English with what to click and what to say at each step.
```

**Other useful prompts**

- "Explain what you just did in simple language."
- "Show me the test results."
- "What could go wrong with this?"
- "Undo the last change."
- "Update docs/SPEC.md with the decision we just made, and tell me what changed."
