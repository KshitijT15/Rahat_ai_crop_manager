"""
retrain_price_model.py
Run this once to regenerate tomato_price_model.pkl compatible with your current
scikit-learn and numpy versions.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
import joblib
import os

print("Generating synthetic tomato price training data...")

# ── Generate synthetic training data ──────────────────────────────────────────
# Covers 5 years of daily dates
start = datetime(2019, 1, 1)
dates = [start + timedelta(days=i) for i in range(5 * 365)]

rows = []
for d in dates:
    month      = d.month
    day        = d.day
    year       = d.year
    dow        = d.weekday()
    doy        = d.timetuple().tm_yday
    quarter    = (month - 1) // 3 + 1
    is_weekend = 1 if dow >= 5 else 0

    # Realistic seasonal price pattern (INR / Quintal)
    seasonal   = 25 + 8 * np.sin(2 * np.pi * doy / 365)
    trend      = (year - 2019) * 2          # slight yearly inflation
    noise      = np.random.normal(0, 3)
    avg_price  = seasonal + trend + noise
    min_price  = avg_price - np.random.uniform(3, 7)
    max_price  = avg_price + np.random.uniform(3, 7)

    rows.append([day, month, year, dow, doy, quarter, is_weekend,
                 min_price, avg_price, max_price])

df = pd.DataFrame(rows, columns=[
    "day", "month", "year", "day_of_week", "day_of_year",
    "quarter", "is_weekend", "min_price", "avg_price", "max_price"
])

X = df[["day", "month", "year", "day_of_week", "day_of_year", "quarter", "is_weekend"]].values
y = df[["min_price", "avg_price", "max_price"]].values

print(f"Training on {len(X)} samples...")

# ── Train model ───────────────────────────────────────────────────────────────
base_gbr = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=4,
    random_state=42
)
model = MultiOutputRegressor(base_gbr)
model.fit(X, y)

# ── Save model ────────────────────────────────────────────────────────────────
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/tomato_price_model.pkl")
print("✅ Saved models/tomato_price_model.pkl")

# ── Quick sanity check ────────────────────────────────────────────────────────
test_date = datetime(2026, 6, 15)
test_X = np.array([[
    test_date.day, test_date.month, test_date.year,
    test_date.weekday(), test_date.timetuple().tm_yday,
    (test_date.month - 1) // 3 + 1,
    1 if test_date.weekday() >= 5 else 0
]])
preds = model.predict(test_X)[0]
print(f"\nSanity check for 2026-06-15:")
print(f"  Min: ₹{preds[0]:.2f} | Avg: ₹{preds[1]:.2f} | Max: ₹{preds[2]:.2f} per Quintal")
print("\nDone! Now run: python app.py")