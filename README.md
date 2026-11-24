# Medibank Analysis for APHA

Working repository for an analysis commissioned informally by Brett Heffernan (CEO, Australian Private Hospitals Association) into whether Medibank's ownership interests in private hospitals are distorting where Medibank members receive care.

Prepared by Aller Consulting (David du Plessis). Private. Not for distribution.

## Current phase

Phase 1: establish exactly which hospitals Medibank holds an ownership interest in, with dates, stakes, provider numbers and locations. This is the anchor for everything else.

Phase 2 (next): test whether Medibank's contracting behaviour with *other* hospitals in the same catchment changed after Medibank took its interest. See `03-method/contracting-change-method.md`.

## Structure

| Folder | What's in it |
|---|---|
| `01-brief/` | Brett's original email and the claims we've pulled out of it |
| `02-ownership/` | Register of Medibank hospital interests, plus things that look like ownership but aren't |
| `03-method/` | How we intend to prove (or disprove) each claim |
| `04-sources/` | Every source we rely on, with access dates |
| `05-lessons/` | The August 2025 APHA retraction and the safeguards it demands |

## Ground rules

1. Every number that leaves this repo must trace to a primary source in `04-sources/sources-log.md`.
2. Every hospital-level contract status must be checked against a second, independent source before it is used (see `05-lessons/2025-data-error.md` for why).
3. Medibank holds minority or 50/50 stakes, not control. Language must say "Medibank has an ownership interest in", not "Medibank-owned", unless we can show control.
4. Facts and inferences are kept apart. Anything not verified is marked `TO VERIFY`.
