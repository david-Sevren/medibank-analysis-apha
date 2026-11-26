# Medibank Analysis for APHA

Working repository for an analysis commissioned informally by Brett Heffernan (CEO, Australian Private Hospitals Association) into whether Medibank's ownership interests in private hospitals are distorting where Medibank members receive care.

Prepared by Aller Consulting (David du Plessis). Private. Not for distribution.

## Current phase

Phase 1: establish exactly which hospitals Medibank holds an ownership interest in, with dates, stakes, provider numbers and locations. This is the anchor for everything else.

Phase 2 (done 27 Nov 2026): test whether Medibank's contracting behaviour with *other* hospitals changed near the hospitals it part-owns, and how its network growth compares with other funds. Findings in `06-findings/01` to `05`; the briefing sent to APHA, with a map from every figure to its source, is in `07-briefing/`.

Open before any figure is used publicly: confirm the data source and fund codes against each fund's published agreement hospital list (see `evidence/README.md`).

## Structure

| Folder | What's in it |
|---|---|
| `01-brief/` | Brett's original email and the claims we've pulled out of it |
| `02-ownership/` | Register of Medibank hospital interests, plus things that look like ownership but aren't |
| `03-method/` | How we intend to prove (or disprove) each claim |
| `04-sources/` | Every source we rely on, with access dates |
| `05-lessons/` | The August 2025 APHA retraction and the safeguards it demands |
| `06-findings/` | Results, one file per question tested |
| `07-briefing/` | The APHA briefing (markdown, PDF, Word, chart) and the figure map: every number, the script and the output file behind it |
| `evidence/` | Files supplied for the analysis, exactly as received, with SHA-256 checksums and a register |
| `data/` | Working copies of the raw inputs (`raw/`, byte-identical to `evidence/`) and cleaned panels (`processed/`) |
| `analysis/` | Scripts. Medibank-only: `clean.py`, `radius.py`, `detail.py`, `charts.py`, `recheck.py`. Multi-fund: `clean_funds.py`, then the `funds_*`, `network_*`, `timing*` scripts. Briefing: `briefing_figures.py`, `briefing_esph.py`, `verify_briefing.py`, `build_audit_workbook.py` (commands in `07-briefing/README.md`) |
| `outputs/` | CSVs, charts and the audit workbook produced by the scripts; `outputs/briefing/` holds the tables behind each briefing figure |

## Ground rules

1. Every number that leaves this repo must trace to a primary source in `04-sources/sources-log.md`.
2. Every hospital-level contract status must be checked against a second, independent source before it is used (see `05-lessons/2025-data-error.md` for why).
3. Medibank holds minority or 50/50 stakes, not control. Language must say "Medibank has an ownership interest in", not "Medibank-owned", unless we can show control.
4. Facts and inferences are kept apart. Anything not verified is marked `TO VERIFY`.
