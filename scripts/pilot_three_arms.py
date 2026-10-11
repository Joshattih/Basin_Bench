"""Pilot: all three arms on the five pilot basins. Writes notes/pilot_three_arms.csv.

Arm 1  GR4J + CemaNeige, calibrated 1990-1999 (warm-up 1989), scored 2000-2008.
Arm 2  XGBoost alone: today's weather + day of year + rain totals over 7/30/90 days.
Arm 3  Hybrid: arm 2 inputs + four GR4J states (soil store, routing store, exchange, snowpack).
Learners: same fixed settings, same 5 seeds, trained 1990-1999, tested 2000-2008.
Per basin per arm: one test NSE (learners averaged over seeds). Pilot only; not reused.
"""
import sys, time, numpy as np, pandas as pd
from scipy.optimize import differential_evolution
import xgboost as xgb
sys.path.insert(0, "scripts")
from gr4j import gr4j_snow, nse, load_basin

BASINS = ["01031500", "01557500", "05408000", "10348850", "06154410"]
SEEDS = [1, 2, 3, 4, 5]
XGB = dict(n_estimators=400, max_depth=6, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, min_child_weight=5)
BOUNDS = [(10, 2500), (-5, 5), (10, 800), (0.5, 10), (0.0, 1.0), (0.5, 10.0)]

rows = []
for g in BASINS:
    t0 = time.time()
    df = load_basin(g)
    yrs = df["date"].dt.year.values
    run = yrs >= 1989
    d = df[run].reset_index(drop=True); y = yrs[run]
    train = (y >= 1990) & (y <= 1999); test = (y >= 2000) & (y <= 2008)
    P, T, E, Q = d["prcp"].values, d["tmean"].values, d["pet"].values, d["q_mm"].values

    # Arm 1: physics with snow
    def loss(th):
        return -nse(Q[train], gr4j_snow(P, T, E, *th)[train])
    res = differential_evolution(loss, BOUNDS, seed=533, maxiter=60, popsize=12, tol=1e-6, polish=True)
    Qp, st = gr4j_snow(P, T, E, *res.x, return_states=True)
    nse_phys = nse(Q[test], Qp[test])

    # Features for learners
    X = pd.DataFrame({
        "prcp": P, "tmax": d["tmax"].values, "tmin": d["tmin"].values, "pet": E,
        "doy_sin": np.sin(2 * np.pi * d["date"].dt.dayofyear / 365.25),
        "doy_cos": np.cos(2 * np.pi * d["date"].dt.dayofyear / 365.25),
        "rain7": pd.Series(P).rolling(7, min_periods=1).sum().values,
        "rain30": pd.Series(P).rolling(30, min_periods=1).sum().values,
        "rain90": pd.Series(P).rolling(90, min_periods=1).sum().values,
    })
    Xh = X.copy()
    for k in ["prod_store_mm", "rout_store_mm", "exchange_mm", "snowpack_mm"]:
        Xh[k] = st[k]
    ok = ~np.isnan(Q)

    def learner(Xf):
        scores = []
        for s in SEEDS:
            m = xgb.XGBRegressor(random_state=s, n_jobs=4, **XGB)
            m.fit(Xf[train & ok], Q[train & ok])
            scores.append(nse(Q[test], m.predict(Xf[test])))
        return float(np.mean(scores)), float(np.std(scores))

    nse_ml, sd_ml = learner(X)
    nse_hy, sd_hy = learner(Xh)
    rows.append(dict(gauge=g, physics=nse_phys, xgb=nse_ml, hybrid=nse_hy, xgb_seed_sd=sd_ml, hybrid_seed_sd=sd_hy,
                     ctg=res.x[4], kf=res.x[5]))
    print(f"{g}: physics {nse_phys:.3f} | xgb {nse_ml:.3f} (seed sd {sd_ml:.3f}) | hybrid {nse_hy:.3f} (seed sd {sd_hy:.3f}) | {time.time()-t0:.0f}s", flush=True)

out = pd.DataFrame(rows)
out["hy_minus_phys"] = out["hybrid"] - out["physics"]
out["hy_minus_xgb"] = out["hybrid"] - out["xgb"]
out["xgb_minus_phys"] = out["xgb"] - out["physics"]
out.to_csv("notes/pilot_three_arms.csv", index=False)
print(out.round(3).to_string(index=False))
