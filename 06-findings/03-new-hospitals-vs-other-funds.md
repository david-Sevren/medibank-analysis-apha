# Finding 3: Is Medibank slower than other funds to contract new hospitals near its sites?

Date: 27 Nov 2026 (rewritten on the full CSV export; supersedes the earlier truncated-file version)
Data: `data/raw/agreements_by_fund_2020-2026.csv` (David, 27 Nov 2026). 102,792 rows; 27 quarterly snapshots, 1 Aug 2020 to 1 Oct 2026; six funds: Medibank (MBP), Bupa (BUP), HCF, nib (NIB), HBF, Australian Unity (AUF, standing in for the AHSA group)
Code: `analysis/clean_funds.py`, `funds_entrants.py`, `funds_oddone.py`, `funds_permutation.py`, `funds_permutation_robust.py`
Outputs: `outputs/fund_entrants_{25,50,100}km.csv`, `fund_near_entrants_*km.csv`, `fund_losses_*km.csv`, `fund_permutation_*.csv`, `fund_permutation_robust.csv`

## Short answer

**Medibank is slower than its competitors at contracting new overnight surgical hospitals, but the data doesn't show that this is specific to areas near its own hospitals.**

- Among 13 comparable new overnight surgical hospitals (listed at least six months, excluding hospices and birth centres), Medibank has agreements with **5**. Bupa, HCF and nib average **86%**.
- Four of the eight Medibank hasn't contracted are within 25 km of a Medibank site: **Wyvern Private, Northern Private, Monash Heart Private and Southern Sydney Private.** Bupa and nib have agreements with all four; HCF with three.
- But Medibank is also missing at three comparable new hospitals nowhere near its sites: **King Street Private and Ramsay Surgical Centre Charlestown (Newcastle) and Victoria Street Private (Wollongong).**
- On comparable hospitals, the near-site gap is in the expected direction (+48 points at 25 km) but **not statistically significant** (exact permutation p = 0.11), and it disappears at 50 km.
- Medibank terminates existing agreements at the **same rate** near its sites as elsewhere (4.3 vs 4.6 per 100 hospitals), and the same as HCF.

For Brett: there is a real, checkable story that **Medibank lags the market in contracting new private hospitals**, which narrows member choice. The four hospitals near Medibank's sites are worth asking about. But the data alone doesn't support "Medibank withholds agreements to protect its own hospitals", and Medibank could point to Newcastle and Wollongong to say so.

## Data checks

| Check | Result |
|---|---|
| Completeness | All 27 snapshots present for all six funds with identical hospital counts (608 to 649) |
| Medibank identity | MBP rows match the separate Medibank-only file on **17,032 of 17,032** rows |
| Funds distinct | Each fund differs from the others on 11 to 14% of rows; no duplication |
| Reporting batches | Funds load changes in batches: Bupa +66 in Jul 2024; HBF +37 Apr 2023 and +26 Apr 2026; Australian Unity +32 Jan 2025; **nib +46 in Jul 2025 after nothing for five years.** "When" a fund signed is unreliable; all comparisons use status at **Oct 2026** |
| Australian Unity | Conflicted: its property trust owns Wyvern Private and Sunshine Private. Main comparison uses Bupa, HCF and nib. Results hold with any comparator set |
| Fund codes | File uses MBP and AUF (not MVP and AUH) |

## Result 1: all new overnight surgical hospitals (C to F), status Oct 2026

"Near" = within R km of a Medibank surgical site and first listed after Medibank took its interest there.

| Distance | | Hospitals | Medibank | Bupa | HCF | nib | HBF | Aus Unity |
|---|---|---|---|---|---|---|---|---|
| 25 km | near | 5 | **20%** | 100% | 80% | 100% | 80% | 80% |
| | elsewhere | 17 | 47% | 47% | 41% | 35% | 41% | 53% |
| 50 km | near | 8 | **50%** | 100% | 88% | 100% | 88% | 88% |
| | elsewhere | 14 | 36% | 36% | 29% | 21% | 29% | 43% |
| 100 km | near | 10 | **40%** | 90% | 80% | 80% | 80% | 70% |
| | elsewhere | 12 | 42% | 33% | 25% | 25% | 25% | 50% |

On this set, the near-site gap (competitor share minus Medibank, near vs elsewhere) is large and looks significant: +79 pts at 25 km (exact permutation p = 0.011), +53 at 50 km (p = 0.048), +57 at 100 km (p = 0.027).

**But the "elsewhere" group flatters the comparison.** It includes hospices, a birth centre and hospitals listed only in the last quarter or two, which few funds contract yet. Those pull the elsewhere gap toward zero.

## Result 2: comparable hospitals only (the fair test)

Listed at least six months before Oct 2026; hospices and birth centres excluded; comparators Bupa, HCF, nib.

| Hospital | Location | Near (25 km) | Medibank | Bupa / HCF / nib |
|---|---|---|---|---|
| Wyvern Private Hospital | Terrey Hills NSW | Yes (13.5 km from TOI) | No | Yes / Yes / Yes |
| Northern Private Hospital (Ramsay) | Epping VIC | Yes (17.6 km from Adeney) | No | Yes / Yes / Yes |
| Monash Heart Private | Clayton VIC | Yes (14.1 km from Adeney) | No | Yes / Yes / Yes |
| Southern Sydney Private Hospital | Kogarah area NSW | Yes (20.8 km from ESPH) | No | Yes / No / Yes |
| Eastwood Private Hospital | Adelaide SA | Yes (near Western) | **Yes** | Yes / Yes / Yes |
| King Street Private Hospital | Newcastle NSW | No | No | Yes / Yes / Yes |
| Ramsay Surgical Centre Charlestown | Newcastle NSW | No | No | Yes / Yes / Yes |
| Victoria Street Private Hospital | Wollongong NSW | No | No | Yes / Yes / No |
| Somerset Private Hospital | Kingswood NSW | No at 25 km | Yes | Yes / Yes / Yes |
| Camden Surgical Hospital | Camden NSW | No at 25 km | Yes | Yes / Yes / Yes |
| The George Centre | Gregory Hills NSW | No at 25 km | Yes | Yes / Yes / Yes |
| Herston Private Hospital | Brisbane QLD | No | Yes | Yes / No / No |
| Toowoomba Private Day Hospital | Toowoomba QLD | No | No | No / No / No |

| Distance | Near n | Elsewhere n | Medibank near | Others near | Medibank elsewhere | Others elsewhere | Near-site gap | Exact p |
|---|---|---|---|---|---|---|---|---|
| 25 km | 5 | 8 | 20% | 93% | 50% | 75% | +48 pts | 0.11 |
| 50 km | 8 | 5 | 50% | 96% | 20% | 60% | +6 pts | 0.51 |
| 100 km | 9 | 4 | 44% | 93% | 25% | 58% | +15 pts | 0.38 |

## Result 3: terminations by fund (existing hospitals, Aug 2020 to Oct 2026, within 50 km)

| Fund | Lost per 100 hospitals, near | Elsewhere |
|---|---|---|
| Medibank | 4.3 | 4.6 |
| HCF | 4.1 | 4.9 |
| Bupa | 1.4 | 2.9 |
| nib | 1.1 | 1.7 |
| HBF | 1.9 | 1.7 |
| Australian Unity | 6.8 | 4.0 |

Medibank is no more likely to drop a hospital near its sites. (Australian Unity's higher near-site rate is outside this brief but notable.)

## Other facts that matter

- **Other funds contract with Adeney.** At Oct 2026, Bupa, HCF, HBF and Australian Unity all have agreements with Adeney; nib doesn't. That cuts against any framing of Adeney as a Medibank-only hospital.
- **Northern Private is a Ramsay hospital.** Medibank has a long-standing group agreement with Ramsay, but has not added Northern Private 32 months after it opened, while Bupa, HCF and nib did. Ramsay can say why.
- **Wyvern is the closest service match**: spinal, neuro and orthopaedic surgery 13.5 km from The Orthopaedic Institute. 22 months open, every other major fund contracted, Medibank not.

## What this means for the brief

1. **Drop "Medibank withholds contracts near its own hospitals" as a data claim.** The direction is right but it doesn't survive a fair comparison, and Newcastle and Wollongong give Medibank an easy rebuttal.
2. **Keep "Medibank lags the market on new hospitals".** It is consistent across sites and comparators, and it bears on member access. It needs Medibank's side.
3. **The four near-site hospitals are the qualitative lead.** Ask Wyvern, Ramsay (Northern Private), Monash Health (Monash Heart) and Southern Sydney Private: did they seek a Medibank agreement, what were they offered, and who walked away? If any were told Medibank already has capacity nearby, or were offered materially worse terms than Medibank-interest hospitals, that is the evidence the data can't give.
