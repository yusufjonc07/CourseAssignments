"""Top-level runner that demonstrates the organized ddp_project package.

This file is a thin wrapper which uses the package modules placed in
`ddp_project/` to generate data, run the cleaning/aggregation pipeline,
train a small OLS forecast and plot results.
"""

from ddp_project import (
    generate_sample_data,
    pipeline_clean_and_aggregate,
    train_and_forecast,
    plot_category_bar,
    plot_forecast_series,
)


def main():
    df = generate_sample_data()
    monthly = pipeline_clean_and_aggregate(df)
    # pivot into months x categories and compute total
    monthly_pivot = monthly.pivot(index='month', columns='category_clean', values='amount_imputed').fillna(0)
    monthly_pivot['total_all'] = monthly_pivot.sum(axis=1)

    latest_month = monthly_pivot.index.max()
    latest_totals = monthly_pivot.loc[latest_month].drop('total_all')
    # bar plot
    plot_category_bar(latest_totals, latest_month)

    # forecast
    pred_mean, pred_ci, forecast_series = train_and_forecast(monthly_pivot)
    # For plotting actuals we will use the index used by the model training
    # the function returns forecast_series which contains the appended predicted value
    plot_forecast_series(forecast_series, actual_series_index=forecast_series.index[:-1], pred_mean=pred_mean, pred_ci=pred_ci) # type: ignore

    next_month = forecast_series.index[-1]
    ci_low, ci_high = pred_ci
    print(f"Predicted total spending for next month ({next_month.strftime('%Y-%m')}): {pred_mean:.2f}")
    print(f"95% prediction interval: [{ci_low:.2f}, {ci_high:.2f}]")


if __name__ == '__main__':
    main()

