# The August 2025 retraction

## What happened

- **24 Aug 2025:** APHA issued a media release claiming Medibank's contracting with local hospitals had "nosedived" around East Sydney Private Hospital. It said Medibank held contracts with 84.13% of private hospitals in adjacent local areas (106 of 126) when it bought 49% of ESPH in August 2020, and that July 2025 data showed a sharp fall. It also flagged Adeney, Nundah and Western Hospital markets for scrutiny.
- **28 Aug 2025:** APHA apologised and withdrew the release. It had "sourced the wrong dataset": another insurer's hospital contract status had been applied to Medibank.
- The consultant named was **Empowered Health Analytics**. The cause was a change in the structure of the contracted hospital agreements data file in late 2021 (attributed to fund mergers and/or closures). Safeguards that should have flagged the structural change didn't, because the data was held as CSV. The consultant said extra safeguards for dynamic data loads were being built.
- The correct Medibank figures were never published.

## Why it matters now

1. Medibank has already won this argument once. Anything new from APHA on the same theme will be checked line by line.
2. The original *question* was never answered. The correct numbers for ESPH may well show a real effect, a smaller one, or none. We should find out before Brett says anything.
3. The 75.6% to 74.5% figure in Brett's November 2026 email may come from the same pipeline.

## Safeguards for this project

See validation rules in `03-method/contracting-change-method.md`. In short: provider-number keys, fund identity checks on every load, two-source confirmation, independent re-derivation before release.

## Sources

- Hospital + Healthcare, "Peak body says Medibank has 'a serious conflict of interest' to answer", 27 Aug 2025
- Hospital + Healthcare, "Peak body issues apology to Medibank 'for data error'", 28 Aug 2025
