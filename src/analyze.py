"""Calculate performance and risk metrics from downloaded market prices."""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PRICE_FILE = ROOT / "data" / "raw" / "adjusted_prices.csv"
OUTPUT_DIR = ROOT / "outputs"
from .metrics import TRADING_DAYS, calculate_metrics, validate_prices, period_returns


def create_charts(prices: pd.DataFrame, returns: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    normalized = prices / prices.apply(lambda col: col.dropna().iloc[0])
    ax = normalized.plot(figsize=(12, 6), linewidth=1.5)
    ax.set_title("Growth of $1 (normalized adjusted prices)")
    ax.set_ylabel("Portfolio value")
    ax.set_xlabel("Date")
    ax.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "cumulative_growth.png", dpi=160)
    plt.close()

    drawdowns = prices / prices.cummax() - 1
    ax = drawdowns.plot(figsize=(12, 6), linewidth=1)
    ax.set_title("Historical drawdowns")
    ax.set_ylabel("Drawdown")
    ax.set_xlabel("Date")
    ax.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "drawdowns.png", dpi=160)
    plt.close()

    rolling_vol = returns.rolling(63).std() * np.sqrt(TRADING_DAYS)
    ax = rolling_vol.plot(figsize=(12, 6), linewidth=1)
    ax.set_title("Rolling 63-trading-day annualized volatility")
    ax.set_ylabel("Annualized volatility")
    ax.set_xlabel("Date")
    ax.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "rolling_volatility.png", dpi=160)
    plt.close()


def run_analysis(prices: pd.DataFrame) -> dict[str, pd.DataFrame]:
    prices = validate_prices(prices)
    returns = prices.pct_change(fill_method=None).dropna(how="all")
    metrics = calculate_metrics(prices)
    annual_returns = period_returns(prices, "Y")
    annual_returns.index.name = "year"
    monthly_returns = period_returns(prices, "M")
    monthly_returns.index.name = "month"
    correlations = returns.corr()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(OUTPUT_DIR / "asset_performance.csv", index=False)
    annual_returns.to_csv(OUTPUT_DIR / "annual_returns.csv", float_format="%.6f")
    monthly_returns.to_csv(OUTPUT_DIR / "monthly_returns.csv", float_format="%.6f")
    correlations.to_csv(OUTPUT_DIR / "correlation_matrix.csv", float_format="%.6f")
    create_charts(prices, returns)

    return {
        "metrics": metrics,
        "annual_returns": annual_returns,
        "monthly_returns": monthly_returns,
        "correlations": correlations,
    }


def main() -> None:
    if not PRICE_FILE.exists():
        raise FileNotFoundError("Price data not found. Run: python -m src.download_data")
    prices = pd.read_csv(PRICE_FILE, index_col="date", parse_dates=True)
    results = run_analysis(prices)
    print("\nAsset performance summary:")
    print(results["metrics"].round(4).to_string(index=False))
    print(f"\nOutputs saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
