import numpy as np
import pandas as pd

import pytest
from src.metrics import calculate_metrics, period_returns


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


def test_first_day_loss_is_in_drawdown():
    prices = pd.DataFrame({'LOSS': [100.0, 80.0, 90.0]}, index=pd.bdate_range('2020-01-01', periods=3))
    assert np.isclose(calculate_metrics(prices).iloc[0].maximum_drawdown, -0.2)


def test_missing_prices_do_not_create_zero_returns():
    prices = pd.DataFrame({'GAP': [100.0, np.nan, 110.0, 120.0]}, index=pd.bdate_range('2020-01-01', periods=4))
    with pytest.raises(ValueError, match='finite and positive'):
        calculate_metrics(prices)


@pytest.mark.parametrize('values', [[100, 0, 110], [100, -1, 110], [100, np.inf, 110]])
def test_invalid_prices_are_rejected(values):
    with pytest.raises(ValueError):
        calculate_metrics(pd.DataFrame({'A': values}, index=pd.bdate_range('2020-01-01', periods=3)))


def test_constant_prices_have_no_sharpe():
    p = pd.DataFrame({'A': [100, 100, 100]}, index=pd.bdate_range('2020-01-01', periods=3))
    m = calculate_metrics(p).iloc[0]
    assert np.isnan(m.sharpe_ratio)
    assert m.annualized_volatility == m.maximum_drawdown == m.cumulative_return == 0


def test_period_returns_include_first_loss_and_compound():
    p = pd.DataFrame({'A': [100., 80., 120., 90.]}, index=pd.to_datetime(['2020-12-30','2020-12-31','2021-01-04','2021-01-05']))
    result = period_returns(p, 'Y')
    assert np.isclose(result.iloc[0,0], -.2)
    assert np.isclose(result.iloc[1,0], .125)
    assert np.isclose((1+result.A).prod()-1, -.1)


def test_tail_loss_matches_manual_fixture():
    p = pd.DataFrame({'A': [100., 80., 120., 90.]}, index=pd.bdate_range('2020-01-01', periods=4))
    m = calculate_metrics(p).iloc[0]
    assert np.isclose(m.daily_var95, .245)
    assert np.isclose(m.daily_es95, .25)
    assert np.isclose(m.maximum_drawdown, -.25)


def test_unsorted_or_duplicate_dates_rejected():
    for dates in [['2020-01-02','2020-01-01','2020-01-03'], ['2020-01-01','2020-01-01','2020-01-03']]:
        with pytest.raises(ValueError, match='sorted and unique'):
            calculate_metrics(pd.DataFrame({'A':[100,101,102]}, index=pd.to_datetime(dates)))
