# Virtual Patient Lab — Feature List

Derived from `docs/SPEC.md` (v2.0). The spec is the source of truth; if they differ, the spec wins.
**Research use only — not for clinical decisions.**

Legend: **V1** = built in Version 1 (modules M1–M10) · **V2 / V3** = later versions · Module/task IDs point to the build plan in SPEC section 7.

---

## 1. Medicine search and library (M2, M6)

| # | Feature | Module | Ver |
|---|---|---|---|
| 1.1 | Search any medicine by brand or generic name (no fixed list) | M2-T4, M6-T7 | V1 |
| 1.2 | Medicine details: active and inactive ingredients, strengths, dosage form, manufacturer, label dose | M2-T4 | V1 |
| 1.3 | Pharmacology values per active ingredient, each with source link and Verified / Unverified label | M2-T4 | V1 |
| 1.4 | Edit composition (add, delete, change ingredients and amounts); saving creates a new **version**, original kept | M2-T5 | V1 |
| 1.5 | Indian brands (e.g. Dolo 650) entered once from pack insert, then active-ingredient data fetched automatically | M2-T2 | V1 |
| 1.6 | Instant results for medicines already in the library | M2-T3 | V1 |

## 2. Live data fetch and data preparation — no paid API (M6)

| # | Feature | Module | Ver |
|---|---|---|---|
| 2.1 | Instant free label fetch from DailyMed and openFDA (composition, dose, side effects, warnings, interactions) | M6-T1 | V1 |
| 2.2 | PubMed paper list for the medicine, with links | M6-T2 | V1 |
| 2.3 | Saved copies of fetched source documents in `storage/sources/` | M6-T3 | V1 |
| 2.4 | "Data preparation" queue and status "Simulation data being prepared" | M6-T4 | V1 |
| 2.5 | `prepare-medicine` command (run via Claude Code): extracts simulation values with quoted excerpts and source links, saves as Unverified | M6-T5 | V1 |
| 2.6 | Pluggable extraction step so a free local model (Ollama) can be added later | M6-T5 | V1 (hook) / V2 (Ollama) |
| 2.7 | Reviewer approval: mark a medicine Verified; scheduled re-check of sources | M6-T6 | V1 |
| 2.8 | Later searches reuse the saved copy (fast, repeatable) | M6 | V1 |

## 3. Data trust and labelling (cross-cutting)

| # | Feature | Ver |
|---|---|---|
| 3.1 | Every parameter stores: value and unit, source URL, quoted excerpt, retrieval date, confidence, status, reviewed by/when | V1 |
| 3.2 | Unsourced values stored as "estimate — not sourced", never shown as verified | V1 |
| 3.3 | Completeness labels: **Verified**, **Unverified**, **Partial data**, **Predicted from lab data**, **Exploratory estimate** | V1 |
| 3.4 | Missing interaction data labelled "not modelled — needs review" (never treated as safe) | V1 |
| 3.5 | "Research use only — not for clinical decisions" on every screen, report and export | V1 |

## 4. Simulation engine and digital twin (M3)

| # | Feature | Module | Ver |
|---|---|---|---|
| 4.1 | One-compartment blood-level model with first-order absorption, validated against the analytical solution | M3-T1 | V1 |
| 4.2 | Repeated dosing (e.g. twice daily for 5 days) | M3-T2 | V1 |
| 4.3 | Person adjustments: weight, age, kidney function (eGFR), liver function — each from a sourced relationship | M3-T3 | V1 |
| 4.4 | Metaboliser genotype adjustment (CPIC) where published data exists | M3-T4 | V1 |
| 4.5 | Single-person simulation (digital twin): most-likely curve plus uncertainty range | M3-T5 | V1 |
| 4.6 | Individual profile form (age, sex, weight, height, kidney, liver, genotype, smoking) with realistic-range checks | M3-T6 | V1 |
| 4.7 | Drug-level chart with peak level, time to peak, effective and toxic reference lines (where sourced) | M3-T7 | V1 |
| 4.8 | "What missing information would narrow the range most" (e.g. a recent kidney test) | M5-T6 | V1 |
| 4.9 | Two-compartment model where published data supports it | — | V1 where data allows |
| 4.10 | Recalibrate the twin with measured blood levels (Bayesian update, PyMC) | — | V2 |

## 5. Population groups and group testing (M4)

| # | Feature | Module | Ver |
|---|---|---|---|
| 5.1 | Prebuilt categories and levels: age band, sex, weight, kidney, liver, smoking, alcohol, fitness, pregnancy, genotype, diabetes | M4-T1 | V1 |
| 5.2 | Admins can add or edit categories and levels | M4-T1 | V1 |
| 5.3 | Public survey data loaded (NHANES; NFHS-5 when access approved), sources recorded | M4-T2 | V1 |
| 5.4 | One large virtual population (~100,000) with realistically linked traits and a fixed seed | M4-T3 | V1 |
| 5.5 | Run a medicine through the whole population (results stored as Parquet) | M4-T4 | V1 |
| 5.6 | Results for every single group, pair and trio; deeper combinations on request | M4-T5 | V1 |
| 5.7 | Groups with too few people flagged and excluded ("too few people") | M4-T5 | V1 |
| 5.8 | Population groups screen: pick groups and combination depth, see group sizes, optionally add one individual profile | M4-T7 | V1 |
| 5.9 | Run and results screen: Run button, progress, per-group drug-level range, peak, time to peak | M4-T8 | V1 |
| 5.10 | Run history list | M4-T6, M4-T8 | V1 |

## 6. Safety, side effects and uncertainty (M5)

| # | Feature | Module | Ver |
|---|---|---|---|
| 6.1 | Sourced effective and toxic levels per medicine | M5-T1 | V1 |
| 6.2 | Risk flag per group (on target / check dose / risk) and share of people above toxic / below effective level | M5-T2 | V1 |
| 6.3 | Interaction check of every pair of active ingredients | M5-T3 | V1 |
| 6.4 | Side effects by body system from label data with published frequencies; openFDA adverse events shown only as signals | M5-T4 | V1 |
| 6.5 | Uncertainty analysis (Sobol sensitivity): ranked list of what drives uncertainty | M5-T5 | V1 |
| 6.6 | Ranking of groups most at risk and least likely to benefit | M5-T6 | V1 |
| 6.7 | Ranked list of real-world tests that would reduce uncertainty most | M5-T6 | V1 |
| 6.8 | Full results screen combining all of the above plus data-completeness labels | M5-T7 | V1 |

## 7. Runs, versions and comparison (M4, M8)

| # | Feature | Module | Ver |
|---|---|---|---|
| 7.1 | Every test saved as a separate run; earlier runs never overwritten | M4-T6 | V1 |
| 7.2 | Each run records: who, when, medicine version and amounts, groups and depth, population version, drug-data version, software version | M4-T6 | V1 |
| 7.3 | Changing groups re-slices the same virtual population (same seed) | M4 | V1 |
| 7.4 | Side-by-side run comparison with changed inputs highlighted and differences in levels, flags, rankings | M8-T1 | V1 |
| 7.5 | "Re-run with latest data" notice and action (creates a new run) | M8-T2 | V1 |

## 8. Reports and export (M8)

| # | Feature | Module | Ver |
|---|---|---|---|
| 8.1 | PDF report (from HTML report page) with research-use label | M8-T3 | V1 |
| 8.2 | Excel export of results per group | M8-T4 | V1 |
| 8.3 | Comparison included in the report | M8 | V1 |

## 9. Creating new medicines (M9)

| # | Feature | Module | Ver |
|---|---|---|---|
| 9.1 | "Create new medicine" screen: name, compounds, amounts or mixing percentages, dose, frequency | M9-T1 | V1 |
| 9.2 | New mix of known ingredients: each simulated from published data; missing interactions flagged | M9-T2 | V1 |
| 9.3 | Brand-new compound with lab values (solubility, permeability, protein binding, clearance) → "Predicted from lab data" | M9-T3 | V1 |
| 9.4 | Structure-only estimate (RDKit) → "Exploratory estimate", wide uncertainty, list of lab tests that would improve it | M9-T4 | V1 |
| 9.5 | Improved support for new compounds (more lab inputs, better structure estimates) | — | V3 |

## 10. Users, organisations, security and files (M7)

| # | Feature | Module | Ver |
|---|---|---|---|
| 10.1 | Organisation workspaces; users see only their own organisation's medicines, runs, files, reports | M7-T1, M7-T6 | V1 |
| 10.2 | Roles: Researcher, Reviewer, Admin | M7-T1 | V1 |
| 10.3 | One-time `create-admin` command for the first admin | M7-T2 | V1 |
| 10.4 | Login page, session timeout, short lockout after repeated failures | M7-T3 | V1 |
| 10.5 | Users page: add users, temporary password shown once, reset passwords, deactivate | M7-T4 | V1 |
| 10.6 | Forced password change on first login; temporary passwords expire (~7 days) | M7-T5 | V1 |
| 10.7 | Passwords stored only as Argon2/bcrypt hashes; minimum 10 characters | M7-T1 | V1 |
| 10.8 | File uploads (pack inserts, lab results, papers, structure files): PDF, images, Excel, CSV, MOL/SDF; 20 MB limit; ClamAV virus scan; warning not to upload patient records | M7-T7 | V1 |
| 10.9 | Audit log of logins, user changes, uploads, Verified approvals | M7-T8 | V1 |
| 10.10 | Email invite links, self-service forgot-password, Google/Microsoft sign-in, two-step verification | — | Later |

## 11. Foundation and deployment (M1, M10)

| # | Feature | Module | Ver |
|---|---|---|---|
| 11.1 | Project skeleton and folder structure; JSON data formats | M1-T2, M1-T3 | V1 |
| 11.2 | `storage/` folders kept out of Git | M1-T4 | V1 |
| 11.3 | PostgreSQL with migrations; FastAPI server with health check | M1-T5, M1-T6 | V1 |
| 11.4 | Screen shell with menu, "Research use only" banner, brand colours | M1-T7 | V1 |
| 11.5 | Docker Compose packaging (one-command start) | M10-T1 | V1 |
| 11.6 | Ubuntu server with Caddy HTTPS | M10-T2 | V1 |
| 11.7 | Nightly backups of database and `storage/`, with tested restore | M10-T3 | V1 |
| 11.8 | End-to-end test on live server; pilot with reviewer and 1–2 researchers; fix findings | M10-T4–T6 | V1 |
| 11.9 | Swappable storage layer (MinIO or cloud later) | — | Later |

## 12. Planned for later versions

| Version | Feature |
|---|---|
| **V2** | Organ-level concentrations (PK-Sim) for well-studied drugs |
| **V2** | Recalibration with measured blood levels |
| **V2** | Optional free local AI (Ollama) for automatic data preparation |
| **V2** | Email invites and self-service password reset |
| **V3** | Better support for brand-new compounds |

## 13. Out of scope for Version 1

- Connection to real patient records or hospital systems
- Clinical or prescribing use
- Regulatory submissions
- Organ-level modelling (V2)
- Mobile apps
- Paid sources (full DrugBank, Simcyp, GastroPlus) and any paid API
