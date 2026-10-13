# Virtual Patient Lab — Project Specification

**Owner:** Appbay Technologies · **Version:** 2.2 (modules, single-developer timeline) · **Date:** 12 October 2026
**Status:** Approved for build · **Build tool:** Claude Code

This is the single source of truth for the project. It says **what** we are building, **how** it works, **which technologies** we use and **why**, and **the order** in which we build it.

---

## 1. What we are building

A web application that lets researchers test, on a computer, how a medicine is likely to behave in different groups of people, before or alongside lab and clinical work.

A researcher:

1. Searches for **any medicine** (for example *Dolo 650*) or creates a new one.
2. The app tests it automatically against a **library of prebuilt population groups** (age, kidney function, smokers, genotype and so on) and their combinations.
3. The app shows, for each group, the **predicted drug levels in the blood over time**, how many people would be **above the toxic level or below the effective level**, **side effects by body system**, how **uncertain** each result is, and the **published source** behind every number.
4. Optionally, the researcher can also test **one individual profile** (a "digital twin").

**Who uses it:** researchers, formulation scientists and trainees in research institutes, contract research organisations (CROs), universities and small or mid-size pharma R&D teams.

**What it is not:** it does not prescribe, diagnose or advise on real patients. Every screen and report says **"Research use only — not for clinical decisions."**

### 1.1 Why it is useful (positioning)

Established tools (Simcyp, GastroPlus, Jinkō) are built for expert modellers in large pharma, sold by enterprise licence, and need training. Our app is:

- **Usable without modelling training:** type a medicine, pick groups, click run.
- **Automatic across groups:** tests every group, pair and trio of groups and ranks those most at risk.
- **Transparent:** every number links to its published source and shows whether a reviewer has verified it.
- **India-first:** Indian brands and Indian population data (NFHS-5) are built in.
- **Affordable:** built entirely on free and open-source technology.

It is **not** a regulatory tool. Its results are for research, screening, teaching and early decisions.

---

## 2. How the application works

### 2.1 The four screens

| # | Screen | What the researcher does | What the app does |
|---|---|---|---|
| 1 | **Medicine** | Chooses *"Test an existing medicine"* or *"Create a new medicine"*. Searches by brand or generic name, or enters compounds and mixing percentages. Can add, delete or edit ingredients. | Shows full composition (active and inactive ingredients, strengths, dosage form, manufacturer, label dose) and the pharmacology values for each active ingredient, each with its source and a *Verified* / *Unverified* label. |
| 2 | **Population groups** | Picks one or more groups from the prebuilt library, and the combination depth (singles, pairs, trios). Optionally adds one individual profile. | Shows how many virtual people fall in each selected group and warns when a combination is too small to give reliable results. |
| 3 | **Run** | Clicks *Run simulation*. | Simulates the medicine in every virtual person, then calculates results for every group and combination. |
| 4 | **Results** | Reviews results, compares groups, downloads a report. | Per group: drug-level chart over time with the group's range, peak level and time, share above toxic / below effective level, risk flag, side effects by body system, interaction warnings, uncertainty and what drives it, ranking of groups most at risk. Export to PDF or Excel. |

### 2.2 Any medicine can be searched

There is **no fixed list** of medicines and no limit.

**No paid API is used.** The only cost is the owner's existing Claude plan. (See section 4.6.)

1. **Medicine already in the library:** results are instant.
2. **First search for a new medicine:** the app instantly fetches what it can from free official sources with no AI: composition, label dose, side effects, warnings and interaction text from DailyMed and openFDA, plus a list of relevant PubMed papers. The researcher sees this straight away.
3. **Simulation numbers** (absorption, clearance, safe and toxic levels) are usually written inside label and paper text, so they need extracting. The app adds the medicine to a **"Data preparation" queue** and shows the researcher *"Simulation data being prepared"*.
4. **The team prepares the data** using Claude Code, which is covered by the existing plan. A ready-made command (for example `uv run prepare-medicine "metformin"`) fetches the sources, extracts the numbers with quoted excerpts, and saves them as **Unverified**. The researcher is notified that the medicine is ready to simulate.
5. **Every later search** reuses the saved copy, so results are fast and identical every time. Saved data is re-checked against its sources on a schedule.
6. **A reviewer** (pharmacology expert) can check the values and mark the medicine **Verified**.
7. **Optional, still free:** if a powerful enough computer is available, a local open-source AI model (via Ollama) can do step 4 automatically and instantly, with no API cost. Values extracted this way also stay **Unverified** until reviewed. The extraction step is built as a pluggable component so this can be switched on later without rebuilding.

Why save instead of fetching every time: results must be repeatable, saved data is instant, extraction work happens only once per medicine, and only saved data can be reviewed.

**Indian brands** (for example Dolo 650 = paracetamol 650 mg) have no free machine-readable source. Their composition is entered once from the pack insert; the research data for the active ingredient is then fetched automatically.

### 2.3 Data completeness labels

Every result shows how complete and trustworthy its data is:

| Label | Meaning |
|---|---|
| **Verified** | A reviewer has checked every value against its source |
| **Unverified** | Fetched live and extracted by AI; not yet checked |
| **Partial data** | Some values are missing; the app lists which ones and what it could not calculate |
| **Predicted from lab data** | New compound simulated from lab measurements entered by the researcher |
| **Exploratory estimate** | New compound simulated from its chemical structure only; low reliability, wide uncertainty |

### 2.4 Creating a new medicine

| Case | Example | How the app tests it |
|---|---|---|
| **New mix of known ingredients** | Paracetamol 500 mg + caffeine 65 mg | Simulates each ingredient from its published data; checks published interactions; flags pairs with no data as *"not modelled — needs review"* |
| **Brand-new compound with lab data** | New molecule with measured solubility, permeability, protein binding, clearance | Predicts drug levels from the lab values; label *"Predicted from lab data"* |
| **Brand-new compound, structure only** | New molecule with only its chemical formula | Estimates properties from the structure with free tools (RDKit and similar); label *"Exploratory estimate"*; tells the researcher which lab tests would make it reliable |

### 2.5 Population groups and combinations

- The app ships with ready-made **categories and levels**: age band, sex, body weight, kidney function, liver function, smoking, alcohol, fitness, pregnancy, metaboliser genotype, and common conditions such as diabetes. Administrators can add or edit them later.
- The app builds **one large virtual population** (for example 100,000 people) from public survey data (NHANES, NFHS-5), so traits stay realistically linked (older people tend to have lower kidney function, for example). It uses a **fixed random seed**, so the same population is produced every time.
- Each group is a **slice** of that population. Order does not change a group, so only **combinations** matter, not permutations.
- By default the app reports every **single group, pair and trio**. Deeper combinations run on request. Any combination with too few virtual people is **flagged, not reported**, because its results would be unreliable.

### 2.6 The digital twin (one individual)

No study exists for one specific person. Published research gives (a) how a drug behaves on average and (b) how that changes with body features: kidney function, liver function, weight, age, genotype, smoking. The app starts from the average values, adjusts them for the person's own values, and simulates their drug levels hour by hour.

The result is a **most-likely curve with an uncertainty range**, plus which missing information would narrow it most (for example *"a recent kidney test"*). If a real blood test result is entered later, the twin is recalibrated and the range narrows.

### 2.7 Users, login and roles

**Organisations.** Each research institute has its own workspace. Users only see their own organisation's medicines, runs and reports. (Published drug data fetched from public sources can be shared across organisations; each organisation's own new medicines and runs are private.)

**Roles**

| Role | Can do |
|---|---|
| **Researcher** | Search medicines, create new medicines, run simulations, view and download reports |
| **Reviewer** | Everything a researcher can, plus check fetched data and mark medicines *Verified* |
| **Admin** | Everything, plus add and deactivate users, assign roles, and edit population categories and levels |

**What is stored about each user:** name, email, organisation, role, active/inactive, created date, last login. **Passwords are never stored as typed.** Only a secure one-way hash is stored (Argon2 or bcrypt), so nobody, including admins, can read a password.

**Setting up accounts (no email service needed)**

1. **First admin (one time only):** after installation, the owner runs a setup command in the terminal (for example `uv run create-admin`). It asks for email and password, then creates the first admin account. The command refuses to run again once an admin exists, unless explicitly forced.
2. **Adding users:** the admin opens the **Users** page, clicks **Add user**, and enters name, email, organisation and role. The app generates a **temporary password** shown once to the admin, who shares it with the user directly.
3. **First login:** a user signing in with a temporary password must **set a new password immediately** before using the app.
4. **Forgotten password:** the admin resets it from the Users page, which issues a new temporary password (same forced-change rule).

**Security rules**

- Minimum password length of 10 characters.
- Temporary passwords expire if unused (for example after 7 days).
- Repeated failed logins briefly lock the account.
- Sessions expire after a period of inactivity.
- Every login, user change and *Verified* approval is recorded in an audit log (who, what, when).

**Later options (not in version 1):** email invite links and self-service "Forgot password" (needs an email service), "Sign in with Google / Microsoft", and two-step verification.

### 2.8 Re-testing a medicine with changes

Every test is saved as a separate **run**. Running again never overwrites an earlier run.

| What the researcher changes | What the app does |
|---|---|
| **Ingredient amounts or composition** | Saves the changed recipe as a new **version** of the medicine (for example *Dolo 650 — v2, paracetamol 500 mg*). The original medicine and its earlier runs stay unchanged. |
| **Population groups, categories or combination depth** | Uses the **same virtual population** (same fixed seed) and slices it differently. No new people are generated, so differences come only from the changed selection. |
| **Both** | Both of the above. |

**What is reused:** the published drug data (absorption, clearance, safe and toxic levels, side effects) is already saved, so nothing is fetched again. Only the simulation is recalculated, which takes seconds.

**Each run records:** who ran it, when, the exact medicine version and amounts, the groups and combination depth, the population version, the drug-data version used, and the software version. Opening an old run always shows exactly what was tested and the original results, even if drug data was later updated or verified.

**Compare runs:** the researcher can select two or more runs and see them **side by side**: what changed in the inputs (highlighted), and how drug levels, risk flags and group rankings changed. The comparison can be exported in the report.

**Re-run with latest data:** if the drug data has been updated or verified since an old run, the app shows a notice and offers *"Re-run with latest data"*, which creates a new run rather than changing the old one.

### 2.9 Scientific approach

| Step | Method | Notes |
|---|---|---|
| Drug levels over time | One-compartment model with first-order absorption (version 1); two-compartment where published data supports it | Validated against the known analytical solution before use |
| Person-level adjustments | Clearance and volume scaled by weight, kidney function (eGFR), liver function, age and genotype, using published relationships | Each relationship stores its source |
| Population | Monte Carlo simulation over the virtual population, fixed seed | Same inputs always give the same outputs |
| Safety flags | Predicted peak and exposure compared with published effective and toxic levels | Flags: on target / check dose / risk |
| Interactions | Every pair of active ingredients checked against published interaction data | Missing data is never treated as safe |
| Side effects | Label-listed adverse reactions grouped by body system, with published frequencies | Adverse-event reports (openFDA) shown only as signals, never as rates |
| Uncertainty | Sensitivity analysis (Sobol indices) shows which inputs drive uncertainty | Ranked list of real-world tests that would reduce it most |
| Recalibration | Bayesian update when measured blood levels are entered (version 2) | |

---

## 3. Data sources (all free)

| Source | What it provides | Used for |
|---|---|---|
| DailyMed (US National Library of Medicine) | US drug labels: ingredients, clinical pharmacology, interactions, adverse reactions | Composition, label values, side effects |
| openFDA | Labels as JSON; adverse-event reports from 2004 | Label lookup; safety signals only |
| PubMed / PMC (NCBI E-utilities) | Published pharmacokinetic studies | Absorption, clearance, distribution values with citations |
| FDA approval reviews, EMA assessment reports | Regulator summaries of trial pharmacology | Cross-checking values |
| CPIC guidelines | Effect of genes (CYP2D6, CYP2C19 and others) on drug levels | Metaboliser genotype |
| NHANES (US), NFHS-5 (India) | Population body measures and lab values | Building the virtual population |
| KDIGO guidelines | Kidney function categories | Kidney-impairment groups |
| Manufacturer pack inserts (India) | Composition of Indian brands | Indian medicines, entered by hand and reviewed |

**Excluded:** paid sources such as full DrugBank, Simcyp and GastroPlus, unless a licence is bought later.

---

## 4. Technology stack and why

Every choice is **free, widely used, and well known to Claude Code**. That keeps the build fast and makes help easy to find.

### 4.1 Architecture

```
 Researcher's browser
        │
   React screens  ──────►  FastAPI server (Python)
                              │
          ┌───────────────────┼────────────────────┬──────────────────────┐
          ▼                   ▼                    ▼                      ▼
  Simulation engine      PostgreSQL         Parquet + DuckDB        Live sources
  (NumPy, SciPy,      (users, medicines,   (virtual population,   (DailyMed, openFDA,
   SALib)              sources, groups,      simulation results)    PubMed)
                       run history)
```

The screens never touch data directly. Every number shown comes through the server from the engine or the database.

### 4.2 Backend and simulation engine

| Technology | What it does here | Why we chose it | Why not the alternatives |
|---|---|---|---|
| **Python 3.13** | Language for the engine and server | Nearly all scientific and drug-modelling libraries are written for Python | R is weak for web apps; Java, C# and JavaScript have few science libraries |
| **uv** | Installs libraries, manages the environment | Very fast; identical setup on every machine with one command | pip is slower and versions drift; Conda is heavy and confusing |
| **FastAPI + Uvicorn** | Web server and API | Simple, fast, documents the API automatically | Django is heavy for our needs; Flask needs more added by hand |
| **Pydantic** | Data formats and input checking | Validates every input and exports JSON schemas | Marshmallow is older and more manual |
| **NumPy, SciPy** | Drug-level maths | Global standard; fast enough for 100,000 people in seconds | MATLAB is paid; hand-written maths is risky |
| **SALib** | Finds what drives uncertainty | Best-known free sensitivity-analysis library | Building it ourselves is slow and hard to validate |
| **PyMC** | Recalibrates with real lab results (version 2) | Free, mature, used in drug research | NONMEM is paid; Stan is harder to set up on Windows |
| **RDKit** | Reads chemical structures of new compounds | Standard free chemistry toolkit | ChemAxon is paid; Open Babel has fewer drug features |
| **Polars** | Large population tables | Much faster than older table libraries | pandas is slower and memory-hungry at our size |
| **httpx, Biopython (Entrez)** | Live fetch from DailyMed, openFDA, PubMed | Official free APIs; tested PubMed connector | Scraping websites is fragile and may break site rules |
| **pytest, Hypothesis** | Tests every calculation | Standard; Hypothesis tries thousands of odd inputs | unittest is wordier and less capable |

### 4.3 Data storage

| Technology | What it does here | Why we chose it | Why not the alternatives |
|---|---|---|---|
| **PostgreSQL** | Users, organisations, medicine library with sources and review status, groups, run history | Free, reliable, many users at once, suits linked records | MySQL is weaker for complex data; MongoDB suits loose documents; SQLite allows one writer; Oracle and SQL Server are paid |
| **SQLAlchemy + Alembic** | Connects Python to the database; tracks every database change | Safe changes that can be undone | Raw database commands are error-prone and untracked |
| **Parquet (PyArrow)** | Stores virtual populations and results | Compact and fast for millions of rows | CSV is large and slow; storing in PostgreSQL slows the main database |
| **DuckDB** | Queries results by any group combination | Answers in seconds with no extra server | Spark or Databricks are heavy and built for far larger data |

### 4.4 Screens

| Technology | What it does here | Why we chose it | Why not the alternatives |
|---|---|---|---|
| **Node.js (LTS)** | Build tool for the screens (development only) | Required by the frontend tools | — |
| **React + TypeScript** | The four screens | Most widely used; Claude Code's strongest area; TypeScript catches mistakes early | Angular is heavier; Vue less common; Streamlit weak for multi-user apps |
| **Vite** | Builds and previews the screens | Instant start; live preview while building | Create React App is discontinued; Webpack is slow |
| **Tailwind CSS** | Styling | Matches the approved design and brand colours quickly | Bootstrap looks generic; plain CSS is slower to keep consistent |
| **Apache ECharts** | Drug-level charts with shaded group ranges | Handles large data and scientific bands well | Chart.js too basic; Recharts slows on large data; Plotly heavy |
| **TanStack Query** | Talks to the server | Handles loading, errors and caching | Hand-written code is repetitive and error-prone |
| **React Hook Form + Zod** | Medicine and composition forms | Checks entries before sending | Formik is older and slower |
| **Vitest, Playwright** | Screen tests | Fast unit tests; Playwright clicks through like a real user | Jest slower with Vite; Selenium older and flakier |

### 4.5 Reports, login and running the app

| Technology | What it does here | Why we chose it | Why not the alternatives |
|---|---|---|---|
| **Playwright (print to PDF)** | PDF reports | Reports look exactly like the screens | ReportLab needs every layout drawn in code; WeasyPrint hard to install on Windows |
| **XlsxWriter** | Excel export | Simple and reliable, supports formatting | openpyxl is for editing existing files |
| **FastAPI security tools** | Login, organisations, roles (researcher, reviewer, admin) | Built in; hashed passwords and signed tokens | Keycloak is a whole separate system; Auth0 is paid beyond small use |
| **Git + GitHub (Appbay-AI)** | Version history and backup | Full history; free private repositories | Company already uses GitHub |
| **Docker Compose** | Starts database, server and screens together | One command, same on every server | Manual setup is slow; Kubernetes far too complex |
| **Caddy** | Secure web address (HTTPS) | Sets up HTTPS automatically, free | Nginx needs HTTPS configured by hand |
| **Own Ubuntu server** | Hosting | Free, no usage limits, data stays in-house | Free cloud plans have limits; paid cloud later if needed |

### 4.6 Cost policy: no paid API

**Decision:** the project pays for nothing beyond the owner's existing Claude plan. The Claude API (pay per use) is **not** used.

Fetching labels and papers is free. Pulling numbers **out of label and paper text** needs an AI, which is handled like this:

| Method | Cost | Speed | Used for |
|---|---|---|---|
| **Claude Code data-preparation command** (version 1 default) | Covered by the existing Claude plan | Minutes per medicine, run by the team | Preparing every new medicine in the "Data preparation" queue |
| **Local open model via Ollama** (optional, later) | Free, but needs a powerful computer (ideally with a good graphics card) | Automatic, near-instant | Switching on automatic extraction without paying for an API |
| Claude API | Pay per use | Automatic | **Not used** (by owner decision) |

Rules that apply whichever method is used:

- The app itself never calls a paid AI service. No API key is required to run it.
- Extracted values always carry a quoted excerpt and source link, and stay **Unverified** until a reviewer checks them.
- The extraction step is a separate, pluggable component, so a different method can be switched on later without rebuilding the app.

(The company's startup programme API credits could be used for automatic extraction while they last, at no cost. They are not part of the design, because the app must keep working after the credits run out.)

---

## 5. Data that every value must carry

Every drug or physiology parameter is stored with:

| Field | Example |
|---|---|
| Value and unit | `0.27` L/h/kg |
| Source URL | DailyMed, PubMed or regulator link |
| Quoted excerpt | The exact sentence or table cell the value came from |
| Retrieved date | 2026-10-09 |
| Confidence | high / medium / low |
| Status | verified / unverified / estimate — not sourced |
| Reviewed by and when | Filled when a reviewer approves it |

(The example value above shows the format only; it is not a real drug parameter.)

Main records the database holds: organisations, users and roles (with hashed passwords only), audit log; medicines, ingredients and compositions; parameters (as above); interaction records; side-effect records; population categories and levels; virtual population versions; simulation runs and their settings; group results. Exact schemas are designed in task M1-T3.

### 5.1 File storage

All files live on the app's own server: one `storage/` folder for files, and PostgreSQL for everything else. No paid cloud storage is used.

| What | Example | Where | Format |
|---|---|---|---|
| Users, medicines, groups, run history, file catalogue, audit log | Dolo 650 composition, "over 65" group | PostgreSQL | Database tables |
| User uploads | Pack inserts, lab results, papers, structure files | `storage/uploads/<organisation>/` | PDF, JPG/PNG, Excel, CSV, MOL/SDF |
| Copies of fetched sources | DailyMed label, PubMed abstract | `storage/sources/` | PDF, XML, text |
| Virtual population | The 100,000 virtual people | `storage/populations/` | Parquet |
| Simulation results | Drug levels for every person in a run | `storage/results/<organisation>/<run>/` | Parquet |
| Generated reports | Group risk report | `storage/reports/<organisation>/` | PDF, Excel |
| App logs | Errors and background activity | `storage/logs/` | Text |
| Code | Python, React, settings | GitHub (Appbay-AI) | Code |
| Secret settings | Database password | `.env` on the server only | Text, never shared |

Rules:

- Files are saved under random names; the original name, uploader, date, organisation and link to a medicine or run are stored in PostgreSQL.
- Users can only open files from their own organisation, and files are only served through the app after login.
- Uploads allow only PDF, images, Excel, CSV and chemical structure files, up to 20 MB each, and are virus-scanned (ClamAV, free) before saving. The upload screen warns not to upload real patient records.
- Nothing in `storage/` goes into Git.
- The database and `storage/` folder are backed up together every night. Uploads, sources, reports and the database cannot be recreated, so they matter most. Populations and results can be rebuilt from code and the fixed seed.
- The storage layer is swappable, so it can move to MinIO (free) or cloud storage later without changing the rest of the app.

---

## 6. Rules the build must follow

1. **Research use only** label on every screen, report and export.
2. **No real patient data.** Public survey data or synthetic data only.
3. **Every number has a source**, or is clearly marked *"estimate — not sourced"*.
4. **No guessed numbers.** All results come from tested, deterministic code.
5. **Reproducible.** Fixed random seed; same inputs give the same outputs.
6. **Free sources only**, unless a licence is confirmed.
7. **Never assume safety.** Missing interaction data is labelled *"not modelled — needs review"*.
8. **Secrets** (passwords, API keys) live in a `.env` file that is never committed.
9. **Tests for every calculation**, with the core model validated against a known analytical solution.
10. **No paid APIs.** The app runs without any paid service or API key (section 4.6).
11. **Every module includes its screen**, so progress can be seen and demonstrated.

---

## 7. How we build it: modules and tasks

Version 1 is built in **10 modules**. Each module is built **end to end**: the engine or data part **and the screen that shows it**. So every module ends with something that can be seen, tested and shown to the client.

Each module is split into numbered **tasks** (for example **M3-T2**). One task is one piece of work that Claude Code plans, builds, tests and explains before moving to the next.

### 7.1 Working rhythm

**For every module**

1. Start a **fresh Claude Code conversation** for the module.
2. Paste the module's prompt from `docs/PROMPTS.md`. Claude Code reads `CLAUDE.md` and this spec.
3. Work through the module's tasks **in order**.

**For every task**

1. **Plan:** in Plan mode, Claude Code proposes how it will do the task. You read it and approve.
2. **Build and test:** Claude Code builds the task, runs the tests and shows the output.
3. **Explain:** Claude Code explains in plain English what was built and what the output means.
4. **Check:** you compare the result with the task's *Done when*.
5. **Commit and push:** you say *"commit this"*. Claude Code saves the work to Git with the task number in the message (for example `M3-T2: kidney and liver adjustments`). You then push to `main`.

**At the end of every module**

- Claude Code runs **all** tests again and starts the app so you can click through the module's screen.
- You check the module's **Module done when**, then mark the module Done in the build plan.
- If the module has a **client demo**, you rehearse it once before showing the client.

### 7.2 Module overview and timeline

The plan assumes **one developer** working with Claude Code, building the modules **one after another** (no overlap) and pushing directly to the `main` branch after each approved task. Dates are working days (Monday to Friday); public holidays are not counted, so add days for Diwali, Christmas and any other leave.

| Module | Name | Screen you can see at the end | Days | Timeline | Client demo |
|---|---|---|---|---|---|
| **M1** | Foundation | App opens with menu and "Research use only" banner | 4 | 13 Oct – 16 Oct 2026 | — |
| **M2** | Medicine Library | Medicine search, composition with sources, edit ingredients | 6 | 19 Oct – 26 Oct 2026 | Optional preview |
| **M3** | Simulation Engine & Digital Twin | Person profile form and drug-level chart | 8 | 27 Oct – 5 Nov 2026 | **Demo 1** (~6 Nov) |
| **M4** | Population Groups & Group Testing | Group selection, Run, results per group, run history | 11 | 6 Nov – 20 Nov 2026 | **Demo 2, core demo** (~23 Nov) |
| **M5** | Safety, Side Effects & Uncertainty | Risk flags, side effects, groups most at risk | 9 | 23 Nov – 3 Dec 2026 | **Demo 3** (~4 Dec) |
| **M6** | Search Any Medicine & Review | Live search, preparation status, reviewer approval | 7 | 4 Dec – 14 Dec 2026 | **Demo 4** (~15 Dec) |
| **M7** | Users, Organisations & File Uploads | Login, Users page, uploads | 5 | 15 Dec – 21 Dec 2026 | — |
| **M8** | Reports & Run Comparison | Download report, compare runs | 4 | 22 Dec – 25 Dec 2026 | **Demo 5, full product** (~28 Dec) |
| **M9** | New Medicines | "Create new medicine" screen with reliability labels | 4 | 28 Dec – 31 Dec 2026 | — |
| **M10** | Go Live & Pilot | The app on a live web link | 8 | 1 Jan – 12 Jan 2027 | **Final demo, live** (~13 Jan) |

Total: about 66 working days.

- **Buffer** for delays, fixes and holidays: 13 Jan – 19 Jan 2027
- **Target launch:** about 19 January 2027

**Order of work**

- The modules are built strictly in order, M1 to M10.
- M3 is first built and tested with test values, then connected to the medicine library from M2.
- M6 comes after M4 and M5, so Demo 2 shows searching only the medicines already in the library. Searching a never-added medicine is shown in Demo 4.
- M10 needs all other modules finished.

**How code is saved**

- One developer, one branch: work goes directly to `main`. There are no branches to merge.
- After you approve a task, Claude Code commits it with the task number in the message, and you push it to GitHub (Appbay-AI). Because everything goes straight to `main`, only push work whose tests pass, and push at least once at the end of every working day as a backup.

**What could move the dates**

- Review time: every plan and result still has to be read and approved by a person.
- Pharmacology reviewer: needed for M2 (by about 23 Oct) and again in M5.
- NFHS-5 data access: if approval is late, M4 starts with NHANES data and adds Indian data later.
- Claude usage limits: heavy days may need a pause.
- Holidays and leave: not counted in the dates above.
- With a single developer, one blocked module delays every module after it. The buffer absorbs about one week; after that the launch moves into February.

---

### M1 — Foundation (13 Oct – 16 Oct)

**Goal:** a working project skeleton with an empty app the client could open.

| Task | What gets done | Done when |
|---|---|---|
| **M1-T1** | Setup check: Claude Code reads `CLAUDE.md` and this spec; checks Python, Git, uv, Node.js and PostgreSQL; installs uv if missing (after asking) | Claude Code summarises the project and rules correctly |
| **M1-T2** | Folder structure for the whole project (engine, server, screens, tests, storage, docs) | Structure explained in plain English and approved |
| **M1-T3** | Data formats (JSON schemas) for medicine, ingredient, parameter, population category and level, individual profile, run and group result | Formats explained with a Dolo 650 example and approved |
| **M1-T4** | File storage set up as in section 5.1 (`storage/` folders, kept out of Git) | Folders exist; `.gitignore` excludes them |
| **M1-T5** | PostgreSQL database created and connected; first database migration | Server connects to the database; a test confirms it |
| **M1-T6** | Python server started (FastAPI) with a health check | Opening the health check address in the browser shows "OK" |
| **M1-T7** | Screen shell (React): app name, menu for the future screens, "Research use only" banner, brand colours | The app opens in the browser with the menu and banner |

**Module done when:** the app opens in the browser, the server and database are connected, and all tests pass.

---

### M2 — Medicine Library (19 Oct – 26 Oct)

**Goal:** search a medicine and see its full composition, with a source behind every number.

| Task | What gets done | Done when |
|---|---|---|
| **M2-T1** | Database records for medicines, ingredients, compositions and parameters (each parameter with value, unit, source, quote, date, confidence, status) | Records created; tests pass |
| **M2-T2** | Add 3 test medicines, including Dolo 650, with real published values and sources; anything unsourced marked "estimate — not sourced" | Parameter table shown to you for review |
| **M2-T3** | Server functions: search medicines, get one medicine with its composition and sources | Tests pass for search and details |
| **M2-T4** | **Medicine screen:** search box, results list, medicine details (ingredients, strengths, dosage form, manufacturer, label dose), each value with its source link and Verified / Unverified label | You can search "Dolo" and see the composition with sources |
| **M2-T5** | Edit composition (add, delete, change ingredients and amounts); saving creates a new medicine **version** and keeps the original | Editing Dolo 650 creates "v2" and the original is unchanged |
| **M2-T6** | Reviewer check of the 3 test medicines; corrections applied | Reviewer has checked every value |

**Module done when:** you can search a medicine, see every value with its source, and edit it into a new version.
**Optional client preview:** show Dolo 650 with a source link on every value.

---

### M3 — Simulation Engine & Digital Twin (27 Oct – 5 Nov)

**Goal:** predict a medicine's blood level over time for one person.

| Task | What gets done | Done when |
|---|---|---|
| **M3-T1** | Blood-level model (one-compartment, first-order absorption) | Tests match the known analytical (textbook) solution |
| **M3-T2** | Repeated dosing (for example twice daily for 5 days) | Tests show levels building up to a steady pattern as expected |
| **M3-T3** | Person-level adjustments: body weight, age, kidney function, liver function, each from a published relationship with its source | A test shows lower kidney function raises levels for a kidney-cleared medicine |
| **M3-T4** | Metaboliser genotype adjustment (from CPIC) where the medicine has published data | Test shows a poor metaboliser gets higher levels where expected |
| **M3-T5** | Server function: run a simulation for one person and one medicine | Returns drug levels over time; tests pass |
| **M3-T6** | **Individual profile screen:** form for age, sex, weight, height, kidney and liver function, genotype, smoking | Form saves a profile with checks on realistic ranges |
| **M3-T7** | **Drug-level chart:** curve over time with peak level and time to peak; effective and toxic levels drawn as reference lines where sourced | Changing kidney function visibly changes the curve |

**Module done when:** you can enter a person, choose a medicine and see their drug-level chart.
**Client Demo 1 (~6 Nov):** show Dolo 650 in the medicine library with its sources, enter one person, show their drug-level curve, then lower kidney function and watch the curve rise.

---

### M4 — Population Groups & Group Testing (6 Nov – 20 Nov)

**Goal:** test a medicine across many groups of virtual people at once.

| Task | What gets done | Done when |
|---|---|---|
| **M4-T1** | Population categories and levels (age band, sex, weight, kidney, liver, smoking, alcohol, fitness, pregnancy, genotype, diabetes) | Categories stored; admins can add or edit later |
| **M4-T2** | Load public survey data (NHANES; NFHS-5 when access is approved) | Data loaded; sources recorded |
| **M4-T3** | Generate one large virtual population (for example 100,000 people) with a fixed seed, keeping traits realistically linked | Running twice gives identical people; group sizes look realistic |
| **M4-T4** | Run a medicine through the whole population (stored as Parquet) | A full run finishes and results are saved |
| **M4-T5** | Group results for every single group, pair and trio; groups below the minimum size flagged and excluded | Group counts add up; flagged groups shown as "too few people" |
| **M4-T6** | Run history: every run saved with its full inputs (medicine version, amounts, groups, population version, data version); old runs never change | A second run with changed amounts and groups keeps the first run intact |
| **M4-T7** | **Population groups screen:** choose groups and combination depth; shows how many virtual people each group has | You can pick groups and see their sizes |
| **M4-T8** | **Run and results screen:** Run button, progress, results per group (drug-level range, peak, time to peak), run history list | You can run Dolo 650 and browse results per group |

**Module done when:** you can pick a medicine and groups, click Run, and see results for every group and combination.
**Client Demo 2, core demo (~23 Nov):** run Dolo 650 across groups and show how responses differ between groups.

---

### M5 — Safety, Side Effects & Uncertainty (23 Nov – 3 Dec)

**Goal:** show which groups are at risk, what side effects to expect, and how certain each result is.

| Task | What gets done | Done when |
|---|---|---|
| **M5-T1** | Effective and toxic levels per medicine, with sources | Values stored with sources and reviewed |
| **M5-T2** | Risk flags per group (on target / check dose / risk) and share of people above toxic or below effective level | Flags follow the numbers in tests |
| **M5-T3** | Interaction check between ingredients; unknown pairs labelled "not modelled — needs review" | Unknown pairs never shown as safe |
| **M5-T4** | Side effects by body system from label data, with published frequencies | Side effects shown grouped by body system with sources |
| **M5-T5** | Uncertainty analysis (which inputs drive uncertainty) | Results explained with a ranked list of drivers |
| **M5-T6** | Ranking of groups most at risk and least likely to benefit; list of real-world tests that would reduce uncertainty most | Rankings come from the numbers, not fixed text |
| **M5-T7** | **Full results screen:** risk flags, side effects by body system, interactions, uncertainty, rankings, data completeness labels | All of the above visible for a test medicine |

**Module done when:** the results screen shows risk, side effects, interactions and uncertainty for every group.
**Client Demo 3 (~4 Dec):** show which groups are most at risk with Dolo 650, and why.

---

### M6 — Search Any Medicine & Review (4 Dec – 14 Dec)

**Goal:** any medicine can be searched, prepared and reviewed, with no paid API.

| Task | What gets done | Done when |
|---|---|---|
| **M6-T1** | Free label fetch from DailyMed and openFDA (composition, dose, side effects, warnings, interactions) | A medicine not in the library shows its label data instantly |
| **M6-T2** | PubMed paper list for the medicine (free) | Relevant papers listed with links |
| **M6-T3** | Copies of fetched source documents saved in `storage/sources/` | Source copies saved and linked to the medicine |
| **M6-T4** | "Data preparation" queue; screen status "Simulation data being prepared" | New medicines appear in the queue |
| **M6-T5** | `prepare-medicine` command, run with Claude Code: extracts simulation values with quotes and source links and saves them as Unverified; extraction step built to be swappable (free local model later) | One new medicine prepared end to end with no paid API |
| **M6-T6** | Reviewer approval: reviewer checks values and marks the medicine Verified; scheduled re-check of sources | Medicine moves from Unverified to Verified |
| **M6-T7** | **Search and review screens:** live search for any medicine, preparation status, reviewer approval page | A brand-new medicine is searched, prepared, simulated and approved |

**Module done when:** a medicine never seen before can be searched, prepared, simulated and approved.
**Client Demo 4 (~15 Dec):** search a medicine that was never added, show label data instantly and the Verified / Unverified labels.

---

### M7 — Users, Organisations & File Uploads (15 Dec – 21 Dec)

**Goal:** secure multi-user access, as described in section 2.7, and file uploads.

| Task | What gets done | Done when |
|---|---|---|
| **M7-T1** | Organisations and users with roles (researcher, reviewer, admin); passwords stored only as secure hashes | Records created; tests pass |
| **M7-T2** | One-time `create-admin` command for the first admin | You create the first admin from the terminal |
| **M7-T3** | **Login page** with session timeout and short lock after repeated failed logins | You can log in and out |
| **M7-T4** | **Users page:** admin adds users, gets a temporary password, resets passwords, deactivates users | A test user is created with a temporary password |
| **M7-T5** | Forced password change on first login; temporary passwords expire | The test user must set a new password |
| **M7-T6** | Organisation privacy: users see only their organisation's medicines, runs, files and reports | A user from organisation A cannot see organisation B's data |
| **M7-T7** | **File uploads** (pack inserts, lab results, papers, structure files) with type and size limits, virus scan, stored as in section 5.1 | Upload works; wrong file types are rejected |
| **M7-T8** | Audit log of logins, user changes, uploads and approvals | Log shows who did what and when |

**Module done when:** users log in with roles, see only their organisation's data, and can upload files.

---

### M8 — Reports & Run Comparison (22 Dec – 25 Dec)

**Goal:** share results and compare tests.

| Task | What gets done | Done when |
|---|---|---|
| **M8-T1** | **Run comparison screen:** two or more runs side by side, changed inputs highlighted, differences in levels, flags and rankings | Comparing two runs shows what changed |
| **M8-T2** | "Re-run with latest data" when drug data has been updated or verified since an old run | Creates a new run; the old run is unchanged |
| **M8-T3** | PDF report (from an HTML report page) with the research-use label | PDF downloads and matches the screen |
| **M8-T4** | Excel export of results | Excel file opens with results per group |

**Module done when:** a researcher can compare runs and download PDF and Excel reports.
**Client Demo 5, full product (~28 Dec):** log in, run a test, compare two runs and download a PDF report.

---

### M9 — New Medicines (28 Dec – 31 Dec)

**Goal:** test medicines that are not on the market yet (section 2.4).

| Task | What gets done | Done when |
|---|---|---|
| **M9-T1** | **"Create new medicine" screen:** name, compounds, amounts or mixing percentages, dose and frequency | A new medicine can be created and saved |
| **M9-T2** | New mix of known ingredients: each simulated from its published data; missing interaction data flagged | Results shown with the right labels |
| **M9-T3** | Brand-new compound with lab-measured values (solubility, permeability, protein binding, clearance) | Results labelled "Predicted from lab data" |
| **M9-T4** | Structure-only estimate (RDKit and similar free tools) with wide uncertainty and a list of lab tests that would improve it | Results labelled "Exploratory estimate" |

**Module done when:** each of the three cases runs and shows the correct reliability label.

---

### M10 — Go Live & Pilot (1 Jan – 12 Jan)

**Goal:** the app running on a secure web link, tested by real users.

| Task | What gets done | Done when |
|---|---|---|
| **M10-T1** | Package the app with Docker Compose | The whole app starts with one command |
| **M10-T2** | Set up the Ubuntu server and Caddy for a secure web address (HTTPS) | The app opens on the web address with a padlock |
| **M10-T3** | Nightly backups of the database and `storage/` folder, and a tested restore | A backup is restored successfully on a test copy |
| **M10-T4** | Full end-to-end test of every module on the live server | All tests pass on the server |
| **M10-T5** | Pilot with the reviewer and 1 to 2 researchers (ideally from the client) | Pilot users complete a full test and give feedback |
| **M10-T6** | Fix pilot findings; final check of research-use labels and data labels | All critical findings fixed |

**Module done when:** pilot users have used the live app successfully and critical issues are fixed.
**Final client demo (~13 Jan):** the client's own researchers use the live link.

### 7.3 Client demo rules

- Demos before M10 run on your laptop over screen share.
- Prepare the medicines and runs before the demo, so nothing waits on data preparation.
- Keep the "Research use only" banner visible and say which data is Unverified.
- Show only finished modules. New ideas from the client go on the Version 2 list, not into the current module.

### 7.4 Versions

| Version | Delivers | Gate before the next version |
|---|---|---|
| **1** | Modules M1–M10 | Engine validated; reviewed medicines give correct results; all tests pass; pilot complete |
| **2** | Organ-level concentrations (PK-Sim) for well-studied drugs; recalibration with measured blood levels; optional free local AI model (Ollama) for automatic data preparation; email invites and self-service password reset | Organ results match published examples |
| **3** | Improved support for brand-new compounds (more lab input types, better structure-based estimates) | — |

---

## 8. Feasibility summary

| Requirement | Verdict | How the app handles it |
|---|---|---|
| Search any medicine and see its composition | Feasible with limits | US medicines fetched from DailyMed; Indian brands entered once from the pack insert |
| Edit composition | Feasible with limits | Any edit allowed; ingredients without published data marked *not modelled* |
| New mix of known ingredients | Feasible with limits | Each ingredient simulated; pairs without interaction data flagged |
| Brand-new compound | Not feasible as asked (without lab data) | Requires lab inputs; otherwise *exploratory estimate* with wide uncertainty |
| Individual digital twin | Feasible | Published adjustments applied to the person's own values |
| Prebuilt population groups | Feasible | One large virtual population from survey data, sliced into groups |
| Every combination and permutation of groups | Feasible with limits | Singles, pairs and trios by default; deeper on request; small groups flagged |
| Drug levels over time with uncertainty | Feasible | Core engine, validated |
| Organ-level concentrations | Feasible with limits | Version 2, for well-studied drugs |
| Interaction checks | Feasible with limits | Every pair checked; missing data never treated as safe |
| "All effects on all body parts" | Not feasible as asked | Blood (and later organ) levels, plus label side effects by body system and toxic-level comparisons |
| Fetch published data live | Feasible with limits | Label information fetched instantly for free; simulation numbers prepared once per medicine with Claude Code (no paid API); saved; *Unverified* until reviewed |

---

## 9. Risks

| Risk | Effect | Mitigation |
|---|---|---|
| Wrong or invented citations from AI extraction | Results look sourced but are not | Every value stores a quoted excerpt; reviewer checks before *Verified* |
| Use on real patients | May be regulated as a medical device | Research-only labels; no real patient data; regulatory advice before any clinical use |
| Thin published data for some medicines | Wide uncertainty or missing results | *Partial data* label listing exactly what is missing |
| Too many group combinations | Noisy results from tiny groups | Default depth of three; minimum group size enforced |
| Established competitors | Pharma already uses commercial tools | Position for institutes, CROs and smaller pharma; affordable and easy |
| Indian brand coverage | No machine-readable Indian source | One-time manual entry from pack inserts, reviewed |

---

## 10. Out of scope for version 1

- Connection to real patient records or hospital systems
- Clinical or prescribing use
- Regulatory submissions
- Organ-level modelling (version 2)
- Mobile apps
