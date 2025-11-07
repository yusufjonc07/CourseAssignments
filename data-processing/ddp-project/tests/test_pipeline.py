import pandas as pd
from ddp_project.pipeline import pipeline_clean_and_aggregate


def test_pipeline_basic():
    # small contrived dataset covering two months and two categories (with a NaN)
    rows = [
        {'date': '2025-01-05', 'amount': 10.0, 'category': 'groceries'},
        {'date': '2025-01-15', 'amount': None, 'category': 'groceries'},
        {'date': '2025-02-02', 'amount': 20.0, 'category': 'transport'},
    ]
    df = pd.DataFrame(rows)
    monthly = pipeline_clean_and_aggregate(df)
    # expect two months present
    months = sorted(monthly['month'].dt.strftime('%Y-%m').unique())
    assert months == ['2025-01', '2025-02']
    # ensure categories present
    cats = sorted(monthly['category_clean'].unique())
    assert 'groceries' in cats and 'transport' in cats
