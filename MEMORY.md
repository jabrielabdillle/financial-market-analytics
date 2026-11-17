# Project memory

Repository: https://github.com/jabrielabdillle/financial-market-analytics
User authorized free hosting, a mock database, implementation milestones, PRs and merging to main.

M1 merged in PR #10: strict daily-price validation, initial-price drawdown, calendar-day CAGR, sample volatility, configurable Sharpe, VaR/ES, compounded partial-period returns, deterministic six-asset dataset, JSON/CSV/SQLite exporter and provenance hash. Thirteen Python tests pass. Dataset: 5,218 dates and 31,308 synthetic prices. It is not observed ETF performance.

M2 implemented locally: Vite dashboard, window/asset/risk-free filters, growth/drawdown/rolling-volatility charts, correlation and annual return views, parameterized SQLite explorer and CSV/database exports. Production build, three JS metric tests and six Playwright checks pass. Taste gate could not reserve a server port; see docs/DESIGN.md. M2 awaits PR/CI/merge.

M3 remaining: verify Pages settings, deploy, check public site, update README and interview guide. Do not claim deployment is live yet. Local Git fails through missing macOS xcrun; commits use the connected GitHub API. Local source is not a Git checkout.
