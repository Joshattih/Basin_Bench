"""Pick the five pilot basins for Basin Bench by a fixed rule.

Rule (written before any daily record was opened, 2026-10-10):
  1. Take all 671 CAMELS basins with their aridity index (camels_clim.txt)
     and their fraction of zero-flow days (camels_hydro.txt).
  2. Drop basins that are dry on more than 5% of days.
  3. Sort the rest by aridity and cut into five equal bands.
  4. Draw one basin at random from each band, seed 533.
These five are for exploration only and are excluded from the confirmatory run.
"""
import pandas as pd
import numpy as np

SEED = 533
clim = pd.read_csv("data/camels_clim.txt", sep=";", dtype={"gauge_id": str})
hydro = pd.read_csv("data/camels_hydro.txt", sep=";", dtype={"gauge_id": str})
name = pd.read_csv("data/camels_name.txt", sep=";", dtype={"gauge_id": str})

df = clim.merge(hydro, on="gauge_id").merge(name, on="gauge_id")
print(f"all basins: {len(df)}")
df = df[df["zero_q_freq"] <= 5.0].copy()
print(f"after dropping basins dry >5% of days: {len(df)}")

df = df.sort_values("aridity").reset_index(drop=True)
df["band"] = pd.qcut(df["aridity"], 5, labels=["very wet", "wet", "middle", "dry", "very dry"])

rng = np.random.default_rng(SEED)
picks = []
for band, grp in df.groupby("band", observed=True):
    row = grp.iloc[rng.integers(len(grp))]
    picks.append(row)
picks = pd.DataFrame(picks)[["gauge_id", "gauge_name", "band", "aridity", "p_mean", "frac_snow", "zero_q_freq", "runoff_ratio"]]
print(picks.to_string(index=False))
picks.to_csv("notes/pilot_basins.csv", index=False)
