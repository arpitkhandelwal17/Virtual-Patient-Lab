# Data formats — draft v0.1

Research use only — not for clinical decisions.

This is the plain-English description of what we store. It is a draft: formats can be refined in later modules. No database exists yet; the database tables (M1-T5, M2-T1) will be built to match this.

**About the examples:** they use Dolo 650 (paracetamol 650 mg, as stated in the spec). Wherever a real drug value, side effect or manufacturer would go, the example shows `<placeholder>`. Real, sourced values are added in M2-T2. No value below is real.

Marks: **Required** = must be filled; *Optional* = may be empty.

---

## 1. Medicine
One product (a brand or a mix). Editing the recipe creates a new version; the old one never changes.

| Box | What goes in it | |
|---|---|---|
| name | Brand or generic name | Required |
| version | 1, 2, 3 … | Required |
| previous version | Which version this was edited from | *Optional* |
| dosage form | Tablet, capsule, syrup … | Required |
| manufacturer | Company | *Optional* |
| label dose | Dose and how often, from the label | *Optional* |
| data label | Verified / Unverified / Partial data / Predicted from lab data / Exploratory estimate | Required |
| ingredients | List of Ingredient records (format 2) | Required |

**Example:** name `Dolo 650` · version `1` · dosage form `<from pack insert>` · manufacturer `<from pack insert>` · data label `Unverified`.

## 2. Ingredient
One compound inside a medicine.

| Box | What goes in it | |
|---|---|---|
| compound name | For example paracetamol | Required |
| strength | Amount and unit | Required |
| role | Active or inactive | Required |
| parameters | List of Parameter records (format 3) | Required for active ingredients (may be empty at first) |

**Example:** compound `paracetamol` · strength `650 mg` · role `active`.

## 3. Parameter
One drug value, such as absorption speed, clearance, or an effective or toxic level. This is where "every number has a source" is enforced.

| Box | What goes in it | |
|---|---|---|
| name | What the value is | Required |
| value | The number | Required |
| unit | Its unit | Required |
| source link | Web address (DailyMed, PubMed, regulator…) | Required unless status is "estimate — not sourced" |
| quoted excerpt | The exact sentence or table cell it came from | Required unless status is "estimate — not sourced" |
| date retrieved | When it was fetched | Required unless status is "estimate — not sourced" |
| confidence | High / medium / low | Required |
| status | Verified / Unverified / estimate — not sourced | Required |
| reviewed by, reviewed on | Filled only when a reviewer approves | *Optional* |

Rules the format enforces:
- A value with no source can only have status "estimate — not sourced".
- "Verified" needs a source, a quote, and a reviewer name and date.

**Example:** name `clearance` · value `<placeholder>` · status `estimate — not sourced`.

## 4. Side effect
One label-listed adverse reaction. Fixed facts, stored once and reused.

| Box | What goes in it | |
|---|---|---|
| medicine, ingredient | Which medicine and active ingredient it belongs to | Required |
| effect | In plain words | Required |
| body system | Digestive, liver, kidney, skin … | Required |
| frequency | Published frequency, if the label gives one | *Optional* |
| kind | "Label-listed" or "Report signal only" (openFDA reports are never shown as rates) | Required |
| source link, quoted excerpt, date retrieved, confidence, status | Same rules as a Parameter | As Parameter |

**Example:** effect `<from label>` · body system `<from label>` · kind `Label-listed` · status `Unverified`.

## 5. Interaction
One pair of ingredients.

| Box | What goes in it | |
|---|---|---|
| ingredient A, ingredient B | The pair | Required |
| result | Published interaction text, or **"not modelled — needs review"** | Required |
| source link, quoted excerpt, date retrieved, confidence, status | Same rules as a Parameter | As Parameter |

Rule: a pair with no published data is stored as "not modelled — needs review", never as safe.

## 6. Population category and level
A group type and its levels.

| Box | What goes in it | |
|---|---|---|
| category | Age band, sex, body weight, kidney function, liver function, smoking, alcohol, fitness, pregnancy, genotype, diabetes | Required |
| levels | Each level has a name and a rule (for example a range), plus its source | Required |

Admins can add or edit these later (M4).

## 7. Individual profile (digital twin)
One person.

| Box | What goes in it | |
|---|---|---|
| age, sex, weight, height | Basic details, checked against realistic ranges | Required |
| kidney function, liver function | Test values if known | *Optional* |
| genotype | Metaboliser type if known | *Optional* |
| smoking | Yes / no | *Optional* |

No name, no identifiers: this is never a real patient record.

## 8. Run
One saved test. Never changed after saving.

| Box | What goes in it | |
|---|---|---|
| who ran it, when | User and time | Required |
| medicine and version, amounts | Exactly what was tested | Required |
| groups, combination depth | What was selected | Required |
| population version, random seed | So the same people are produced again | Required |
| drug-data version, software version | So the run can be reproduced | Required |
| individual profile | If a digital twin was included | *Optional* |

## 9. Group result
The result for one group (or combination of groups) in one run.

| Box | What goes in it | |
|---|---|---|
| run, group | Which run and which group | Required |
| group size | Number of virtual people | Required |
| too few people | Yes / no: if yes, results are not reported | Required |
| drug-level range, peak, time to peak | Calculated by the engine | Required unless too few people |
| share above toxic, share below effective | Calculated by the engine | Added in M5 |
| risk flag | On target / check dose / risk | Added in M5 |
| uncertainty drivers | Ranked list | Added in M5 |

The detailed curve for every virtual person is not stored here. It goes into result files (Parquet) linked to the run.
