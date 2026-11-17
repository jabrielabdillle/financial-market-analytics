# Methodology

The public demo uses a deterministic factor simulation (NumPy PCG64 seed 42), six fictional asset models, and weekday dates from 2006-01-02 to 2025-12-31. This is not historical ETF data. Stress intervals are arbitrary and parameters are not estimated from observations. Weekday dates include exchange holidays. Default risk-free rate is zero.

## Definitions
- Daily return: P(t)/P(t-1)-1. Require a complete aligned panel of finite positive prices, sorted unique daily dates and at least three observations. Reject gaps instead of implicitly carrying prices forward.
- Total return: last price / first price - 1.
- CAGR: (last / first)^(365.25 / elapsed calendar days)-1. Short windows can produce extreme annualized values.
- Annualized volatility: sample standard deviation of daily returns times sqrt(252).
- Sharpe: mean excess daily return / sample standard deviation times sqrt(252). Convert the annual effective risk-free assumption to a daily effective rate. Zero variance yields undefined Sharpe, displayed as a dash.
- Drawdown: price / running maximum price - 1, including the initial price. Maximum drawdown is the minimum of that series.
- Historical VaR95: linear-interpolated 95th percentile of daily losses (-return). ES95: average observed loss at or above that threshold. These describe the selected sample, not a forecast. Negative values are possible in all-gain samples.
- Correlation: Pearson correlation of paired daily returns. Constant series produce undefined correlation.
- Period returns: compound observed daily returns within each month/year; first and last periods may be partial. No return is invented for the first price date.

## Storage and reproducibility
`python -m src.export` creates prices.csv, metrics.csv, annual_returns.csv, market.json, provenance.json and market.sqlite under web/public/data. SQLite uses a composite (date,ticker) key and positive-price constraint. Metadata includes the CSV SHA-256, row counts, source, adjustment convention and assumptions. Generated demo files are rebuilt in CI, not checked into Git.

For private analysis of an actual dataset, pass `--prices file.csv --source 'provider, retrieval date' --adjustment 'adjustment convention'`. Input is wide CSV with a date column and one price column per asset. Import metadata is a declaration, not independent verification of quality or redistribution rights. Publish only data you are entitled to redistribute.

This project has no predictive model, automated trading, transaction costs, tax model or investment recommendation. The existing PostgreSQL scripts are templates; the working database exporter uses SQLite.
