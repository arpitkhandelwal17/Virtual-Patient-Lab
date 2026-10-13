# Virtual Patient Lab — rules for Claude Code

Read this file and `docs/SPEC.md` at the start of every session. The spec is the source of truth for what to build. If something in a request conflicts with it, stop and ask.

## What this project is

A research tool for institutes. A researcher searches any medicine (for example Dolo 650), and the app tests it against a library of prebuilt population groups and their combinations, then reports how each group is likely to respond: drug levels over time, risk flags, side effects by body system, and uncertainty. An optional single-person "digital twin" can be tested alongside the groups.

## About the owner

The project owner is not a programmer. Always:

- Explain what you built in plain English, without jargon. Say what it does, not how the code works.
- Show the actual output of tests or runs, then say in one or two sentences what it means.
- When you need a decision, give 2 or 3 options with a recommendation, not an open question.
- Give exact commands to type, and say which window to type them in.

## Hard rules — never break these

1. **Research use only.** Every result screen, report and export says: "Research use only — not for clinical decisions."
2. **No real patient data.** Populations come from public survey data (NHANES, NFHS-5) or are synthetic. Never store identifiable patient information.
3. **Every number has a source.** Each drug parameter stores: value, unit, source URL, a short quoted excerpt from the source, retrieval date, and confidence. If no source is found, store it as `"estimate — not sourced"`. Never present an unsourced value as verified.
4. **No guessed numbers.** All results come from tested, deterministic code. Never type a number into results, tests' expected values, or the UI from your own memory without a cited source or a calculation.
5. **Reproducible.** Use a fixed random seed wherever a virtual population is generated. The same inputs must give the same outputs.
6. **Free sources only.** Use DailyMed, openFDA, PubMed/PMC, FDA and EMA reviews, CPIC, NHANES, NFHS-5, KDIGO. No paywalled sources (for example full DrugBank) unless the owner says a licence exists.
7. **Never assume safety.** If interaction data for a pair of ingredients is missing, label it "not modelled — needs review".
8. **Any medicine can be searched.** There is no fixed medicine list. On first search, fetch label data for free (DailyMed, openFDA, PubMed list) and show it instantly. Simulation numbers that need extracting from text go into a "Data preparation" queue and are prepared with the `prepare-medicine` command run through Claude Code. Save everything with its sources, labelled "unverified". Later runs reuse the saved copy. Only a reviewer can change the label to "verified".
9. **Brand-new compounds** need lab-measured inputs; without them, label results "exploratory estimate" and show wide uncertainty.
10. **Secrets.** Passwords and API keys go in a `.env` file, which is listed in `.gitignore` and never committed. Never print secret values in chat.
11. **No paid APIs.** The owner pays only for the existing Claude plan. The app must never call the Claude API or any other paid service, and must run without any API key. Keep the extraction step pluggable so a free local model (Ollama) can be added later.

## Tech stack — do not change without asking

- **Engine and server:** Python 3.13, uv, FastAPI, Pydantic, NumPy, SciPy, SALib, PyMC (later phase), RDKit, Polars, httpx, Biopython
- **Storage:** PostgreSQL (SQLAlchemy and Alembic), Parquet files with DuckDB for large result tables
- **Screens:** React, TypeScript, Vite, Tailwind CSS, Apache ECharts, TanStack Query, React Hook Form and Zod
- **Reports:** Playwright for PDF, XlsxWriter for Excel
- **Tests:** pytest and Hypothesis (Python), Vitest and Playwright (screens)
- **Deployment (later):** Docker Compose and Caddy on Ubuntu

If a better option seems necessary, explain why and ask before switching.

## How we work

1. **Modules and tasks.** We build in the 10 modules of `docs/SPEC.md` section 7 (M1 to M10). One module per conversation; within a module, one task at a time (for example M3-T2), in order.
2. **Plan first.** For every task, propose your plan and wait for approval before writing code.
3. **End to end.** Each module includes its screen, so the result can be seen in the browser and shown to the client. Never leave all screens for later.
4. **Small steps.** Build a little, run it, show the output, explain it. Put the task number in every commit message (for example `M3-T2: kidney and liver adjustments`).
5. **Tests for every calculation.** Validate the drug-level model against a known analytical solution or published example before trusting it.
6. **Parameter review.** After adding any drug or organ-function values, show the owner a table of every value with its source and confidence for review.
7. **Never commit without approval.** Only run `git commit` after the owner says the step works. Use clear commit messages.
8. **Keep the docs current.** If a decision changes the plan, update `docs/SPEC.md` and say what changed.

## Development environment

- Windows, VS Code, PowerShell terminal.
- Python 3.13 is installed. Git is installed.
- Node.js and PostgreSQL may not be installed yet. Check before a phase that needs them, and give install steps if missing.
