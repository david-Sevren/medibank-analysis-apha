# Medibank hospital ownership register

Last updated: 24 Nov 2026
Status: draft for David's review. Items marked `TO VERIFY` have not been confirmed against a primary source.

## Headline

Medibank (through Medibank Health Solutions Pty Ltd / Amplar Health) holds ownership interests in **seven declared private hospitals** across **five equity-accounted vehicles**. The anchor source is Medibank's FY26 Annual Report, Note 16(c), which lists exactly five equity-accounted investments, all described as "short stay hospital":

| Vehicle (legal entity, per Note 16(c)) | Type | Medibank interest FY26 | FY25 |
|---|---|---|---|
| East Sydney Day Hospital Pty Ltd | Associate | 49.2% | 49.0% |
| Adeney Private Hospital Pty Ltd | Associate | 49.0% | 49.0% |
| SydOrtho Holdings Pty Ltd | Joint venture | 50.0% | 50.0% |
| Integrated Mental Health Pty Ltd (iMH) | Joint venture | 50.0% | 50.0% |
| Western Adelaide Private Hospital Pty Ltd | Associate | 49.0% | 49.0% |

iMH runs three hospitals, so five vehicles map to seven facilities.

None is a controlled subsidiary. In every case Medibank is a minority or 50/50 partner alongside doctors or an operator. That matters for framing: Medibank will say it has "no involvement in clinical care decisions" (its own words on Western Hospital). Our case has to rest on what Medibank does as **funder**, not as owner.

## Register

### Surgical / short stay

| # | Hospital | Address | Provider no. | Medibank interest | Partner(s) | Interest taken | Opened under JV | Size | LGA |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **East Sydney Private Hospital** | 75-85 Crown St, Woolloomooloo (East Sydney) NSW 2010/2011 | 0017500W | 49.2% (East Sydney Day Hospital Pty Ltd) | Founding doctors | Aug 2020 (announced ~17-19 Aug 2020) | Existing hospital | 32 beds, 5 theatres at 2020; NSW licence lists 40 beds; 7 theatres after 2024 expansion | City of Sydney |
| 2 | **Adeney Private Hospital** | 209 Cotham Rd, Kew VIC 3101 | 0037140T | 49.0% (Adeney Private Hospital Pty Ltd) | ~42-45 specialists (trust), led by Prof Michael Grigg | JV announced Mar 2021 | Declared 10 Feb 2025; first patients 4 Mar 2025 | 60 beds, 5 theatres | City of Boroondara |
| 3 | **The Orthopaedic Institute** at Macquarie University Hospital | Macquarie University Hospital, North Ryde/Macquarie Park NSW | Operates within MUH (0017360L); no separate provider number found | 50.0% (SydOrtho Holdings Pty Ltd) | Orthopaedic surgeons (SydOrtho); floor space from MQ Health | JV announced Sep 2022 | Opened ~2024 `TO VERIFY` | 29 beds, 4 theatres | City of Ryde |
| 4 | **Western Hospital** (Western Adelaide Private Hospital) | 168 Cudmore Tce, Henley Beach SA 5022 | 0065780W (revoked and re-declared 1 Nov 2024 under new operator) | 49.0% (Western Adelaide Private Hospital Pty Ltd) | 11-member doctor group (Seabreeze Healthcare) | 1 Nov 2024 (out of administration) | Existing hospital, converted to short stay | 24 beds, 4 theatres post conversion | City of Charles Sturt |

### Mental health (iMH, 50/50 with Aurora Healthcare)

| # | Hospital | Address | Provider no. | Interest taken / opened | Beds | LGA |
|---|---|---|---|---|---|---|
| 5 | **Deakin Private Hospital** | Cnr Strickland Cres and Denison St, Deakin ACT 2600 | 0095140A `TO VERIFY` (parsed from PHI 17/23) | Declared 3 Mar 2023 (new build) | 52 | ACT (no LGAs; use SA3 Woden Valley / Inner South `TO VERIFY`) |
| 6 | **iMH Hirondelle Private Hospital** | 10 Wyvern Ave, Chatswood NSW 2067 | 0015550A | Aurora contributed existing hospital to iMH (JV Mar 2023); reopened as iMH mental health Jan 2024 | 45 | Willoughby |
| 7 | **iMH Nundah Private Hospital** | 20 Nellie St, Nundah QLD 4012 | 0056310K | Declared 23 Nov 2024; opened Jan 2025 | 58 | City of Brisbane |

## What this means for the contracting analysis

**Event dates differ by hospital.** Each one gives us its own before and after window:

| Catchment | Event date for analysis | Before window available? |
|---|---|---|
| Inner/East Sydney (ESPH) | Aug 2020 | Depends on agreement-list history pre-2020. EHA data structure changed late 2021 |
| Ryde / North Shore (TOI) | Sep 2022 (announced) or ~2024 (opened) | Yes |
| Kew / inner east Melbourne (Adeney) | Mar 2021 (announced) or Mar 2025 (opened) | Yes |
| Western Adelaide (Western) | Nov 2024 | Yes, but short "after" window |
| Mental health catchments (Deakin, Hirondelle, Nundah) | Mar 2023, Jan 2024, Jan 2025 | Yes |

**The surgical four are the priority.** Mental health is a separate contracting market (psychiatric beds, different hospital set), so test it separately or park it.

**TOI is a special case.** It sits inside Macquarie University Hospital, which is owned by Macquarie University. Medibank contracts with MUH, not with TOI. Any "Medibank has no agreement with its own hospital" claim cannot use TOI cleanly.

**Two dates per site.** For Adeney and TOI the announcement came years before opening. Contracting behaviour could shift at either point, so test both.

## Looks like ownership, but isn't (exclude from the register)

| Item | Why it's excluded |
|---|---|
| **No Gap partner hospitals** (e.g. Healthe Care sites, Vermont Private, Westside Private, South Perth, Stirling, Lingard, Buderim, St John of God Murdoch, MUH itself) | Commercial no-gap partnerships, no equity. Relevant to claim 6, not to ownership |
| **Amplar Health Home Hospital / My Home Hospital (SA)** | Hospital-in-the-home for SA Health public patients. Was a Calvary JV; Calvary exited and Amplar is moving to sole ownership (Calvary exit announced Nov 2024; Minister's consent reported Feb 2026). Not a private hospital competing for insured surgical volume. Note it, don't analyse it |
| **Transition Care Service** (Pullman Adelaide; College Grove, Walkerville) | SA Health collaboration for step-down patients, not a declared private hospital |
| **Myhealth Medical Group** (90%) and **Better Medical** (100%) | GP and primary care clinics, not hospitals. But relevant later: GP referral pathways could feed Medibank-interest hospitals |
| **Cura Day Hospitals Group** | Reported Medibank buy-in talks in Feb 2022; Fresenius/Cura publicly denied it. No investment |
| **iMH Alexandria (NSW)** | Planned 56-bed greenfield mental health hospital (announced Mar 2023, targeted 2025/2026). No evidence it has opened `TO VERIFY` |
| **Centuria / CPP** | Owns the Adeney building (20-year lease). Property landlord, unrelated to Medibank |

## Open questions for David

1. You said you know of others. Anything not on this list? The FY26 Note 16(c) lists only five vehicles, so anything else would have to be (a) held outside Medibank Health Solutions, (b) acquired after 30 June 2026, or (c) a non-equity arrangement that behaves like ownership.
2. ESPH address: some sources say Woolloomooloo 2011, NSW licence says East Sydney 2010. Same site; we'll use the NSW licence for LGA mapping.
3. TOI opening date and whether it has any separate HCP reporting identity.
4. Deakin provider number to confirm against the current Commonwealth declared hospitals list.
