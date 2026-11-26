"""Clean the multi-fund agreement export into a snapshot panel (prov x snapshot x fund).
Handles the export's preamble rows, drops zero-length rows, and drops any snapshot not present for every fund
at full hospital count (the Excel export truncates at 80,000 rows)."""
import sys, pandas as pd
src, out = sys.argv[1], sys.argv[2]
if src.endswith('.csv'):
    df = pd.read_csv(src, dtype=str, encoding='utf-8-sig')
else:
    raw = pd.read_excel(src, header=None, dtype=str)
    hdr = raw.index[raw[0] == 'FacilityName'][0]
    df = raw.iloc[hdr + 1:].copy(); df.columns = raw.iloc[hdr].tolist()
df = df.dropna(subset=['ProviderNumber', 'FundCode'])
df['FromDate'] = pd.to_datetime(df.FromDate); df['ToDate'] = pd.to_datetime(df.ToDate)
df = df[df.ToDate >= df.FromDate].copy()
df['agree'] = df.HasAgreement.astype(float).astype(int)
df = df.rename(columns={'FromDate': 'snapshot', 'ProviderNumber': 'prov', 'FacilityName': 'name', 'HospitalState': 'state',
                        'HospitalStreetPostcode': 'postcode', 'HospitalLatitude': 'lat', 'HospitalLongitude': 'lon', 'FundCode': 'fund'})
df['cat'] = df.SecondTierCategory.str[0].fillna('?')
assert not df.duplicated(['prov', 'snapshot', 'fund']).any()
cnt = df.groupby(['snapshot', 'fund']).prov.nunique().unstack()
complete = cnt.index[(cnt.min(axis=1) == cnt.max(axis=1)) & (cnt.min(axis=1) > 0.9 * cnt.min(axis=1).median())]
dropped = sorted(set(cnt.index) - set(complete))
df = df[df.snapshot.isin(complete)]
df[['snapshot', 'prov', 'name', 'state', 'postcode', 'lat', 'lon', 'cat', 'fund', 'agree']].to_csv(out, index=False)
print('funds', sorted(df.fund.unique()), '| snapshots kept', len(complete), complete.min().date(), 'to', complete.max().date(),
      '| dropped incomplete', [d.date() for d in dropped])
