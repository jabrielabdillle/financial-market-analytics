# Project memory

Repository: https://github.com/jabrielabdillle/financial-market-analytics
Live demo: https://jabrielabdillle.github.io/financial-market-analytics/
User authorized free hosting, mock data, milestone commits, PRs and merging to main.

M1 merged in PR #10: validated daily-price analytics, initial-price drawdown, calendar-day CAGR, configurable Sharpe, tail metrics, deterministic JSON/CSV/SQLite export and provenance. Thirteen Python tests pass.

M2 merged in PR #11: responsive Vite dashboard, filters, growth/drawdown/rolling volatility, correlations, calendar returns, parameterized browser SQLite queries and exports. Three JavaScript parity/fixture tests and six Playwright checks pass. Taste gate could not reserve a local server port; see docs/DESIGN.md. Do not claim it passed.

M3: GitHub Actions Pages deployment run 44028291382 succeeded for main commit 88b044c061fe996516b7b8e057801d422ca232d8. Live overview and SQLite explorer verified on 2026-11-17: 31,308 total records; TECH filter returns 5,218. README, deployment notes, validation evidence and interview guide complete in this documentation milestone.

Dataset contains six fictional asset models over 5,218 weekday dates. All prices and performance are synthetic, not observed ETF performance. No predictions, live feeds, PostgreSQL server or Power BI deployment are claimed.

Local Git fails through missing macOS xcrun; commits use the connected GitHub API. Local source is not a Git checkout. Future updates must start from current remote main, run relevant checks and use reviewed PRs. No paid infrastructure or secrets are required.
