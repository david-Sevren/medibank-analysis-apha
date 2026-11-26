"""Network growth by fund, Aug 2020 to Oct 2026: stock, flows, new-hospital uptake by age and category.
Writes outputs/network_*.csv and a hospital-level audit table."""
import sys, numpy as np, pandas as pd
f = pd.read_csv(sys.argv[1], dtype={'prov': str, 'postcode': str}, parse_dates=['snapshot']); out = sys.argv[2]
FUNDS = ['MBP', 'BUP', 'HCF', 'NIB', 'HBF', 'AUF']
S = sorted(f.snapshot.unique()); F0, END = S[0], S[-1]
loc = f.sort_values('snapshot').groupby('prov')[['name', 'state', 'postcode', 'lat', 'lon', 'cat']].last()
grp = lambda c: 'Overnight surgical (C-F)' if c in 'CDEF' else ('Day hospital (G)' if c == 'G' else ('Mental health / rehab (A-B)' if c in 'AB' else 'Uncategorised'))
loc['group'] = loc.cat.map(grp)
W = {fd: f[f.fund == fd].pivot(index='prov', columns='snapshot', values='agree') for fd in FUNDS}
pres = W['MBP'].notna(); first = pres.idxmax(axis=1); last = pres[pres.columns[::-1]].idxmax(axis=1)

# 1. stock
stock = []
for fd in FUNDS:
    for g in ['All'] + sorted(loc.group.unique()):
        ids = loc.index if g == 'All' else loc.index[loc.group == g]
        a = W[fd].loc[ids, F0].dropna(); b = W[fd].loc[ids, END].dropna()
        stock.append(dict(fund=fd, group=g, listed_aug20=len(a), agreements_aug20=int(a.sum()), share_aug20=a.mean(),
                          listed_oct26=len(b), agreements_oct26=int(b.sum()), share_oct26=b.mean(),
                          agreements_change=int(b.sum() - a.sum()), share_change_pp=(b.mean() - a.mean()) * 100))
stock = pd.DataFrame(stock); stock.to_csv(f'{out}/network_stock.csv', index=False)

# 2. flows (agreement count change decomposition)
flows = []
for fd in FUNDS:
    w = W[fd]; gained = lost = 0
    for a, b in zip(S[:-1], S[1:]):
        both = w[[a, b]].dropna(); gained += int(((both[a] == 0) & (both[b] == 1)).sum()); lost += int(((both[a] == 1) & (both[b] == 0)).sum())
    ent = first[first > F0].index; ex = last[last < END].index
    flows.append(dict(fund=fd, gained_existing=gained, lost_existing=lost,
                      entrants=len(ent), entrants_with_agreement_at_entry=int(sum(w.at[i, first[i]] for i in ent)),
                      exits=len(ex), exits_had_agreement=int(sum(w.at[i, last[i]] for i in ex)),
                      net_change=int(w[END].sum() - w[F0].sum())))
pd.DataFrame(flows).to_csv(f'{out}/network_flows.csv', index=False)

# 3. hospital-level audit table: every hospital first listed after Aug 2020 and still listed Oct 2026
rows = []
for i in first.index:
    if not (first[i] > F0 and last[i] == END): continue
    r = dict(provider_number=i, hospital=loc.at[i, 'name'], state=loc.at[i, 'state'], postcode=loc.at[i, 'postcode'],
             second_tier_cat=loc.at[i, 'cat'], group=loc.at[i, 'group'], first_listed=first[i].date(),
             months_listed=round((END - first[i]).days / 30.44, 1))
    for fd in FUNDS:
        s = W[fd].loc[i].dropna(); g = s[s == 1]
        r[f'{fd}_oct26'] = int(s.iloc[-1]); r[f'{fd}_first_agreement'] = g.index[0].date() if len(g) else None
    rows.append(r)
aud = pd.DataFrame(rows).sort_values(['group', 'first_listed', 'hospital']); aud.to_csv(f'{out}/network_new_hospitals_audit.csv', index=False)

# 4. uptake by age band and group
aud['age'] = pd.cut(aud.months_listed, [0, 6, 12, 24, 100], labels=['<6m', '6-12m', '12-24m', '24m+'], right=False)
up = aud.groupby(['group', 'age'], observed=True)[[f'{fd}_oct26' for fd in FUNDS]].mean()
up['n'] = aud.groupby(['group', 'age'], observed=True).size(); up.to_csv(f'{out}/network_uptake_by_age.csv')
up2 = aud[aud.months_listed >= 12].groupby('group')[[f'{fd}_oct26' for fd in FUNDS]].mean(); up2['n'] = aud[aud.months_listed >= 12].groupby('group').size()
up2.to_csv(f'{out}/network_uptake_12m_plus.csv')
pd.set_option('display.width', 250)
print(stock[stock.group.isin(['All', 'Overnight surgical (C-F)', 'Day hospital (G)'])].round(3).to_string(index=False))
print(pd.DataFrame(flows).to_string(index=False)); print(up.round(2).to_string()); print(up2.round(2).to_string())
# rank of Medibank among funds, entrants listed >=12 months, excluding HBF (WA-centric)
print('Medibank rank (1=highest) among 6 funds by group, 12m+:'); print(up2.drop(columns='n').rank(axis=1, ascending=False)['MBP_oct26'])
