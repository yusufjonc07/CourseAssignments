"""Data generation utilities for the demo."""
from datetime import datetime
import pandas as pd
import numpy as np
import random


def generate_sample_data(seed: int = 42, months: int = 24) -> pd.DataFrame:
    """Generate a synthetic transactions DataFrame similar to the original script.

    Columns: date, amount, category, desc
    """
    np.random.seed(seed)
    random.seed(seed)
    months_idx = pd.date_range(end=pd.Timestamp.today().normalize(), periods=months, freq='M')
    categories_clean = ['groceries', 'transport', 'rent', 'entertainment', 'utilities', 'health']

    rows = []
    for m in months_idx:
        for _ in range(random.randint(20, 40)):
            cat = np.random.choice(categories_clean, p=[0.25, 0.15, 0.18, 0.18, 0.12, 0.12])
            if np.random.rand() < 0.08:
                cat = cat.upper()
            if np.random.rand() < 0.06:
                cat = cat.replace('e', '3')
            if np.random.rand() < 0.05:
                cat = 'transportation'
            base = {
                'groceries': 30,
                'transport': 5,
                'rent': 800,
                'entertainment': 20,
                'utilities': 60,
                'health': 40,
                'transportation': 6,
            }.get(cat.lower(), 20)
            amount = round(np.random.gamma(shape=2.0, scale=base / 2), 2)
            if np.random.rand() < 0.03:
                amount = np.nan
            rows.append({'date': m - pd.Timedelta(days=random.randint(0, 27)), 'amount': amount, 'category': cat, 'desc': 'txn'})

    df = pd.DataFrame(rows)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sample(frac=1, random_state=1).reset_index(drop=True)
    return df
