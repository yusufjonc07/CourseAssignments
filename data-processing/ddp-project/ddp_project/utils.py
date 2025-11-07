"""Utility helpers: normalization and imputation."""
from typing import Any
import pandas as pd


def normalize_category(cat: Any) -> str:
    if pd.isna(cat):
        return 'unknown'
    c = str(cat).strip().lower()
    c = c.replace('3', 'e')
    mapping = {
        'transportation': 'transport',
    }
    return mapping.get(c, c)


def impute_amounts(df: pd.DataFrame, category_col: str = 'category_clean', amount_col: str = 'amount') -> pd.Series:
    """Return a Series of imputed amounts based on median per cleaned category."""
    medians = df.groupby(category_col)[amount_col].median()
    global_median = df[amount_col].median()
    return df.apply(lambda r: medians.get(r[category_col], global_median) if pd.isna(r[amount_col]) else r[amount_col], axis=1)
