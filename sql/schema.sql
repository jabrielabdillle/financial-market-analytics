CREATE TABLE IF NOT EXISTS daily_prices (
    date DATE NOT NULL,
    ticker VARCHAR(12) NOT NULL,
    adjusted_close NUMERIC(18, 6) NOT NULL CHECK (adjusted_close > 0),
    PRIMARY KEY (date, ticker)
);

CREATE INDEX IF NOT EXISTS idx_daily_prices_ticker_date
    ON daily_prices (ticker, date);

COMMENT ON TABLE daily_prices IS
    'Adjusted daily ETF prices downloaded from a public market-data provider.';
