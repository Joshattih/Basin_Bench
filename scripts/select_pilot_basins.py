"""Pick the five pilot basins for Basin Bench by a fixed rule.

Rule (written before any daily record was opened, 2026-10-10):
  1. Take all 671 CAMELS basins with their aridity index (camels_clim.txt)
     and their fraction of zero-flow days (camels_hydro.txt).
  2. Drop basins whose zero-flow share (a fraction, 0 to 1) is above 0.05, i.e. dry on
     more than one day in twenty, and basins whose zero-flow share is missing.
  3. Sort the rest by aridity and cut into five equal bands.
  4. Draw one basin at random from each band, seed 533.
These five are for exploration only and are excluded from the confirmatory run.

Correction 2026-10-11: the first version compared the zero-flow share against 5 instead
of 0.05, so the dry rule removed nothing and the one basin dropped (03281100, Goose Creek,
KY) was dropped for a blank attribute. See notes/decision_log.md item 13.
"""
import pandas as pd
import numpy as np

SEED = 533
clim = pd.read_csv("data/camels_clim.txt", sep=";", dtype={"gauge_id": str})
hydro = pd.read_csv("data/camels_hydro.txt", sep=";", dtype={"gauge_id": str})
name = pd.read_csv("data/camels_name.txt", sep=";", dtype={"gauge_id": str})

df = clim.merge(hydro, on="gauge_id").merge(name, on="gauge_id")
print(f"all basins: {len(df)}")
missing = df["zero_q_freq"].isna()
print(f"dropped for missing zero-flow attribute: {int(missing.sum())} ({df[missing].gauge_name.tolist()})")
dry = df["zero_q_freq"] > 0.05
print(f"dropped for being dry on more than 1 day in 20: {int(dry.sum())}")
df = df[~missing & ~dry].copy()
print(f"remaining: {len(df)}")

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
