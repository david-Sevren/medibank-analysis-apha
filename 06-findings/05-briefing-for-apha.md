# Finding 5: Briefing for APHA (27 Nov 2026)

The briefing is a Claude Doc: "Medibank contracting analysis: briefing for APHA" (https://claude.ai/artifact/WVPLPSQc4F9oKqGhePdvju). The version of record (rev 13) and a figure-by-figure source map are in `07-briefing/`.

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

## Sensitivity: surgical hospitals only (27 Nov 2026)

Question from David: the three iMH hospitals are mental health, so do the results change if the analysis is limited to surgical hospitals?

- Near-site tests (Finding 1) already used only the four surgical sites (East Sydney, Adeney, Macquarie/TOI, Western) as centres (`radius.py`, `funds_entrants.py`). The iMH hospitals were never centres in any headline figure. No change.
- Network and new-hospital figures (Finding 2) rerun on second-tier C to G only, all seven Medibank-interest hospitals still excluded (`analysis/briefing_surgical_only.py` -> `outputs/briefing/surgical_only_sensitivity.txt`). Conclusions hold:
  - Network Aug 2020 -> Oct 2026: Medibank 407 -> 406 (-1); Bupa +47; HCF +36; nib -3; HBF +6; Australian Unity -17.
  - New surgical hospitals open 12+ months: 75. Medibank 22 (29%), Bupa 43 (57%), HCF 34 (45%), nib 33 (44%).
  - Paired: Bupa 22 vs 1 (p < 0.001), HCF 14 vs 2 (p = 0.004), nib 14 vs 3 (p = 0.013).
  - Before 2023: 43% vs 44%. From 2023: 24% vs 51%. Permutation p = 0.009; every-split p = 0.048.
  - Six mental health / rehab openings dropped; Medibank matched Bupa, HCF and nib on all six.
  - 2026 surgical listings: Medibank 9 of 22 (41%) vs 24%.
