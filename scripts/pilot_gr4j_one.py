"""Calibrate GR4J on one basin (train 1990-1999, warm-up 1989) and score the test years 2000-2008."""
import sys, time, numpy as np
from scipy.optimize import differential_evolution
sys.path.insert(0, "scripts")
from gr4j import gr4j, nse, load_basin

gauge = sys.argv[1] if len(sys.argv) > 1 else "01031500"
df = load_basin(gauge)
P, E, Qobs = df["prcp"].values, df["pet"].values, df["q_mm"].values
yrs = df["date"].dt.year.values
warm = (yrs >= 1989); train = (yrs >= 1990) & (yrs <= 1999); test = (yrs >= 2000) & (yrs <= 2008)
run_mask = yrs >= 1989  # run from 1989 onward; 1989 is warm-up and never scored

def loss(theta):
    Q = gr4j(P[run_mask], E[run_mask], *theta)
    return -nse(Qobs[run_mask][train[run_mask]], Q[train[run_mask]])

bounds = [(10, 2500), (-5, 5), (10, 800), (0.5, 10)]
t0 = time.time()
res = differential_evolution(loss, bounds, seed=533, maxiter=60, popsize=12, tol=1e-6, polish=True)
x = res.x
Q = gr4j(P[run_mask], E[run_mask], *x)
print(f"basin {gauge}: calibrated in {time.time()-t0:.0f}s")
print(f"  x1 soil bucket {x[0]:.0f} mm | x2 exchange {x[1]:+.2f} mm/day | x3 slow bucket {x[2]:.0f} mm | x4 delay {x[3]:.2f} days")
print(f"  NSE train 1990-1999: {nse(Qobs[run_mask][train[run_mask]], Q[train[run_mask]]):.3f}")
print(f"  NSE test  2000-2008: {nse(Qobs[run_mask][test[run_mask]],  Q[test[run_mask]]):.3f}")
print(f"  missing flow days in test: {int(np.isnan(Qobs[test]).sum())} of {int(test.sum())}")
