# Basin Bench decision log

One line per decision, dated, never deleted. A changed decision gets a new line that points to the old one.

1. 2026-10-10. Question: does a hybrid (GR4J internal states fed to XGBoost) predict daily streamflow better than GR4J alone or XGBoost alone on CAMELS?
2. 2026-10-10. Data: CAMELS v1.2, Maurer forcing (1980-2008), USGS daily flow. Zenodo 15529996, DOI 10.5065/D6MW2F4D, CC BY 4.0.
3. 2026-10-10. Unit of analysis: one basin. All arms score every basin; comparison is paired on basin. Seeds and days are not replicates.
4. 2026-10-10. Pilot basins: five, by rule before any daily record was opened (drop basins dry >5% of days; sort by aridity; five equal bands; one per band at random, seed 533). 01031500, 01557500, 05408000, 10348850, 06154410. Pilot only; excluded from the confirmatory run.
5. 2026-10-10. Time windows: warm-up 1989, calibrate/train 1990-1999, test 2000-2008, same for all arms.
6. 2026-10-10. Metric: NSE per basin on the test period (primary), RMSE mm/day (secondary). Missing flow days dropped, never zero.
7. 2026-10-10. Learner memory: XGBoost alone gets physics-free memory (rain totals over 7, 30, 90 days). Hybrid gets the same plus four GR4J states (soil store, routing store, exchange, snowpack).
8. 2026-10-10. Equal tuning: both learners use one fixed setting, the same five seeds, the same split.
9. 2026-10-11. Snow: pilot run 1 showed GR4J without snow fails on snowy basins (NSE -0.86 at 83% snow). Decision: add CemaNeige to the physics arm. Rejected alternative: restrict to low-snow basins.
10. 2026-10-11. Pilot run 2 (all arms): hybrid beat XGBoost on 5/5 basins; hybrid vs physics 2 wins, 3 losses. The M0 expectation "hybrid beats both" becomes a hypothesis to test, not an assumption.
11. Open. Delta (smallest NSE difference worth caring about) and the primary comparison: to be set by Joshua and Felix, then n from 8/d^2 with pilot sigma (0.27 hybrid-physics, 0.18 hybrid-XGBoost).
12. Open. Confirmatory basin draw: stratified by the same five aridity bands from the 665 non-pilot, non-dry basins, recorded seed, after item 11 is fixed.
13. 2026-10-11. Correction. The pilot selection script compared the CAMELS zero-flow share (a fraction) against 5 instead of 0.05, so the "dry on more than one day in twenty" rule removed no basin; the single basin dropped (03281100, Goose Creek, KY) was dropped because its zero-flow attribute is blank. Applied correctly the rule removes 85 basins and leaves 585. The five basins already run all have zero dry days. Script fixed. Decision on whether to redraw and rerun the pilot: pending (Joshua).
