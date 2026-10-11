# Basin Bench

A controlled, preregistered comparison of physics-based, data-driven and hybrid
models for daily streamflow prediction on the CAMELS benchmark of 671 US river basins.

## Question

Does feeding the internal states of a conceptual rainfall-runoff model (GR4J) into a
gradient-boosted learner (XGBoost) predict daily streamflow better than either model
on its own, when all three are compared on the same basins, the same periods and the
same tuning budget?

## Why it matters

Hybrid physics-plus-learning models have been reported to beat both parents, but on a
handful of hand-picked catchments and with signs of overfitting. No large-sample,
paired, statistically controlled test exists on the standard benchmark. This project
supplies one, with the design, sample size and analysis fixed in writing before the
confirmatory data are touched.

## Design in one paragraph

The experimental unit is the basin. Each basin receives all three models (GR4J,
XGBoost with physics-free memory features, and the GR4J-state-fed hybrid) on identical
train and test periods, so the comparison is paired. The response is Nash-Sutcliffe
Efficiency per basin on the test period, with RMSE as a secondary metric. Pilot basins,
drawn by a written rule, are used only to learn the shape and spread of the response
and are excluded from the confirmatory run. The analysis plan, including the
multiple-comparison rule, is preregistered.

## Layout

- `notes/`      decisions, dated; pilot basin selection; reading notes
- `scripts/`    reproducible steps (selection, download, model runs)
- `notebooks/`  exploration and pilot analysis
- `data/`       CAMELS v1.2 (not tracked; see `notes/pilot_basins_2026-10-10.md` for the source)
- `slides/`     the running presentation

## Data

CAMELS: Catchment Attributes and Meteorology for Large-sample Studies, v1.2.
Addor, Newman, Mizukami and Clark (2017), DOI 10.5065/D6MW2F4D. Zenodo record 15529996, CC BY 4.0.

## Authors

Joshua Attih and Felix Oteng Mensah, University of New Mexico.
