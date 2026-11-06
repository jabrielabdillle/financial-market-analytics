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
TRADING_DAYS = 252


def calculate_metrics(prices: pd.DataFrame, risk_free_rate: float = 0.0) -> pd.DataFrame:
    """Calculate descriptive performance metrics for each price series."""
    returns = prices.pct_change().dropna(how="all")
    rows = []

    for ticker in prices.columns:
        series = prices[ticker].dropna()
        asset_returns = returns[ticker].dropna()
        if len(series) < 2 or asset_returns.empty:
            continue

        years = len(asset_returns) / TRADING_DAYS
        cumulative_return = series.iloc[-1] / series.iloc[0] - 1
        annualized_return = (series.iloc[-1] / series.iloc[0]) ** (1 / years) - 1 if years > 0 else np.nan
        annualized_volatility = asset_returns.std(ddof=1) * np.sqrt(TRADING_DAYS)
        daily_rf = (1 + risk_free_rate) ** (1 / TRADING_DAYS) - 1
        excess_returns = asset_returns - daily_rf
        sharpe = (
            excess_returns.mean() / asset_returns.std(ddof=1) * np.sqrt(TRADING_DAYS)
            if asset_returns.std(ddof=1) > 0 else np.nan
        )
        wealth = (1 + asset_returns).cumprod()
        drawdown = wealth / wealth.cummax() - 1

        rows.append({
            "ticker": ticker,
            "start_date": series.index.min().date().isoformat(),
            "end_date": series.index.max().date().isoformat(),
            "observations": len(asset_returns),
            "cumulative_return": cumulative_return,
            "annualized_return": annualized_return,
            "annualized_volatility": annualized_volatility,
            "sharpe_ratio": sharpe,
            "maximum_drawdown": drawdown.min(),
        })

    return pd.DataFrame(rows).sort_values("annualized_return", ascending=False)


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

    wealth = (1 + returns).cumprod()
    drawdowns = wealth / wealth.cummax() - 1
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
    prices = prices.apply(pd.to_numeric, errors="coerce").dropna(how="all")
    returns = prices.pct_change().dropna(how="all")
    metrics = calculate_metrics(prices)
    annual_returns = prices.resample("YE").last().pct_change()
    annual_returns.index = annual_returns.index.year
    annual_returns.index.name = "year"
    monthly_returns = prices.resample("ME").last().pct_change().dropna(how="all")
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
