# Finding 5: Briefing for APHA (27 Nov 2026)

The briefing is a Claude Doc: "Medibank contracting analysis: briefing for APHA" (https://claude.ai/artifact/WVPLPSQc4F9oKqGhePdvju).

Every figure in it is reproduced by:
- `analysis/briefing_figures.py` -> `outputs/briefing_figures.txt` (all comparisons exclude the seven Medibank-interest hospitals)
- `analysis/verify_briefing.py` (HBF/Australian Unity alignment, state mix of new hospitals, re-declaration check, independent recount from the raw CSV, list of Bupa-yes/Medibank-no hospitals)
- Finding 1 figures: `outputs/fund_losses_50km.csv`, `outputs/radius_results_CDEF.csv`, `outputs/placebo.csv`

Corrections made during verification:
- Headline new-hospital figures now exclude Medibank's own part-owned hospitals (Deakin and Nundah had been counted against Medibank): 25 of 81, not 26 of 84.
- With that exclusion the 2023 break survives the every-start-date test (p = 0.039; was 0.08).
- East Sydney 30 km figure now excludes the other Medibank-interest hospitals: 100 of 123 (81.3%) to 98 of 123 (79.7%).
- The change dates from hospitals first listed in 2023, not 2022 (2022 cohort shows no gap).
- Surgical coverage near sites at Oct 2026 is 89% to 100% (cross-section), not 90% to 100%.

Checks that came back clean:
- Only 2 "new" hospitals are re-declarations of an existing site (Boroondara Day Surgery, Paso Infusion Centre); all four main funds contract both, so they don't affect the gap.
- HBF and Australian Unity match on 95.6% of hospital-quarters outside WA, 83.9% in WA: consistent with HBF contracting through the AHSA outside WA (nib also matches HBF on 94.8% outside WA, so this is supportive, not proof).
- 77 of the 84 new hospitals (incl. Medibank sites) are outside WA.
