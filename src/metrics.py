"""Descriptive metrics for a complete daily adjusted-price panel."""
from __future__ import annotations
import numpy as np
import pandas as pd

TRADING_DAYS = 252

def validate_prices(prices: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(prices, pd.DataFrame) or len(prices) < 3 or len(prices.columns) == 0:
        raise ValueError('Provide at least three dates and one asset.')
    if not isinstance(prices.index, pd.DatetimeIndex) or prices.index.hasnans:
        raise ValueError('Prices require valid daily dates.')
    if prices.index.tz is not None or not prices.index.equals(prices.index.normalize()):
        raise ValueError('Use timezone-free daily dates, not intraday timestamps.')
    if not prices.index.is_monotonic_increasing or not prices.index.is_unique:
        raise ValueError('Dates must be sorted and unique.')
    if not prices.columns.is_unique or any(not isinstance(c, str) or not c.strip() for c in prices.columns):
        raise ValueError('Asset names must be nonempty, unique strings.')
    try:
        clean = prices.astype(float)
    except (ValueError, TypeError) as exc:
        raise ValueError('All prices must be numeric.') from exc
    if not np.isfinite(clean.to_numpy()).all() or (clean <= 0).any().any():
        raise ValueError('All prices must be finite and positive; align missing dates explicitly before analysis.')
    return clean

def calculate_metrics(prices: pd.DataFrame, risk_free_rate: float = 0.0) -> pd.DataFrame:
    prices = validate_prices(prices)
    if not np.isfinite(risk_free_rate) or risk_free_rate <= -1:
        raise ValueError('Annual effective risk-free rate must be finite and greater than -1.')
    returns = prices.pct_change(fill_method=None).iloc[1:]
    years = (prices.index[-1] - prices.index[0]).days / 365.25
    daily_rf = (1 + risk_free_rate) ** (1 / TRADING_DAYS) - 1
    rows = []
    for ticker in prices:
        series, r = prices[ticker], returns[ticker]
        sd = r.std(ddof=1)
        losses = -r
        var95 = losses.quantile(.95, interpolation='linear')
        rows.append(dict(ticker=ticker, start_date=prices.index[0].date().isoformat(),
            end_date=prices.index[-1].date().isoformat(), observations=len(r),
            cumulative_return=series.iloc[-1]/series.iloc[0]-1,
            annualized_return=(series.iloc[-1]/series.iloc[0])**(1/years)-1,
            annualized_volatility=sd*np.sqrt(TRADING_DAYS),
            sharpe_ratio=(r.mean()-daily_rf)/sd*np.sqrt(TRADING_DAYS) if sd > 1e-15 else np.nan,
            maximum_drawdown=(series/series.cummax()-1).min(),
            daily_var95=var95, daily_es95=losses[losses >= var95].mean()))
    return pd.DataFrame(rows).sort_values('annualized_return', ascending=False)

def period_returns(prices: pd.DataFrame, frequency: str) -> pd.DataFrame:
    """Compound available daily returns, including the first partial period."""
    prices = validate_prices(prices)
    if frequency not in ('Y', 'M'):
        raise ValueError('Frequency must be Y or M.')
    r = prices.pct_change(fill_method=None).iloc[1:]
    return (1+r).groupby(r.index.to_period(frequency)).prod()-1
