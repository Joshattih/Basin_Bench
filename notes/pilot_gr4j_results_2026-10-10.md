# Pilot run 1: GR4J alone on the five pilot basins (2026-10-10)

Setup: Maurer forcing, Oudin evaporation, warm-up 1989, calibrate 1990-1999 on NSE
(differential evolution, seed 533), score 2000-2008 untouched. No snow module.

| gauge | river | snow share | NSE train | NSE test |
|---|---|---|---|---|
| 01031500 | Piscataquis, ME | 0.29 | 0.44 | 0.49 |
| 01557500 | Bald Eagle Creek, PA | 0.16 | 0.52 | 0.63 |
| 05408000 | Kickapoo, WI | 0.14 | 0.50 | 0.74 |
| 10348850 | Galena Creek, NV | 0.83 | 0.31 | -0.86 |
| 06154410 | Little Peoples Creek, MT | 0.20 | 0.53 | 0.75 |

What the pilot shows:
1. The chain runs end to end; no missing flow days in any test period.
2. The two snowiest basins score worst; the 83%-snow basin goes negative on test and its
   exchange parameter hit the bound (-5 mm/day). GR4J without a snow module is not a fair
   physics arm on snowy basins. Decision needed: add CemaNeige, or restrict to low-snow basins.
3. NSE across basins already shows the long lower tail (-0.86 to 0.75 in five basins).
   The analysis plan must not rely on a mean of raw NSE; use paired differences with a
   bootstrap CI alongside the paired t, or a bounded transform, stated in advance.
4. Train NSE below test NSE in four of five basins: the 1990s were harder years than the 2000s
   here, not a sign of leakage. Worth one sentence under statistical validity.
Raw output: notes/pilot_gr4j_run1.txt
