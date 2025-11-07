"""Forecasting helpers (simple OLS with lag features)."""
from typing import Tuple
import pandas as pd
import statsmodels.api as sm


def train_and_forecast(monthly_pivot: pd.DataFrame) -> Tuple[float, Tuple[float, float], pd.Series]:
    """Train a small OLS using 3 lags on total_all and return forecast mean, CI and forecast series.

    monthly_pivot must have a `total_all` column and DateTime index (month start timestamps).
    Returns: (pred_mean, (ci_low, ci_high), forecast_series)
    """
    ts = monthly_pivot[['total_all']].sort_index()
    for lag in [1, 2, 3]:
        ts[f'lag_{lag}'] = ts['total_all'].shift(lag)
    ts = ts.dropna()
    train = ts.iloc[:-1]
    test = ts.iloc[-1:]
    X_train = train[[f'lag_{l}' for l in [1, 2, 3]]]
    y_train = train['total_all']
    X_train_const = sm.add_constant(X_train)
    model = sm.OLS(y_train, X_train_const).fit()

    X_test = test[[f'lag_{l}' for l in [1, 2, 3]]]
    X_test_const = sm.add_constant(X_test)
    # Align columns/order with model parameters (const, lag_1, lag_2, lag_3)
    X_test_const = X_test_const.reindex(columns=model.params.index, fill_value=1.0) # type: ignore

    pred = model.get_prediction(X_test_const)
    pred_mean = float(pred.predicted_mean.iloc[0])
    pred_ci = tuple(pred.conf_int(alpha=0.05).iloc[0].tolist())

    # create forecast series that appends predicted value to actuals
    actual_series = monthly_pivot['total_all'].loc[ts.index]
    forecast_index = pd.date_range(start=ts.index.min(), periods=len(ts) + 1, freq='M')
    forecast_values = list(actual_series.values) + [pred_mean]
    forecast_series = pd.Series(index=forecast_index, data=forecast_values)

    return pred_mean, pred_ci, forecast_series
