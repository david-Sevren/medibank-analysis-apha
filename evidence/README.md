# Evidence register

Files supplied by David du Plessis (Aller Consulting) for this analysis, kept exactly as received. **Do not edit anything in `original-files/`.** Working copies used by the scripts sit in `data/raw/` under descriptive names and are byte-identical (same SHA-256).

To check integrity at any time:

```
cd evidence/original-files && sha256sum -c ../SHA256SUMS
```

## Files

| # | File as received | Received (AEDT) | What it is | Rows | Working copy | SHA-256 |
|---|---|---|---|---|---|---|
| E1 | `Sum_of_Hasagreement__1795727125573.xlsx` | 27 Nov 2026 08:09 | Medibank (MBP) hospital agreement status by hospital and quarter, Aug 2020 to Oct 2026 | 17,132 (17,032 after removing 100 zero-length rows) | `data/raw/medibank_agreements_2020-2026.xlsx` | `dac6a5695c2633cb140059be1a7a702544b567f19a43976ba4603a84a95b1279` |
| E2 | `Sum_of_Hasagreement__1795727998909.xlsx` | 27 Nov 2026 08:26 | Agreement status for six funds (MBP, BUP, HCF, NIB, HBF, AUF). **Truncated at 80,000 data rows by the export tool; superseded by E3. Not used for any figure.** | 80,000 + title rows | `data/raw/agreements_by_fund_2020-2026.xlsx` | `2126f403c8dedb446c8016d831167208829d4be41a05fdbc9bf07acb8fa36777` |
| E3 | `Sum_of_Hasagreement__1795729191261.csv` | 27 Nov 2026 08:40 | Full six-fund export, same structure as E1 plus `FundCode`. 17,132 rows per fund. Primary source for every multi-fund figure | 102,792 | `data/raw/agreements_by_fund_2020-2026.csv` | `d097e6501d3de0fc5243c96764c166489ca5fd099cd6b15aaf8d51bda12df4a8` |
| E4 | Email from Brett Heffernan (APHA CEO), pasted into the session | 27 Nov 2026 | The questions this work answers | n/a | `01-brief/brett-email.md` | n/a |

Columns in E1 and E3: `FacilityName, FromDate, ToDate, HospitalLatitude, HospitalLongitude, HospitalState, HospitalStreetPostcode, ProviderNumber, SecondTierCategory, [FundCode], HasAgreement`. E3 starts with a UTF-8 byte-order mark and uses ISO dates; E1 uses "Mon d, yyyy" dates.

## Known properties of the source data

- **Source still to be confirmed.** The export's origin (fund-reported agreement hospital lists) and its fund codes must be checked against each fund's published agreement hospital list before any figure is used publicly. Owner: David.
- E1 and the MBP rows of E3 match on 17,032 of 17,032 records, which supports the MBP code being Medibank.
- 100 records per fund have an end date before their start date. They are removed in cleaning (`analysis/clean.py`, `analysis/clean_funds.py`).
- Funds report changes in batches (e.g. Bupa +66 in Jul 2024, nib +46 in Jul 2025), so the quarter a change first appears is when it was reported, not when it was signed.

## Other evidence

Public sources (annual reports, media, ASA letter, etc.) are logged with references in `04-sources/sources-log.md`. They are cited, not stored here.
