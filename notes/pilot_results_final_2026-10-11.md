# Pilot results, final (draw 2, corrected rule, melt cap 50), 2026-10-11

Test NSE, 2000-2008. Learner scores are means over five seeds.

| gauge | basin | snow share | physics no snow | physics | XGBoost | hybrid |
|---|---|---|---|---|---|---|
| 01414500 | Mill Brook, NY | 0.22 | 0.45 | 0.36 | 0.36 | 0.34 |
| 01532000 | Towanda Creek, PA | 0.18 | 0.67 | 0.66 | 0.20 | 0.64 |
| 07376000 | Tickfaw River, LA | 0.00 | 0.77 | 0.77 | 0.68 | 0.81 |
| 13235000 | SF Payette River, ID | 0.68 | 0.07 | 0.65 | 0.51 | 0.75 |
| 06632400 | Rock Creek, WY | 0.74 | 0.19 | 0.55 | 0.65 | 0.69 |

Per-basin differences (D_b) in test NSE:

| comparison | NY | PA | LA | ID | WY | mean | sd |
|---|---|---|---|---|---|---|---|
| hybrid minus physics | -0.02 | -0.03 | +0.04 | +0.09 | +0.15 | +0.05 | 0.075 |
| hybrid minus XGBoost | -0.03 | +0.43 | +0.13 | +0.23 | +0.05 | +0.16 | 0.18 |
| XGBoost minus physics | 0.00 | -0.46 | -0.09 | -0.14 | +0.10 | -0.12 | 0.21 |

Findings:
1. Snow module: on the two snow-dominated basins the physics score rose from 0.07 to 0.65 (ID) and 0.19 to 0.55 (WY); on the snow-free basin it was unchanged; on Mill Brook (22% snow) it was 0.09 lower (0.45 to 0.36). The lower score on Mill Brook is a calibration-search limitation: with the no-snow parameters and a large melt factor the snow version reaches 0.44, but the six-parameter search did not find that region. Decision 15 fixes this for the confirmatory run.
2. Hybrid beat XGBoost on 4 of 5 basins; hybrid beat physics on 3 of 5, by small margins (-0.03 to +0.15). Physics and hybrid are close on low-snow basins; the hybrid's gain is largest on the snow-dominated basins.
3. NSE across arms spans 0.20 to 0.81 with the snow module; 0.07 without it. Long lower tail confirmed.
4. Seed-to-seed sd of the learners is at most 0.025: seeds are a minor nuisance.
Raw: notes/pilot_three_arms.csv, notes/pilot_three_arms.log.
