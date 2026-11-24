# Method: did Medibank's contracting change around its hospital interests?

Status: draft for discussion, 24 Nov 2026

## The hypothesis

After Medibank takes an ownership interest in a hospital, it becomes less willing to hold agreements with *competing* hospitals in the same catchment, because every member who can't use a competitor is a member who may end up at the Medibank-interest hospital.

If this is true we should see, in Medibank-interest catchments and after the event date:

1. Medibank agreement coverage of nearby competing hospitals falls, **and**
2. it falls by more than Bupa, HCF and nib coverage of the same hospitals, **and**
3. it falls by more than Medibank's own coverage in comparable catchments with no Medibank interest.

All three are needed. (1) alone is what sank the August 2025 release: it can be explained by closures, industry-wide disputes or data errors. (2) and (3) are what turn a number into evidence.

## Design: difference-in-differences

| | Before event | After event |
|---|---|---|
| Medibank, treated catchment | A | B |
| Other funds, treated catchment | C | D |
| Medibank, control catchment | E | F |

The effect we're testing is roughly (B - A) minus (D - C), cross-checked against (B - A) minus (F - E).

## Decisions to make

**1. Unit of analysis.** Hospital x fund x snapshot date, with agreement status as yes / no / interim / Members' Choice tier. Medibank can hurt a competitor without terminating: dropping it from Members' Choice, or leaving it on an interim contract, may matter as much as an outright termination. We should capture tier as well as yes/no if the data allows.

**2. Catchment definition.** Three options, and we should run at least two to show the result isn't an artefact of the boundary:
- LGA of the Medibank-interest hospital plus adjacent LGAs (closest to what APHA used in 2025: "adjacent local areas")
- Drive-time radius (e.g. 20 and 40 minutes)
- Specialty overlap: only competitors that do the same work (orthopaedics, general surgery, endoscopy for the surgical sites; psychiatry for iMH)

**3. Event date.** Announcement or opening? For Adeney (Mar 2021 vs Mar 2025) and TOI (Sep 2022 vs ~2024) these are years apart. Test both.

**4. Control catchments.** Comparable metro areas with similar private hospital density and no Medibank interest. Candidates to discuss: e.g. Melbourne south-east, Sydney south-west, Brisbane south, Adelaide east.

**5. Metric.** Report both counts (hospitals with an agreement / hospitals in catchment) and a size-weighted version (beds or theatres), so a lost small day hospital doesn't look the same as a lost major hospital.

## Data sources

| Source | What it gives | Concerns |
|---|---|---|
| privatehealth.gov.au insurer "Agreement Hospitals" lists | Current agreement status by fund | Point in time only. Need history |
| EHA / ROADS historical agreement files | Snapshot history | **File structure changed late 2021; this caused the Aug 2025 error.** Must be re-mapped and validated before use |
| Wayback Machine snapshots of privatehealth.gov.au and fund websites | Independent history | Patchy coverage |
| Medibank find-a-provider / Members' Choice list | Medibank's own view, incl. tier | Current only |
| Commonwealth declared hospitals list and PHI circulars | Provider numbers, openings, closures, re-declarations | Needed to remove closures from the denominator |
| APHA members | Confirmation of status and dates from the hospital side | Best validation; also source for claims 1, 5 and 6 |

## Validation rules (non-negotiable after 2025)

1. Every status change Medibank-side is confirmed in at least two independent sources before it counts.
2. Every row is keyed on Commonwealth hospital provider number, never on hospital name.
3. Fund identity is checked on every snapshot load (fund code + fund name), so a re-ordered file can't silently swap funds again.
4. Closures, re-declarations (e.g. Western Hospital, 1 Nov 2024) and mergers are handled explicitly, not dropped.
5. Before anything goes to Brett, a separate reviewer re-derives the headline numbers from raw data.

## Things Medibank will say, and how we pre-empt them

| Medibank response | What we need |
|---|---|
| "Hospitals walked away, not us" | Who initiated: termination notices, dispute timelines from APHA members |
| "It's industry-wide pressure" | Other funds as controls in the same catchment |
| "Those hospitals closed" | Closure-adjusted denominators |
| "We have agreements with most private hospitals" | Catchment-level, not national, figures |
| "Your data is wrong again" | Validation log, provider-number keys, second-source confirmation |
| "We're a minority, non-controlling investor" | Focus on Medibank as funder; ownership only defines where to look |

## Inputs needed from David / Brett

- [ ] Source and definition of the 75.6% to 74.5% figure (Jun 2023 to Aug 2026). Is it ROADS?
- [ ] Access to EHA historical agreement snapshots, and confirmation the 2021 mapping issue is fixed
- [ ] APHA member hospitals in each treated catchment, willing to confirm contract history
- [ ] Decision on whether mental health (iMH) is in scope for phase 2
