# Finding 3: Is Medibank slower than other funds to contract new hospitals near its sites?

Date: 27 Nov 2026
Data: `data/raw/agreements_by_fund_2020-2026.xlsx` (David, 27 Nov 2026). Six funds: Medibank (MBP), Bupa (BUP), HCF, nib (NIB), HBF, Australian Unity (AUF, standing in for the AHSA group)
Code: `analysis/clean_funds.py`, `analysis/funds_entrants.py`, `analysis/funds_oddone.py`
Outputs: `outputs/fund_entrants_{25,50,100}km.csv`, `fund_entrants_did_50km.csv`, `fund_near_entrants_50km.csv`, `fund_odd_one_out.csv`, `fund_losses_50km.csv`

## Short answer

**Yes, for overnight surgical hospitals, and the closer to a Medibank site the clearer it gets.** Within 25 km of a Medibank part-owned surgical hospital, five new overnight surgical hospitals opened after Medibank took its interest. By June 2025 **Medibank had contracted none of them; Bupa had contracted four and HCF three.** Further away, Medibank contracted new hospitals at the same rate or better than its competitors. As of October 2026, Medibank still has no agreement with any of the four that remain listed.

This is the first pattern in the analysis that points Brett's way. It is small (five to eight hospitals), the data has gaps (below), and each hospital has possible innocent explanations. It is a strong lead to take to those hospitals, not yet a finding to publish.

There is **no** such pattern for day hospitals, and **no** difference in terminations: Medibank drops existing agreements near its sites at the same rate as HCF and at the same rate as elsewhere.

## Data limits (read first)

| Issue | Effect |
|---|---|
| **Export truncated at 80,000 rows** (Excel limit; file says to use CSV) | Complete for all six funds from Aug 2020 to **Jun 2025** only. Jul 2025 to Oct 2026 missing. Medibank's later status comes from the Medibank-only file. **Need CSV re-export** |
| **Fund codes** | File uses MBP (not MVP) and AUF (not AUH). Assumed Medibank and Australian Unity |
| **Batch reporting** | Bupa's agreements mostly appear in one batch in Jul 2024, Australian Unity's in Apr 2025. "When" a fund signed is unreliable; "whether" at a date is the safer measure. All comparisons below use status at a point in time |
| **nib** | Records **zero** new agreements in five years. Not plausible; nib's data looks frozen at source. Excluded from comparisons |
| **HBF** | WA-focused; few east-coast agreements. Excluded from comparisons |
| **Australian Unity is conflicted** | Its Healthcare Property Trust owns Wyvern Private and Sunshine Private, and its fund contracted both. Robust comparison is **Bupa and HCF only** |
| **Identity checks** | MBP rows match the earlier Medibank file 100% (13,224 rows). Each fund differs from the others on 11 to 14% of rows, so no fund duplicated another. No external proof of identity yet |

## Result: new overnight surgical hospitals (second-tier C to F)

Share with an agreement at June 2025, among new hospitals still listed. "Near" means first listed after Medibank took its interest in the nearest site.

| Distance | | Hospitals | Medibank | Bupa | HCF | Aus Unity |
|---|---|---|---|---|---|---|
| **Within 25 km** | near | 5 | **0%** | 80% | 60% | 60% |
| | elsewhere | 10 | 60% | 50% | 60% | 50% |
| **Within 50 km** | near | 8 | **38%** | 88% | 75% | 75% |
| | elsewhere | 7 | 43% | 29% | 43% | 29% |
| **Within 100 km** | near | 10 | **40%** | 70% | 70% | 70% |
| | elsewhere | 5 | 40% | 40% | 40% | 20% |

At 50 km, Medibank is the **only** fund without an agreement while at least two of Bupa, HCF and Australian Unity have one at 4 of 8 new surgical hospitals near its sites, against 0 of 7 elsewhere (one-sided Fisher exact p = 0.051). There is no hospital, near or far, where Medibank has an agreement and none of the others do.

## The hospitals

| Hospital | Opened | Type | Near | Medibank | Bupa | HCF | Aus Unity | Medibank Oct 2026 |
|---|---|---|---|---|---|---|---|---|
| **Wyvern Private Hospital**, Terrey Hills | Dec 2024 | 85-bed surgical and rehab: spinal, neuro, orthopaedic | 13.5 km from TOI | No | Yes | Yes | No | **No** |
| **Northern Private Hospital**, Epping (Ramsay) | Feb 2024 | 70 beds, 4 theatres, cath lab, medical, surgical, mental health | 17.6 km from Adeney | No | Yes | Yes | Yes | **No** |
| **Monash Heart Private** (Jessie McPherson), Clayton | Apr 2023 | Cardiac | 14.1 km from Adeney | No | Yes | Yes | Yes | **No** |
| **Sunshine Private Hospital**, St Albans | Mar 2023 | 75 beds, general and women's | 21.0 km from Adeney | No | Yes | Had, then lost | Yes | Left list Jul 2025 |
| Southern Sydney Private Hospital | Jun 2025 | Overnight surgical | 20.8 km from ESPH | No | No | No | No | No |
| Somerset Private Hospital | Jan 2022 | Overnight surgical | 47.9 km from ESPH | Yes | Yes | Yes | Yes | Yes |
| Camden Surgical Hospital | Apr 2023 | Overnight surgical | 48.3 km from TOI | Yes | Yes | Yes | Yes | Yes |
| The George Centre | Oct 2023 | Overnight | 42.4 km from TOI | Yes | Yes | Yes | Yes | Yes |

The three Medibank did contract are all 40 to 50 km out in outer south-west Sydney. The four it didn't are 13 to 21 km from Adeney or TOI.

## Possible innocent explanations (to test, not to assume)

1. **Service overlap.** Monash Heart is cardiac; Adeney doesn't do cardiac. Northern Private is a broad medical and surgical hospital in a different part of Melbourne. Wyvern is the closest match: orthopaedic and spinal surgery 13.5 km from The Orthopaedic Institute.
2. **Price or volume.** Medibank may have offered terms the hospitals refused. Only the hospitals can say who walked away.
3. **Data lag.** Medibank's recorded agreements may lag signing, as Bupa's and Australian Unity's clearly do. But Medibank still shows no agreement in Oct 2026, 20 to 43 months after these hospitals opened, and its own lag for new hospitals that it did contract was a median of 9 months.
4. **Ramsay group deal.** Northern Private is Ramsay. If Medibank's Ramsay agreement covers named hospitals only, adding a new one is a negotiation; but Bupa and HCF did add it.
5. **Public-hospital-linked sites.** Monash Heart and Northern Private are co-located with public hospitals; some funds treat these differently.

## Termination rates by fund (existing hospitals, Aug 2020 to Jun 2025)

| Fund | Near: lost per 100 hospitals | Elsewhere |
|---|---|---|
| Medibank | 3.0 | 3.4 |
| HCF | 3.0 | 3.4 |
| Bupa | 1.4 | 2.8 |
| Australian Unity | 1.4 | 1.5 |

Medibank terminates at the same rate near its sites as elsewhere, and the same as HCF. Consistent with Findings 1 and 2.

## What to do with this

1. **Re-export as CSV** to cover Jul 2025 to Oct 2026 for all funds, then rerun (`clean_funds.py` drops incomplete snapshots automatically).
2. **Ask the four hospitals directly** (Wyvern, Northern Private/Ramsay, Monash Health for Monash Heart, and Unitas or the receivers for Sunshine): did you seek a Medibank agreement, when, what was offered, and why didn't it land? Correspondence would be the smoking gun or the rebuttal.
3. **Get service-line data** so overlap with each Medibank site can be measured, not assumed.
4. **Fix or explain nib's data** before using it as a comparator.
