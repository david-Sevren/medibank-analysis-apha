"""Sensitivity: rerun the briefing's network and new-hospital figures on surgical hospitals only.
Drops second-tier categories A and B (mental health, rehab) and uncategorised hospitals from every comparison,
and still excludes all seven Medibank-interest hospitals (the three iMH hospitals are mental health anyway).
Same definitions as briefing_figures.py."""
import sys, numpy as np, pandas as pd
from math import comb
f = pd.read_csv(sys.argv[1], dtype={'prov': str}, parse_dates=['snapshot']); out = sys.argv[2]
FUNDS = ['MBP', 'BUP', 'HCF', 'NIB', 'HBF', 'AUF']
MB = ['0017500W', '0037140T', '0017360L', '0065780W', '0095140A', '0015550A', '0056310K']
S = sorted(f.snapshot.unique()); F0, END = S[0], S[-1]
loc = f.sort_values('snapshot').groupby('prov')[['name', 'state', 'cat']].last()
surg = loc.index[loc.cat.fillna('?').str[0].isin(list('CDEFG'))]
W = {fd: f[f.fund == fd].pivot(index='prov', columns='snapshot', values='agree') for fd in FUNDS}
pres = W['MBP'].notna(); first = pres.idxmax(axis=1); last = pres[pres.columns[::-1]].idxmax(axis=1)
L = []
def P(*a): s = ' '.join(str(x) for x in a); print(s); L.append(s)
P('SURGICAL HOSPITALS ONLY (second-tier C to G), all seven Medibank-interest hospitals excluded')
P('Category mix of all hospitals ever listed:', loc.cat.fillna('?').str[0].value_counts().to_dict())
P('Network size, Aug 2020 -> Oct 2026:')
for fd in FUNDS:
    w = W[fd].loc[W[fd].index.isin(surg) & ~W[fd].index.isin(MB)]
    P(f'  {fd}: {int(w[F0].sum())} -> {int(w[END].sum())} ({int(w[END].sum() - w[F0].sum()):+d})')
new = [i for i in first.index if first[i] > F0 and last[i] == END and (END - first[i]).days >= 365 and i not in MB and i in surg]
d = pd.DataFrame({fd: W[fd].loc[new, END] for fd in FUNDS}); d['year'] = first[new].dt.year
P(f'New surgical hospitals listed 12+ months: {len(new)}')
P('  agreements Oct 2026:', {fd: f'{int(d[fd].sum())} ({d[fd].mean():.0%})' for fd in FUNDS})
P('Paired (exact McNemar):')
for fd in FUNDS[1:]:
    a = int(((d[fd] == 1) & (d.MBP == 0)).sum()); b = int(((d[fd] == 0) & (d.MBP == 1)).sum()); n = a + b
    p = min(1, 2 * sum(comb(n, i) for i in range(min(a, b) + 1)) / 2 ** n) if n else 1
    P(f'  {fd}: {fd}-only {a}, Medibank-only {b}, p={p:.4f}')
d['comp'] = d[['BUP', 'HCF', 'NIB']].mean(axis=1)
P('By year first listed:')
for y, s in d.groupby('year'): P(f'  {y}: n={len(s)} MBP {s.MBP.mean():.0%} comp {s.comp.mean():.0%} gap {100*(s.comp.mean()-s.MBP.mean()):+.0f}')
pre, post = d[d.year < 2023], d[d.year >= 2023]
P(f'  before 2023: n={len(pre)} MBP {pre.MBP.mean():.0%} comp {pre.comp.mean():.0%} | 2023 on: n={len(post)} MBP {post.MBP.mean():.0%} comp {post.comp.mean():.0%}')
g = (d.comp - d.MBP).values; m = (d.year >= 2023).values; obs = g[m].mean() - g[~m].mean()
rng = np.random.default_rng(11); perm = np.array([(lambda q: g[q].mean() - g[~q].mean())(rng.permutation(m)) for _ in range(50000)])
P(f'  change in gap {obs*100:+.1f} pts, permutation p={(perm >= obs - 1e-12).mean():.4f}')
dates = first[new].values; splits = sorted(set(dates))[1:]
def best(gv): return max(gv[dates >= s].mean() - gv[dates < s].mean() for s in splits if 4 <= (dates >= s).sum() <= len(gv) - 4)
b0 = best(g); pm = np.mean([best(rng.permutation(g)) >= b0 - 1e-12 for _ in range(4000)])
P(f'  scan over every split: best change {b0*100:+.1f} pts, scan-adjusted p={pm:.3f}')
dropped = [i for i in first.index if first[i] > F0 and last[i] == END and (END - first[i]).days >= 365 and i not in MB and i not in surg]
P(f'Dropped new non-surgical hospitals ({len(dropped)}):')
for i in dropped: P(f'  {loc.at[i,"name"]} ({loc.at[i,"cat"]}, {loc.at[i,"state"]}):', {fd: int(W[fd].at[i, END]) for fd in FUNDS})
n26 = [i for i in first.index if first[i].year == 2026 and last[i] == END and i not in MB and i in surg]
c = pd.DataFrame({fd: W[fd].loc[n26, END] for fd in FUNDS}); 
P(f'2026 surgical listings (<12 months): n={len(n26)} MBP {int(c.MBP.sum())} ({c.MBP.mean():.0%}) Bupa/HCF/nib avg {c[["BUP","HCF","NIB"]].mean(axis=1).mean():.0%}')
open(f'{out}/briefing/surgical_only_sensitivity.txt', 'w').write('\n'.join(L))
