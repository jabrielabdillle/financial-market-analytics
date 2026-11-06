import numpy as np
import pandas as pd

from src.analyze import calculate_metrics


def test_metrics_on_simple_price_series():
    dates = pd.bdate_range("2020-01-01", periods=253)
    prices = pd.DataFrame({"TEST": np.linspace(100, 110, len(dates))}, index=dates)

    result = calculate_metrics(prices)
    assert len(result) == 1
    assert result.loc[0, "ticker"] == "TEST"
    assert result.loc[0, "cumulative_return"] > 0
    assert result.loc[0, "annualized_volatility"] >= 0
    assert result.loc[0, "maximum_drawdown"] <= 0


def test_multiple_assets_are_returned():
    dates = pd.bdate_range("2021-01-01", periods=30)
    prices = pd.DataFrame({
        "AAA": np.linspace(100, 120, len(dates)),
        "BBB": np.linspace(100, 95, len(dates)),
    }, index=dates)

    result = calculate_metrics(prices)
    assert set(result["ticker"]) == {"AAA", "BBB"}
