"""Verification checks for the APHA briefing (27 Nov 2026).
1. HBF vs Australian Unity: do their statuses move together outside WA (AHSA contracting), and not in WA?
2. Where are the new hospitals (state)?
3. Are any 'new hospitals' re-declarations of an existing hospital (new provider number, same site)?
4. Independent re-derivation of headline figures straight from the raw CSV.
5. Which hospitals make up the Bupa-yes / Medibank-no gap (by type and operator name)?"""
import sys, csv, math, datetime as dt, collections
import pandas as pd, numpy as np
raw, panel = sys.argv[1], sys.argv[2]
f = pd.read_csv(panel, dtype={'prov': str, 'postcode': str}, parse_dates=['snapshot'])
S = sorted(f.snapshot.unique()); F0, END = S[0], S[-1]
loc = f.sort_values('snapshot').groupby('prov')[['name', 'state', 'lat', 'lon', 'cat']].last()
W = {fd: f[f.fund == fd].pivot(index='prov', columns='snapshot', values='agree') for fd in ['MBP', 'BUP', 'HCF', 'NIB', 'HBF', 'AUF']}
pres = W['MBP'].notna(); first = pres.idxmax(axis=1); last = pres[pres.columns[::-1]].idxmax(axis=1)
print('== 1. HBF vs Australian Unity agreement on status, Oct 2026 and all snapshots')
for where, mask in [('WA', loc.state == 'WA'), ('outside WA', loc.state != 'WA')]:
    ids = loc.index[mask]
    a = W['HBF'].loc[ids].stack(); b = W['AUF'].loc[ids].stack(); j = pd.concat([a, b], axis=1).dropna()
    e = pd.concat([W['HBF'].loc[ids, END], W['AUF'].loc[ids, END]], axis=1).dropna()
    others = {fd: (pd.concat([W['HBF'].loc[ids].stack(), W[fd].loc[ids].stack()], axis=1).dropna().pipe(lambda x: (x.iloc[:, 0] == x.iloc[:, 1]).mean())) for fd in ['MBP', 'BUP', 'HCF', 'NIB']}
    print(f'  {where}: hospitals {len(ids)}; HBF=AUF on {(j.iloc[:,0]==j.iloc[:,1]).mean():.1%} of hospital-quarters, Oct26 {(e.iloc[:,0]==e.iloc[:,1]).mean():.1%}; HBF vs others', {k: f'{v:.1%}' for k, v in others.items()})
print('== 2. New hospitals (first listed after Aug 2020, still listed Oct 2026, listed 12+ months) by state')
new = [i for i in first.index if first[i] > F0 and last[i] == END]
new12 = [i for i in new if (END - first[i]).days >= 365]
print(' ', loc.loc[new12].state.value_counts().to_dict(), '| total', len(new12))
print('== 3. Possible re-declarations: new provider number within 0.3 km of a provider that left the list within 2 quarters')
exited = [i for i in last.index if last[i] < END]
hav = lambda a, b, c, d: 12742 * np.arcsin(np.sqrt(np.sin(np.radians(c - a) / 2) ** 2 + np.cos(np.radians(a)) * np.cos(np.radians(c)) * np.sin(np.radians(d - b) / 2) ** 2))
redecl = []
for i in new:
    for x in exited:
        dkm = hav(loc.at[i, 'lat'], loc.at[i, 'lon'], loc.at[x, 'lat'], loc.at[x, 'lon'])
        gap = (first[i] - last[x]).days
        if dkm <= 0.3 and -100 <= gap <= 200:
            redecl.append((i, loc.at[i, 'name'], first[i].date(), x, loc.at[x, 'name'], last[x].date(), round(dkm, 2),
                           {fd: (W[fd].at[x, last[x]], W[fd].at[i, END]) for fd in ['MBP', 'BUP', 'HCF', 'NIB']}))
for r in redecl: print(' ', r)
print('  count', len(redecl), '| of which in the 12+ month set', sum(r[0] in new12 for r in redecl))
pd.DataFrame(redecl, columns=['new_prov', 'new_name', 'first', 'old_prov', 'old_name', 'old_last', 'km', 'status_old_vs_new']).to_csv('outputs/verify_redeclarations.csv', index=False)
print('== 4. Independent recompute from raw CSV (csv module only)')
rows = collections.defaultdict(dict)
with open(raw, encoding='utf-8-sig') as fh:
    for r in csv.DictReader(fh):
        P = lambda x: dt.datetime.strptime(x[:10], '%Y-%m-%d') if x[:4].isdigit() else dt.datetime.strptime(x, '%b %d, %Y')
        a, b = P(r['FromDate']), P(r['ToDate'])
        if b < a: continue
        rows[(r['ProviderNumber'], a)][r['FundCode']] = int(float(r['HasAgreement']))
snaps = sorted({k[1] for k in rows}); s0, s1 = snaps[0], snaps[-1]
for fd in ['MBP', 'BUP', 'HCF', 'NIB', 'HBF', 'AUF']:
    print(f'  {fd}: Aug20 {sum(v[fd] for k, v in rows.items() if k[1] == s0)}  Oct26 {sum(v[fd] for k, v in rows.items() if k[1] == s1)}')
fl = collections.defaultdict(set)
for (p, s) in rows: fl[p].add(s)
n12 = [p for p, ss in fl.items() if min(ss) > s0 and max(ss) == s1 and (s1 - min(ss)).days >= 365]
print('  new 12m+', len(n12), {fd: sum(rows[(p, s1)][fd] for p in n12) for fd in ['MBP', 'BUP', 'HCF', 'NIB', 'HBF', 'AUF']})
print('  Bupa-yes/Medibank-no', sum(rows[(p, s1)]['BUP'] == 1 and rows[(p, s1)]['MBP'] == 0 for p in n12),
      ' Medibank-yes/Bupa-no', sum(rows[(p, s1)]['BUP'] == 0 and rows[(p, s1)]['MBP'] == 1 for p in n12))
print('== 5. The Bupa-yes / Medibank-no hospitals')
gap = [i for i in new12 if W['BUP'].at[i, END] == 1 and W['MBP'].at[i, END] == 0]
g = loc.loc[gap, ['name', 'state', 'cat']].assign(first=first[gap].dt.date, HCF=W['HCF'].loc[gap, END], NIB=W['NIB'].loc[gap, END])
pd.set_option('display.width', 220); print(g.sort_values(['cat', 'first']).to_string())
