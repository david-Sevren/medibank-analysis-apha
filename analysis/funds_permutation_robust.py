"""Robustness: like funds_permutation.py but only hospitals listed >= 6 months before the last snapshot,
excluding hospices and birthing centres (which no fund or few funds contract). Comparators Bupa, HCF, nib."""
import sys, itertools, numpy as np, pandas as pd
f = pd.read_csv(sys.argv[1], dtype={'prov': str}, parse_dates=['snapshot']); out = sys.argv[2]
COMP = ['BUP', 'HCF', 'NIB']; S = sorted(f.snapshot.unique()); END = S[-1]
end = f[f.snapshot == END].pivot(index='prov', columns='fund', values='agree')
loc = f.sort_values('snapshot').groupby('prov')[['name', 'cat', 'state', 'postcode']].last()
first = f[f.fund == 'MBP'].groupby('prov').snapshot.min()
MB = ['0017500W', '0037140T', '0017360L', '0065780W', '0095140A', '0015550A', '0056310K']
excl = loc.name.str.contains('HOSPICE|BIRTHING|Hospice|Birthing|Anam Cara', regex=True)
rows = []
for R in [25, 50, 100]:
    near = set(pd.read_csv(f'{out}/fund_near_entrants_{R}km.csv').name)
    ids = [i for i in end.index if S[0] < first[i] <= END - pd.Timedelta(days=182) and loc.at[i, 'cat'] in 'CDEF' and i not in MB and not excl[i]]
    d = pd.DataFrame({'name': loc.loc[ids, 'name'], 'pc': loc.loc[ids, 'postcode'], 'near': loc.loc[ids, 'name'].isin(near),
                      'mbp': end.loc[ids, 'MBP'], 'comp': end.loc[ids, COMP].mean(axis=1)})
    d['gap'] = d.comp - d.mbp; g = d.gap.values; k = int(d.near.sum()); n = len(g)
    obs = g[d.near.values].mean() - g[~d.near.values].mean(); tot = g.sum(); cnt = m = 0
    for c in itertools.combinations(range(n), k):
        s = g[list(c)].sum(); m += 1; cnt += (s / k - (tot - s) / (n - k)) >= obs - 1e-12
    rows.append(dict(radius_km=R, near_n=k, else_n=n - k, mbp_near=d[d.near].mbp.mean(), comp_near=d[d.near].comp.mean(),
                     mbp_else=d[~d.near].mbp.mean(), comp_else=d[~d.near].comp.mean(), did_pp=obs * 100, perm_p=cnt / m))
    if R == 25: print(d.sort_values(['near', 'gap'], ascending=False).round(2).to_string())
r = pd.DataFrame(rows); r.to_csv(f'{out}/fund_permutation_robust.csv', index=False); print(r.round(3).to_string(index=False))
