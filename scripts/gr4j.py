"""GR4J daily rainfall-runoff model (Perrin, Michel, Andreassian 2003), plain Python.

Inputs per day: rain P (mm) and potential evaporation E (mm). Output: flow Q (mm/day).
Four parameters:
  x1  production (soil) store capacity, mm
  x2  groundwater exchange, mm/day (negative = loss)
  x3  routing store capacity, mm
  x4  unit hydrograph time base, days
Also here: Oudin potential evaporation from temperature and latitude, CAMELS loaders,
unit conversion and NSE.
"""
import math
import numpy as np
import pandas as pd


def _uh_ordinates(x4):
    n1 = int(math.ceil(x4)); n2 = int(math.ceil(2 * x4))
    def sh1(t):
        if t <= 0: return 0.0
        if t < x4: return (t / x4) ** 2.5
        return 1.0
    def sh2(t):
        if t <= 0: return 0.0
        if t < x4: return 0.5 * (t / x4) ** 2.5
        if t < 2 * x4: return 1 - 0.5 * (2 - t / x4) ** 2.5
        return 1.0
    uh1 = [sh1(i + 1) - sh1(i) for i in range(n1)]
    uh2 = [sh2(i + 1) - sh2(i) for i in range(n2)]
    return uh1, uh2


def gr4j(P, E, x1, x2, x3, x4, s0=0.3, r0=0.5, return_states=False):
    """Run GR4J. P, E arrays in mm/day. Returns Q (mm/day) and optionally internal states."""
    uh1, uh2 = _uh_ordinates(x4)
    n1, n2 = len(uh1), len(uh2)
    q1 = [0.0] * n1; q2 = [0.0] * n2
    S = s0 * x1; R = r0 * x3
    n = len(P)
    Q = np.empty(n); Sarr = np.empty(n); Rarr = np.empty(n); Fx = np.empty(n)
    for t in range(n):
        p, e = float(P[t]), float(E[t])
        if p >= e:
            pn, en = p - e, 0.0
            ws = math.tanh(pn / x1); sr = S / x1
            ps = x1 * (1 - sr * sr) * ws / (1 + sr * ws)
            S += ps; es = 0.0
        else:
            pn, en = 0.0, e - p
            ws = math.tanh(en / x1); sr = S / x1
            es = S * (2 - sr) * ws / (1 + (1 - sr) * ws)
            S -= es; ps = 0.0
        perc = S * (1 - (1 + (4.0 / 9.0 * S / x1) ** 4) ** -0.25)
        S -= perc
        pr = perc + (pn - ps)
        # split 90/10 into the two unit hydrographs
        for i in range(n1 - 1): q1[i] = q1[i + 1] + uh1[i] * 0.9 * pr
        q1[n1 - 1] = uh1[n1 - 1] * 0.9 * pr
        for i in range(n2 - 1): q2[i] = q2[i + 1] + uh2[i] * 0.1 * pr
        q2[n2 - 1] = uh2[n2 - 1] * 0.1 * pr
        f = x2 * (R / x3) ** 3.5
        R = max(0.0, R + q1[0] + f)
        qr = R * (1 - (1 + (R / x3) ** 4) ** -0.25)
        R -= qr
        qd = max(0.0, q2[0] + f)
        Q[t] = qr + qd
        Sarr[t] = S; Rarr[t] = R; Fx[t] = f
    if return_states:
        return Q, {"prod_store_mm": Sarr, "rout_store_mm": Rarr, "exchange_mm": Fx}
    return Q


def oudin_pet(tmean_c, doy, lat_deg):
    """Potential evaporation (mm/day), Oudin et al. 2005, from mean air temperature."""
    lat = math.radians(lat_deg)
    out = np.empty(len(tmean_c))
    for i, (T, d) in enumerate(zip(tmean_c, doy)):
        dr = 1 + 0.033 * math.cos(2 * math.pi * d / 365)
        dec = 0.409 * math.sin(2 * math.pi * d / 365 - 1.39)
        ws = math.acos(max(-1.0, min(1.0, -math.tan(lat) * math.tan(dec))))
        Ra = 24 * 60 / math.pi * 0.0820 * dr * (ws * math.sin(lat) * math.sin(dec) + math.cos(lat) * math.cos(dec) * math.sin(ws))
        out[i] = Ra / 2.45 * (T + 5) / 100 if T + 5 > 0 else 0.0
    return out


def nse(obs, sim):
    obs = np.asarray(obs, float); sim = np.asarray(sim, float)
    m = ~np.isnan(obs)
    return 1 - np.sum((obs[m] - sim[m]) ** 2) / np.sum((obs[m] - obs[m].mean()) ** 2)


def load_basin(gauge_id, root="data/pilot/basin_dataset_public_v1p2", product="maurer"):
    """Return one daily table: date, prcp, tmax, tmin, tmean, pet, q_mm (NaN where missing)."""
    import glob
    fpath = glob.glob(f"{root}/basin_mean_forcing/{product}/*/{gauge_id}_lump_*_forcing_leap.txt")[0]
    with open(fpath) as f:
        lat = float(f.readline()); _elev = float(f.readline()); area_m2 = float(f.readline())
    forc = pd.read_csv(fpath, sep=r"\s+", skiprows=3)
    forc.columns = ["year", "mnth", "day", "hr", "dayl", "prcp", "srad", "swe", "tmax", "tmin", "vp"]
    forc["date"] = pd.to_datetime(forc[["year", "mnth", "day"]].rename(columns={"mnth": "month"}))
    qpath = glob.glob(f"{root}/usgs_streamflow/*/{gauge_id}_streamflow_qc.txt")[0]
    q = pd.read_csv(qpath, sep=r"\s+", header=None, names=["gauge", "year", "month", "day", "q_cfs", "flag"], dtype={"gauge": str})
    q["date"] = pd.to_datetime(q[["year", "month", "day"]])
    q.loc[q["q_cfs"] < 0, "q_cfs"] = np.nan
    q["q_mm"] = q["q_cfs"] * 0.0283168 * 86400 / area_m2 * 1000
    df = forc[["date", "prcp", "tmax", "tmin"]].merge(q[["date", "q_mm", "flag"]], on="date", how="left")
    df["tmean"] = (df["tmax"] + df["tmin"]) / 2
    df["pet"] = oudin_pet(df["tmean"].values, df["date"].dt.dayofyear.values, lat)
    df.attrs.update({"lat": lat, "area_m2": area_m2, "gauge_id": gauge_id})
    return df
