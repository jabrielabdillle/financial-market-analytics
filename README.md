# Financial Market Analytics

An interactive research dashboard for comparing growth, volatility, drawdowns, correlations and tail losses. Python prepares a reproducible dataset; JavaScript recomputes metrics for selected windows; SQLite runs inside the browser through WebAssembly.

**Public demo:** https://jabrielabdillle.github.io/financial-market-analytics/

The public dataset is **synthetic**: 31,308 prices across six fictional asset models and 5,218 weekday dates from 2006-01-02 through 2025-12-31. It does not represent actual ETF performance. The demo is an educational analytics tool, not an investment recommendation or predictive model.

## What you can do

- Compare all six assets over a chosen date range and risk-free-rate assumption.
- Inspect normalized growth, drawdown and 63-session rolling volatility.
- Compare CAGR, total return, volatility, Sharpe, VaR95 and expected shortfall.
- Inspect correlations and compounded calendar-year returns, including partial periods.
- Query the SQLite price table by asset and date, paginate results, and export filtered CSV.
- Download the database, price dataset and provenance metadata.

## Run locally

Python 3.12 and Node 22 are used in CI.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.lock
python -m src.export
python -m pytest -q
cd web
npm ci
npm run test:unit
npm run dev
```

Production build and browser checks:

```bash
cd web
npx playwright install --with-deps chromium
npm test
```

On macOS the browser configuration uses the installed Google Chrome application. On Linux it uses Playwright Chromium. `npm test` builds the production assets before opening the preview server.

## Data pipeline

`python -m src.export` generates the demo and exports these files into `web/public/data/`:

| File | Purpose |
| --- | --- |
| `prices.csv` | Wide daily price panel |
| `market.json` | Frontend data and Python reference metrics |
| `metrics.csv` | Full-window performance and risk metrics |
| `annual_returns.csv` | Compounded available returns by calendar year |
| `market.sqlite` | Price records, asset/date index, provenance table |
| `provenance.json` | Source, coverage, counts, assumptions and CSV SHA-256 |

Generated data is ignored by Git and rebuilt in CI. The simulation uses a fixed random seed and documented arbitrary stress periods. Price panels must be complete, finite, positive, sorted and unique; missing values are rejected rather than implicitly filled.

To analyze a dataset you are entitled to use, supply a wide CSV with a `date` column and explicit source metadata:

```bash
python -m src.export --prices adjusted_prices.csv \
  --source "Provider and retrieval date" \
  --adjustment "Describe split and dividend adjustment"
```

The original optional `src.download_data` module downloads ETF data through yfinance. Network access and the provider's terms/availability apply. It was not used for the public demo. PostgreSQL-compatible templates remain in `sql/`; the deployed application uses SQLite. No PostgreSQL server or Power BI report is deployed.

## Validation

- 13 Python regression tests cover initial-day loss, invalid/missing values, constant series, partial periods, tail metrics, SQL returns, export integrity and deterministic generation.
- 3 JavaScript tests cover analytic fixtures and agreement with Python metrics.
- 6 Playwright checks cover filters, invalid windows, chart controls, CSV/SQLite downloads, provenance and five viewport widths.

The CI workflow repeats these checks before publishing the application. The separate Taste design gate could not run its local server; see [design notes](docs/DESIGN.md) for that limitation.

## Architecture

```text
Seeded simulator OR supplied adjusted-price CSV
  → validated Pandas price panel
  → NumPy/Pandas metrics + provenance hash
  → JSON + CSV + indexed SQLite exports
  → Vite browser dashboard + sql.js queries
  → GitHub Actions checks → GitHub Pages
```

No paid hosting, external database account, API secret or persistent server is required. Visitor filters run locally. The SQLite database is a read-only research snapshot; exports create local copies.

## Documentation

- [Metric definitions and limitations](docs/METHODOLOGY.md)
- [Deployment and maintenance](docs/DEPLOYMENT.md)
- [Interview explanation](docs/INTERVIEW_GUIDE.md)
- [Milestone evidence](docs/VALIDATION.md)
- [Agent instructions](AGENTS.md) and [project memory](MEMORY.md)

Historical or simulated descriptive statistics do not establish future returns. This analysis excludes trading costs, taxes and investor-specific constraints. CAGR uses elapsed calendar days; volatility and Sharpe use the 252-session convention. Boundary years may be partial.
