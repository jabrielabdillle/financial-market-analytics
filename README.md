# Financial Market Analytics & Investment Trends

A reproducible analytics project that explores historical market performance, return patterns, volatility, drawdowns, and relationships across a diversified set of publicly traded ETFs.

> **Purpose:** Demonstrate an end-to-end analytics workflow using Python, SQL, PostgreSQL, and Power BI. This is an educational portfolio project, not investment advice.

## Business questions

1. How have selected asset classes performed over time?
2. Which assets have had the highest historical volatility?
3. What were the largest peak-to-trough drawdowns?
4. How have returns and correlations changed across market regimes?
5. How can these findings be communicated to a non-technical audience?

## Tools

- Python: `pandas`, `numpy`, `yfinance`, `matplotlib`
- SQL: PostgreSQL-compatible schema and analytical queries
- BI: Power BI (dashboard build guide included below)
- Git: version control and reproducibility

## Assets

The default universe uses liquid, widely followed ETFs as market proxies:

| Ticker | Proxy |
|---|---|
| SPY | US large-cap equities |
| QQQ | Nasdaq-100 equities |
| IWM | US small-cap equities |
| EFA | Developed international equities |
| AGG | US investment-grade bonds |
| GLD | Gold |

These are proxies, not complete representations of entire asset classes. Historical performance does not predict future results.

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/jabrielabdillle/financial-market-analytics.git
cd financial-market-analytics
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Download public market data

```bash
python -m src.download_data --start 2012-01-01
```

This downloads adjusted daily prices through the latest available date and saves:
- `data/raw/adjusted_prices.csv`
- `data/processed/daily_returns.csv`

The data provider may change its access policies, symbols, or availability. Review the provider's terms before use.

### 3. Run the analysis

```bash
python -m src.analyze
```

Outputs are written to `outputs/`:
- `asset_performance.csv`
- `annual_returns.csv`
- `monthly_returns.csv`
- `correlation_matrix.csv`
- `cumulative_growth.png`
- `drawdowns.png`
- `rolling_volatility.png`

### 4. Run tests

```bash
pytest
```

## Repository structure

```text
financial-market-analytics/
├── data/
│   ├── raw/
│   └── processed/
├── outputs/
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
├── src/
│   ├── __init__.py
│   ├── download_data.py
│   └── analyze.py
├── tests/
│   └── test_metrics.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Key metrics

- **Cumulative return:** total percentage change over the selected period.
- **Annualized return:** geometrically annualized growth rate.
- **Annualized volatility:** standard deviation of daily returns multiplied by the square root of 252.
- **Sharpe ratio:** annualized average excess daily return divided by annualized volatility. This project uses a configurable zero risk-free-rate assumption by default; interpret it as a simplified comparison.
- **Maximum drawdown:** largest peak-to-trough decline in the cumulative wealth index.

Metrics are calculated from adjusted closing prices and daily percentage returns. Trading days are approximated as 252 per year.

## SQL / PostgreSQL

Create a database, then run:

```bash
psql -d market_analytics -f sql/schema.sql
```

After running the Python pipeline, load `data/raw/adjusted_prices.csv` into the `daily_prices` table using your preferred PostgreSQL import method (for example, `\copy`). Example:

```sql
\copy daily_prices(date, ticker, adjusted_close)
FROM 'data/raw/adjusted_prices_long.csv'
WITH (FORMAT csv, HEADER true);
```

The download script also creates `adjusted_prices_long.csv` for this purpose. Then run the queries in `sql/analysis_queries.sql`.

## Power BI dashboard

Import these files from `outputs/`:
- `asset_performance.csv`
- `annual_returns.csv`
- `monthly_returns.csv`

Suggested report pages:

**Page 1 — Executive overview**
- KPI cards: best annualized return, lowest volatility, strongest Sharpe ratio
- Line chart: cumulative growth of $10,000
- Slicers: ticker and date range

**Page 2 — Risk and return**
- Scatter plot: annualized volatility vs. annualized return
- Bar chart: maximum drawdown by ticker
- Table: all performance metrics

**Page 3 — Performance over time**
- Matrix: annual returns by ticker and year
- Line chart: rolling annualized volatility
- Heatmap: correlation matrix

Document your DAX measures and include dashboard screenshots in the repository once built.

## Interpretation checklist

When writing the findings, answer:
- Did the asset with the highest return also have the highest volatility?
- Which asset experienced the deepest drawdown?
- Were correlations stable across the period?
- Did rankings change when measuring risk-adjusted returns?
- What limitations could affect the conclusions?

Do not claim causation from these descriptive comparisons.

## Limitations

- ETF proxies do not capture every investment exposure.
- Yahoo Finance data is a third-party source and may be revised or unavailable.
- This analysis does not model taxes, fees, bid-ask spreads, or investor-specific constraints.
- Sharpe ratios depend on the risk-free-rate assumption.
- Historical data contains survivorship and selection limitations.

## Next improvements

- Add a risk-free-rate series and calculate excess-return Sharpe ratios.
- Compare rolling correlations across market regimes.
- Add a PostgreSQL ingestion script and automated data-quality checks.
- Publish an interactive Power BI report with documented measures.
- Add a scheduled refresh workflow.

## Author

**Jabriel Abdille**  
Data Science student | Data Analytics | Python | SQL | BI
