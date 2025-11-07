"""Data cleaning and aggregation pipeline."""
import pandas as pd
from .utils import normalize_category, impute_amounts


def pipeline_clean_and_aggregate(df_input: pd.DataFrame) -> pd.DataFrame:
    """Clean transaction dataframe and return month x category aggregated totals.

    Returns a DataFrame with columns ['month', 'category_clean', 'amount_imputed'] matching original shape.
    """
    dfc = df_input.copy()
    dfc['date'] = pd.to_datetime(dfc['date'])
    dfc['category_clean'] = dfc['category'].apply(normalize_category)
    dfc['amount_imputed'] = impute_amounts(dfc, category_col='category_clean', amount_col='amount')
    dfc['month'] = dfc['date'].dt.to_period('M').dt.to_timestamp()
    monthly = dfc.groupby(['month', 'category_clean'], as_index=False)['amount_imputed'].sum()
    return monthly # type: ignore
