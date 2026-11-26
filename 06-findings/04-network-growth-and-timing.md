# Finding 4: Medibank's network growth vs other funds, and when it changed

Date: 27 Nov 2026
Data: `data/raw/agreements_by_fund_2020-2026.csv` (six funds, 27 quarters, Aug 2020 to Oct 2026)
Code: `analysis/network_growth.py`, `network_paired.py`, `timing.py`, `timing_break.py`, `build_audit_workbook.py`
Audit workbook: `outputs/medibank_network_audit.xlsx`, also loaded as a Claude Sheet ("Medibank network growth vs other funds (audit workbook)"). Every summary figure is a formula over hospital-level rows.

## The synopsis, tested

> David (27 Nov): there's no evidence Medibank isn't contracting in areas where it has hospitals, but it isn't growing its network compared with competing funds; everywhere it is very slow to engage in new contracts.

| Part of the statement | Verdict | Evidence |
|---|---|---|
| No evidence of different behaviour near Medibank's hospitals | **Holds** | Findings 1 to 3: terminations at the same rate near and far; near-site gap on new hospitals not significant on a fair test |
| Medibank isn't growing its network | **Holds** | 476 agreements in Aug 2020, 473 in Oct 2026 (-3). Bupa +59, HCF +40 |
| ...compared with competing funds | **Holds against Bupa and HCF; not against all** | nib -2, HBF +2, Australian Unity -32. The growth in the market is Bupa and HCF |
| Slow to contract new hospitals, everywhere | **Holds, and is the strongest point** | New hospitals listed 12+ months: Medibank has agreements with 31% (26 of 84); Bupa 58%, HCF 48%, nib 46%. Lowest of six for overnight surgical (41%) and day hospitals (27%) |
| ..."slow", rather than not engaging | **Understates it** | The gap persists for hospitals listed 2 years or more. Medibank gained 53 agreements with existing hospitals over six years against Bupa's 113 and HCF's 83 |

Suggested wording for Brett:

> Since 2020, Medibank's hospital network has not grown, while Bupa and HCF have added 59 and 40 agreements. Medibank is the slowest of the six funds examined to contract new private hospitals: of the 84 hospitals that opened since August 2020 and have been operating at least a year, Medibank has agreements with 26 (31%), against 49 for Bupa (58%), 40 for HCF (48%) and 39 for nib (46%). Head to head on the same hospitals, Bupa has agreements at 24 where Medibank has none; the reverse is true at one.

## Paired tests (same 84 hospitals)

| Comparator | Comparator yes, Medibank no | Medibank yes, comparator no | Exact McNemar p |
|---|---|---|---|
| Bupa | 24 | 1 | <0.001 |
| HCF | 16 | 2 | 0.001 |
| nib | 17 | 4 | 0.007 |
| HBF | 12 | 9 | 0.66 |
| Australian Unity | 10 | 7 | 0.63 |

Driven mostly by day hospitals (59 of the 84). On overnight surgical alone (17 hospitals) the direction is the same against every fund but no single comparison is significant.

## When did it change?

New hospitals grouped by year first listed; agreement status at Oct 2026 (so every fund's reporting batches have caught up).

| Year first listed | Hospitals | Medibank | Bupa / HCF / nib avg | Gap | Medibank agreement within 12 months |
|---|---|---|---|---|---|
| 2021 | 11 | 55% | 55% | 0 | 36% |
| 2022 | 11 | 27% | 30% | +3 | 27% |
| 2023 | 26 | 35% | 56% | +22 | 23% |
| 2024 | 17 | 29% | 47% | +18 | 12% |
| 2025 | 19 | 16% | 56% | +40 | 5% |
| 2026 | 25 | 36% | 21% | -15 | too recent |

- **Before 2023 Medibank kept pace; from 2023 it fell behind.** Listed before 2023: Medibank 41% vs 42%. Listed 2023 to 2025: 27% vs 54%. Exact permutation p = 0.007 for that split.
- **Medibank's own pace slowed steadily.** Share of new hospitals contracted within 12 months of listing: 36%, 27%, 23%, 12%, 5% for the 2021 to 2025 groups. (Medibank's dates are reliable for this: it reports changes every quarter, not in batches.)
- **Caution on the date.** 2023 was picked after seeing the table. Testing every possible split gives p = 0.08. The pre-2023 group is mostly day hospitals, so for overnight surgical hospitals there is too little before 2023 to time a change. Defensible wording: "from around 2023", not a precise date.
- **Possible reversal in 2026.** On hospitals first listed in 2026, Medibank currently leads (36% vs 21%), and its 9 agreements gained in Jul to Oct 2026 are its most in any half-year of the series. Too early to call; worth re-running in 6 months.

## Caveats

1. Agreement counts per hospital, not weighted by beds or activity.
2. Fund identity rests on the export's source; confirm against each fund's published agreement hospital list before publication.
3. Australian Unity's property trust owns Wyvern and Sunshine Private; not a neutral comparator for those two.
4. Reporting batches make "first shown with agreement" dates unreliable for Bupa, HBF, nib and Australian Unity; all cross-fund comparisons use Oct 2026 status.
