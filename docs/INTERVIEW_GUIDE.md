# Interview guide

## One-minute explanation

“I built a reproducible market analytics application to explore how return and risk rankings change across assets and time windows. The public demo contains 31,308 synthetic price observations across six fictional asset models. Python validates the data and calculates metrics such as CAGR, volatility, maximum drawdown, Sharpe and tail losses. I export a real SQLite database and use WebAssembly to query it in a browser dashboard. I also compare the browser's calculations against Python reference outputs and deploy through GitHub Actions to GitHub Pages.”

## Technical decisions to explain

**Why synthetic data?** It gives a reproducible, openly distributable demo and lets me exercise stress scenarios. It cannot establish any real asset's performance. The same exporter accepts adjusted-price CSVs with explicit source metadata.

**Why SQLite?** It demonstrates relational storage, a composite key, an index and parameterized queries without a paid database server. The trade-off is a downloadable snapshot with no shared transactional writes.

**What calculation bug did you fix?** Computing drawdown from returns alone can omit the initial investment. For prices 100 → 80 → 90, a return-only wealth series starts at 0.8 and can report no drawdown. Comparing prices to their running maximum correctly records a 20% decline.

**What about missing prices?** I reject an incomplete panel. Implicit forward filling can create artificial zero returns and distort volatility and correlation. A real ingestion pipeline needs an explicit trading-calendar and missing-data policy.

**Why both Python and JavaScript calculations?** Python generates auditable reference metrics. JavaScript makes custom windows interactive without a backend. Tests compare every full-window browser metric to Python, and simple analytical fixtures cover edge cases.

**What does Sharpe mean here?** It divides mean excess daily return by daily variation, then annualizes. The risk-free rate is a user assumption, zero by default. It is undefined for zero variance, and it does not describe all forms of risk.

**What is the difference between VaR and expected shortfall?** VaR gives a loss percentile. Expected shortfall summarizes observed losses at or beyond that threshold. Here both are descriptive sample statistics, not predictions.

**What would you improve next?** Use licensed historical adjusted prices, a genuine trading calendar and a measured risk-free series. Add data-quality reporting and evaluate how results change under different observation windows. A predictive model would need its own out-of-time evaluation; none is currently implemented.

## Demonstration sequence

1. Show the synthetic-data notice and explain reproducibility.
2. Change the focus asset and start date, then compare how metrics change.
3. Switch growth to drawdown and explain the running peak.
4. Open Price explorer, filter one asset, show pagination and export.
5. Open Methodology to show definitions and the dataset hash.

## Resume claims supported by this implementation

- Built a reproducible risk analytics pipeline for 31,308 synthetic price observations across six asset models using Python, Pandas, NumPy and indexed SQLite storage.
- Validated an interactive market research dashboard with 22 automated checks spanning Python regression tests, browser/Python metric agreement and Playwright workflows, and deployed it through GitHub Actions to GitHub Pages.

Do not claim real trading returns, predictive accuracy, deployed PostgreSQL/Power BI, live market feeds or measured commercial impact. Explain your own contribution and the AI assistance you used accurately when asked.
