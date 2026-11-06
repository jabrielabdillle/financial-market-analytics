-- 1. Latest available observation for each asset
SELECT ticker, MAX(date) AS latest_date
FROM daily_prices
GROUP BY ticker
ORDER BY ticker;

-- 2. Daily returns using LAG
WITH price_changes AS (
    SELECT
        date,
        ticker,
        adjusted_close,
        LAG(adjusted_close) OVER (
            PARTITION BY ticker ORDER BY date
        ) AS previous_close
    FROM daily_prices
)
SELECT
    date,
    ticker,
    ROUND(
        ((adjusted_close / NULLIF(previous_close, 0)) - 1) * 100,
        4
    ) AS daily_return_pct
FROM price_changes
WHERE previous_close IS NOT NULL
ORDER BY ticker, date;

-- 3. Year-end price and annual return
WITH year_end_prices AS (
    SELECT DISTINCT ON (ticker, EXTRACT(YEAR FROM date))
        ticker,
        EXTRACT(YEAR FROM date)::INT AS year,
        date,
        adjusted_close
    FROM daily_prices
    ORDER BY ticker, EXTRACT(YEAR FROM date), date DESC
),
annual_changes AS (
    SELECT
        ticker,
        year,
        adjusted_close,
        LAG(adjusted_close) OVER (
            PARTITION BY ticker ORDER BY year
        ) AS prior_year_close
    FROM year_end_prices
)
SELECT
    ticker,
    year,
    ROUND(
        ((adjusted_close / NULLIF(prior_year_close, 0)) - 1) * 100,
        2
    ) AS annual_return_pct
FROM annual_changes
WHERE prior_year_close IS NOT NULL
ORDER BY ticker, year;

-- 4. Average price and observation count by calendar year
SELECT
    ticker,
    EXTRACT(YEAR FROM date)::INT AS year,
    ROUND(AVG(adjusted_close), 2) AS average_adjusted_close,
    COUNT(*) AS trading_days
FROM daily_prices
GROUP BY ticker, EXTRACT(YEAR FROM date)
ORDER BY ticker, year;
