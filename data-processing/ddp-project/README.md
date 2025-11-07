# ddp-project

This small demo project generates synthetic transaction data, cleans and aggregates it by month/category, and fits a simple OLS forecast using lag features.

Structure
- `ddp_project/` — package with reusable modules
  - `data_gen.py` — synthetic data generator
  - `utils.py` — normalization and imputation helpers
  - `pipeline.py` — cleaning & aggregation pipeline
  - `forecast.py` — forecasting logic
  - `visualize.py` — plotting helpers
- `main.py` — example runner that demonstrates the package
- `requirements.txt` — runtime dependencies

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the demo:

```bash
python main.py
```

3. Run tests (pytest):

```bash
pytest -q
```
