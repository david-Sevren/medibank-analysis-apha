"""Clean the Medibank hospital agreement file into a snapshot panel.

Rules:
- Drop rows where ToDate < FromDate (zero-length artefacts; 100 rows, all HasAgreement=1).
- Snapshot key = FromDate. Rows with ToDate 3999-12-31 before the final period are a facility's
  last appearance (it exits the list afterwards); keep them as present in that snapshot.
"""
import sys, pandas as pd
src, out = sys.argv[1], sys.argv[2]
df = pd.read_excel(src, dtype={'ProviderNumber': str, 'HospitalStreetPostcode': str})
df['FromDate'] = pd.to_datetime(df['FromDate']); df['ToDate'] = pd.to_datetime(df['ToDate'])
n0 = len(df)
df = df[df.ToDate >= df.FromDate].copy()
df['snapshot'] = df['FromDate']
df['cat'] = df['SecondTierCategory'].str[0].fillna('?')
assert not df.duplicated(['ProviderNumber', 'snapshot']).any()
df = df.rename(columns={'HospitalLatitude': 'lat', 'HospitalLongitude': 'lon', 'HospitalState': 'state',
                        'HospitalStreetPostcode': 'postcode', 'ProviderNumber': 'prov', 'FacilityName': 'name',
                        'HasAgreement': 'agree'})
df[['snapshot', 'prov', 'name', 'state', 'postcode', 'lat', 'lon', 'cat', 'agree']].to_csv(out, index=False)
print(f'rows in {n0}, kept {len(df)}, snapshots {df.snapshot.nunique()}, hospitals {df.prov.nunique()}')
