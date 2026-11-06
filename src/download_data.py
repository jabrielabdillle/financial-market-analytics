"""Download adjusted ETF prices and prepare tidy CSV files."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

DEFAULT_TICKERS = ["SPY", "QQQ", "IWM", "EFA", "AGG", "GLD"]


def download_prices(tickers: list[str], start: str) -> pd.DataFrame:
    """Return adjusted close prices indexed by date."""
    data = yf.download(
        tickers=tickers,
        start=start,
        auto_adjust=True,
        progress=False,
        group_by="column",
        threads=True,
    )
    if data.empty:
        raise RuntimeError("No market data returned. Check the tickers or data provider.")

    # yfinance returns MultiIndex columns for multiple tickers; single ticker can differ.
    if isinstance(data.columns, pd.MultiIndex):
        level_names = list(data.columns.names)
        if "Close" in data.columns.get_level_values(0):
            prices = data["Close"].copy()
        elif "Close" in data.columns.get_level_values(-1):
            prices = data.xs("Close", axis=1, level=-1).copy()
        else:
            raise RuntimeError(f"Could not locate adjusted close prices. Column levels: {level_names}")
    else:
        if "Close" not in data.columns:
            raise RuntimeError("Could not locate adjusted close prices.")
        prices = data[["Close"]].rename(columns={"Close": tickers[0]})

    if isinstance(prices, pd.Series):
        prices = prices.to_frame(name=tickers[0])

    prices.index = pd.to_datetime(prices.index).tz_localize(None)
    prices = prices.sort_index().dropna(how="all")
    prices.columns.name = "ticker"
    return prices


def save_outputs(prices: pd.DataFrame) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    prices.index.name = "date"
    prices.to_csv(RAW_DIR / "adjusted_prices.csv", float_format="%.6f")

    long_prices = (
        prices.rename_axis("date")
        .reset_index()
        .melt(id_vars="date", var_name="ticker", value_name="adjusted_close")
        .dropna()
    )
    long_prices["date"] = pd.to_datetime(long_prices["date"]).dt.strftime("%Y-%m-%d")
    long_prices.to_csv(RAW_DIR / "adjusted_prices_long.csv", index=False, float_format="%.6f")

    returns = prices.pct_change().dropna(how="all")
    returns.index.name = "date"
    returns.to_csv(PROCESSED_DIR / "daily_returns.csv", float_format="%.8f")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", default="2012-01-01", help="Start date, YYYY-MM-DD")
    parser.add_argument("--tickers", nargs="+", default=DEFAULT_TICKERS)
    args = parser.parse_args()

    prices = download_prices(args.tickers, args.start)
    save_outputs(prices)
    print(f"Saved {len(prices):,} trading-day rows for {len(prices.columns)} tickers.")


if __name__ == "__main__":
    main()
