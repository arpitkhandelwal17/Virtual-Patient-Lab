# server — the web server

Connects the calculator to the database, the screens and the free data sources.

**Belongs here:** API, database records, medicine search, fetching from DailyMed/openFDA/PubMed, saved source copies, data-preparation queue, login and roles, reports, commands (`prepare-medicine`, `create-admin`).

**Does not belong here:** drug-level maths (that is in `engine/`) and screen code (that is in `screens/`).

Tests are in `tests/server/`.
