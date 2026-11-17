# Milestone evidence

## M1 — Analytics foundation
PR #10 merged. Thirteen local Python tests passed; GitHub Actions also passed. The deterministic exporter created 5,218 dates × 6 asset models = 31,308 SQLite price records. CSV SHA-256: dd92fef8090223d33aa030c5dd03cd4f18e330da04c89eea881b8b2988ed9223.

## M2 — Interactive dashboard
PR #11 merged after both CI workflows passed. Three JavaScript tests passed, including full metric agreement with Python reference outputs at absolute tolerance 1e-8. Six local Playwright tests passed. After the responsive SVG adjustment, the affected viewport check passed again. Production Vite build succeeded. Screenshots reviewed at desktop and phone sizes; overflow checks cover 1440, 1024, 768, 390 and 320 pixels.

The first browser run exposed an exact-label selector issue in the asset filter. Explicit select labels fixed it. The Taste design checker did not run because it could not reserve a local server port; no Taste gate pass is claimed.

## M3 — Deployment
Pages source is GitHub Actions. [Deployment run 44028291382](https://github.com/jabrielabdillle/financial-market-analytics/actions/runs/44028291382) passed checks and deployment for main commit `88b044c061fe996516b7b8e057801d422ca232d8`.

On 2026-11-17, verified the [public site](https://jabrielabdillle.github.io/financial-market-analytics/) in a browser: overview metrics and charts loaded, SQLite explorer displayed 31,308 matching records, and filtering to TECH returned 5,218 records. The synthetic-data notice was visible on both views.
