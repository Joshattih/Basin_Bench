# Pilot basins, chosen 2026-10-10, before any daily record was opened

Purpose: the exploration the M1 handout asks for ("explore before you commit").
These five basins inform design only. They are excluded from the confirmatory
experiment of Milestones 2 and 3.

Rule (scripts/select_pilot_basins.py, seed 533):
1. All 671 CAMELS basins, with aridity (evaporation demand / rain) from camels_clim.txt
   and share of zero-flow days from camels_hydro.txt.
2. Drop basins dry on more than 5% of days (1 basin dropped, 670 remain).
3. Sort by aridity, cut into five equal bands.
4. Draw one basin at random from each band.

Result:

| gauge_id | name | band | aridity | rain mm/day | snow share |
|---|---|---|---|---|---|
| 01031500 | Piscataquis River near Dover-Foxcroft, Maine | very wet | 0.59 | 3.52 | 0.29 |
| 01557500 | Bald Eagle Creek at Tyrone, PA | wet | 0.75 | 3.15 | 0.16 |
| 05408000 | Kickapoo River at La Farge, WI | middle | 0.89 | 2.49 | 0.14 |
| 10348850 | Galena Creek at Galena Creek State Park, NV | dry | 1.18 | 2.51 | 0.83 |
| 06154410 | Little Peoples Creek near Hays, MT | very dry | 1.60 | 1.29 | 0.20 |

What the pilot must tell us:
1. The shape of NSE across basins (bunched or long-tailed), which decides the test.
2. The spread of the per-basin difference between models, the sigma for the power calculation.
3. That the whole chain runs end to end.

Data source: CAMELS v1.2, Addor et al. 2017, DOI 10.5065/D6MW2F4D, Zenodo record 15529996, CC BY 4.0.
