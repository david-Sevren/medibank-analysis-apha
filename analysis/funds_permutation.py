"""Hospital-level gap test on new overnight surgical hospitals (C-F) still listed at the last snapshot.
gap_i = share of comparator funds with an agreement - Medibank agreement (1/0).
Statistic = mean gap near - mean gap elsewhere. Exact permutation p (all splits of the same sizes)."""
import sys, itertools, numpy as np, pandas as pd
f = pd.read_csv(sys.argv[1], dtype={'prov': str}, parse_dates=['snapshot']); out = sys.argv[2]
COMP = sys.argv[3].split(',') if len(sys.argv) > 3 else ['BUP', 'HCF', 'NIB']
S = sorted(f.snapshot.unique()); END = S[-1]
end = f[f.snapshot == END].pivot(index='prov', columns='fund', values='agree')
rows = []
for R in [25, 50, 100]:
    near = pd.read_csv(f'{out}/fund_near_entrants_{R}km.csv')
    loc = f.sort_values('snapshot').groupby('prov')[['name', 'cat']].last()
    first = f[f.fund == 'MBP'].groupby('prov').snapshot.min()
    MB = ['0017500W', '0037140T', '0017360L', '0065780W', '0095140A', '0015550A', '0056310K']
    ids = [i for i in end.index if first[i] > S[0] and loc.at[i, 'cat'] in 'CDEF' and i not in MB]
    d = pd.DataFrame({'name': loc.loc[ids, 'name'], 'near': loc.loc[ids, 'name'].isin(set(near.name)),
                      'mbp': end.loc[ids, 'MBP'], 'comp': end.loc[ids, COMP].mean(axis=1)})
    d['gap'] = d.comp - d.mbp
    g = d.gap.values; k = int(d.near.sum()); obs = g[d.near.values].mean() - g[~d.near.values].mean()
    tot = g.sum(); n = len(g); cnt = 0; m = 0
    for c in itertools.combinations(range(n), k):
        s = g[list(c)].sum(); stat = s / k - (tot - s) / (n - k); m += 1; cnt += stat >= obs - 1e-12
    rows.append(dict(radius_km=R, near_n=k, else_n=n - k, mbp_near=d[d.near].mbp.mean(), comp_near=d[d.near].comp.mean(),
                     mbp_else=d[~d.near].mbp.mean(), comp_else=d[~d.near].comp.mean(), did_pp=obs * 100, perm_p=cnt / m))
    if R == 25: print(d.sort_values(['near', 'gap'], ascending=False).round(2).to_string())
res = pd.DataFrame(rows); res.to_csv(f'{out}/fund_permutation_{"_".join(COMP)}.csv', index=False); print(res.round(3).to_string(index=False))
