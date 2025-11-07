"""Matplotlib visualizations for the demo."""
import matplotlib.pyplot as plt
import pandas as pd


def plot_category_bar(latest_totals: pd.Series, month_timestamp: pd.Timestamp):
    plt.figure(figsize=(10, 5))
    ax = latest_totals.sort_values(ascending=False).plot(kind='bar')
    plt.title(f'Category-wise spending - {month_timestamp.strftime("%Y-%m")}')
    plt.ylabel('Amount')
    plt.xlabel('Category')
    plt.tight_layout()
    plt.show()


def plot_forecast_series(forecast_series: pd.Series, actual_series_index: pd.DatetimeIndex, pred_mean: float, pred_ci: tuple):
    plt.figure(figsize=(11, 5))
    # actual part is the forecast_series except last point
    actual_series = pd.Series(index=actual_series_index, data=forecast_series.iloc[:-1].values)
    plt.plot(actual_series.index, actual_series.values, marker='o', label='Actual total') # type: ignore
    next_month = forecast_series.index[-1]
    plt.plot([next_month], [pred_mean], marker='X', markersize=10, label='Predicted next month')
    ci_low, ci_high = pred_ci
    plt.vlines(next_month, ci_low, ci_high, linestyle='--', label='95% CI')
    plt.title('Total monthly spending — actual and 1-month forecast')
    plt.xlabel('Month')
    plt.ylabel('Total spending')
    plt.legend()
    plt.tight_layout()
    plt.show()
