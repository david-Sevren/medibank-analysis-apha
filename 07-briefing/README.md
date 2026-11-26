# Briefing for APHA (27 Nov 2026)

The briefing prepared for Brett Heffernan, exported from the live Claude Doc ("Medibank contracting analysis: briefing for APHA", revision 13, https://claude.ai/artifact/WVPLPSQc4F9oKqGhePdvju) on 27 Nov 2026.

| File | What |
|---|---|
| `briefing-for-apha.md` | Markdown version (converted from the Word export, with the chart) |
| `briefing-for-apha.pdf` | PDF export, A4, as it reads in the doc |
| `briefing-for-apha.docx` | Word export |
| `finding2-new-hospitals-by-year.png` | Finding 2 chart. Data: `outputs/briefing/year_cohorts_chart_data.csv` |

If the live doc is edited, re-export it here so the repo copy stays the version of record.

## Rebuild every figure

From the repo root, Python 3 with pandas, numpy, openpyxl:

```
python3 analysis/clean_funds.py data/raw/agreements_by_fund_2020-2026.csv data/processed/panel_funds.csv
python3 analysis/briefing_figures.py data/processed/panel_funds.csv outputs
python3 analysis/briefing_esph.py data/processed/panel_funds.csv
python3 analysis/verify_briefing.py data/raw/agreements_by_fund_2020-2026.csv data/processed/panel_funds.csv
python3 analysis/build_audit_workbook.py data/processed/panel_funds.csv outputs
```

All Finding 2 comparisons leave out Medibank's seven part-owned hospitals (provider numbers 0017500W, 0037140T, 0017360L, 0065780W, 0095140A, 0015550A, 0056310K). "New hospitals" means first listed after Aug 2020, still listed Oct 2026, and listed for at least 12 months.

## Figure map

Every number in the briefing, and where it comes from.

### What we tested

| Briefing figure | Source |
|---|---|
| 27 quarterly snapshots, 1 Aug 2020 to 1 Oct 2026; 649 hospitals at latest date | `data/processed/panel_funds.csv` |
| Medibank rows match the Medibank-only export on 17,032 of 17,032 records; 100 zero-length records removed | `06-findings/03-new-hospitals-vs-other-funds.md`; evidence E1 vs E3 (`evidence/README.md`) |
| Independent recount from the raw file | `outputs/briefing/verification_log.txt` section 4 (`analysis/verify_briefing.py`, csv module only, no shared code) |

### Finding 1: no sign of steering through contracting

| Briefing figure | Source |
|---|---|
| Terminations within 50 km of a Medibank surgical site vs elsewhere: Medibank 4.3 vs 4.6 per 100, HCF 4.1 vs 4.9 | `outputs/fund_losses_50km.csv` |
| 16 of Medibank's 32 terminations (50%) within 50 km of a surgical site, where 51.5% of hospitals are | `06-findings/01-regional-contracting.md`; `outputs/all_status_changes.csv` |
| Overnight surgical (C to F) within 50 km at Oct 2026: 89% to 100% (East Sydney 89.3%, Macquarie 90.0%, Adeney 92.5%, Western 100%); national 86.7% | `outputs/radius_results_CDEF.csv` (area 50 km, filter relevant, column xsec_end); `outputs/national_trend_CDEF.csv` |
| 9 overnight surgical agreements ended nationally; 3 near sites (Northern Beaches public takeover Apr 2026, two likely artefacts) | `06-findings/02-regional-contracting-surgical-only.md`; `outputs/events_within_50km_CDEF.csv` |
| East Sydney 30 km: 100 of 123 (81.3%) Aug 2020 to 98 of 123 (79.7%) Jul 2025 | `outputs/briefing/esph_30km.txt` (`analysis/briefing_esph.py`; cross-section, East Sydney and the other Medibank sites excluded; reproduces on both E1 and E3) |
| Placebo: 15% to 93% of placebo areas did as badly or worse | `outputs/placebo.csv`, surgical sites at 50 km (Western 15%, East Sydney 30%, Macquarie 41% and 45%, Adeney 65% and 93%) |
| New surgical hospitals within 25 km: Medibank 1 of 5, Bupa/HCF/nib 93%; permutation p = 0.11 | `outputs/fund_permutation_robust.csv` (radius 25) |

### Finding 2: Medibank has not kept pace since around 2023

| Briefing figure | Source |
|---|---|
| Network counts Aug 2020 to Oct 2026 (Bupa 480 to 535, HCF 459 to 495, HBF 512 to 514, Medibank 472 to 468, nib 535 to 531, Australian Unity 523 to 491) | `outputs/briefing/network_counts.csv` |
| 81 new hospitals; Medibank 25 (31%), Bupa 46 (57%), HCF 37 (46%), nib 37 (46%) | `outputs/briefing/new_hospitals_81.csv` (one row per hospital), `outputs/briefing/new_hospitals_by_type.csv` |
| Same-hospital comparison: Bupa 22 vs 1, HCF 14 vs 2, nib 15 vs 3; exact McNemar p | `outputs/briefing/paired_tests.csv` |
| Before 2023: 41% vs 42% (22 hospitals). From 2023: 27% vs 52% (59 hospitals). p = 0.009; every-start-date p = 0.039 | `outputs/briefing_figures.txt`; chart data `outputs/briefing/year_cohorts_chart_data.csv` |
| Overnight surgical 6 of 16 (38%) vs 62% to 75%; day 16 of 59 (27%) vs 39% to 53% | `outputs/briefing/new_hospitals_by_type.csv` |
| HBF and Australian Unity 35% each; match on 96% of hospital-quarters outside WA, 84% in WA (nib matches HBF 95% outside WA) | `outputs/briefing/new_hospitals_by_type.csv`; `outputs/briefing/verification_log.txt` section 1 |

### Concerns not yet substantiated

| Briefing figure | Source |
|---|---|
| Wyvern (13.5 km from Macquarie), Northern Private (17.6 km from Adeney), Monash Heart (14 km from Adeney), Southern Sydney Private (21 km from East Sydney): no Medibank agreement | `outputs/fund_near_entrants_25km.csv` |
| No Medibank agreement at Deakin or Nundah; Adeney from Jul 2026 | `outputs/briefing/medibank_sites_status_oct2026.csv`; first-agreement dates in the New hospitals sheet of `outputs/medibank_network_audit.xlsx` |
| Oncology and infusion units: Medibank 6 of 11, Bupa/HCF/nib 11; without them 27% vs 37% to 50% | `outputs/briefing_figures.txt`; flag column `oncology_infusion` in `outputs/briefing/new_hospitals_81.csv` |
| 2026 listings: Medibank 9 of 25 (36%) vs Bupa/HCF/nib average 21% | `outputs/briefing/cohort_2026_under_12_months.csv` |

### What Medibank will challenge

| Briefing figure | Source |
|---|---|
| Reporting batches: Bupa +66 Jul 2024, nib +46 Jul 2025 | `06-findings/03-new-hospitals-vs-other-funds.md`; `outputs/timing_status_events.csv` |
| 59 of the 81 new hospitals are day hospitals | `outputs/briefing/new_hospitals_by_type.csv` |
| Only 2 new provider numbers are re-declarations of an existing site; neither affects the gap | `outputs/verify_redeclarations.csv` |

## Audit workbook

`outputs/medibank_network_audit.xlsx`: hospital-level sheets with every summary figure as a formula. Medibank's seven hospitals are flagged in the last column of each sheet and excluded from the Summary, so it matches the briefing (25 of 81). Recalculated in LibreOffice on 27 Nov 2026 with no formula errors.
