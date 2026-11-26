"""Medibank as the odd one out: new hospitals where Medibank has no agreement but >=2 of the active
contractors (Bupa, HCF, Australian Unity) do, at the last complete snapshot. Near vs elsewhere, with Fisher exact test.
Also merges Medibank's later status from the Medibank-only file (to Oct 2026)."""
import sys, numpy as np, pandas as pd
from math import comb
f = pd.read_csv(sys.argv[1], dtype={'prov': str}, parse_dates=['snapshot'])
mbfull = pd.read_csv(sys.argv[2], dtype={'prov': str}, parse_dates=['snapshot'])
out = sys.argv[3]
S = sorted(f.snapshot.unique()); END = S[-1]
ACTIVE = sys.argv[4].split(',') if len(sys.argv) > 4 else ['BUP', 'HCF', 'AUF']
MIN_OTHERS = int(sys.argv[5]) if len(sys.argv) > 5 else 2
TAG = '_'.join(ACTIVE)
near = pd.read_csv(f'{out}/fund_near_entrants_50km.csv')
loc = f.sort_values('snapshot').groupby('prov')[['name', 'cat']].last()
w = {fd: f[f.fund == fd].pivot(index='prov', columns='snapshot', values='agree') for fd in ['MBP'] + ACTIVE}
first = w['MBP'].notna().idxmax(axis=1); last = w['MBP'].notna()[w['MBP'].columns[::-1]].idxmax(axis=1)
MB = ['0017500W', '0037140T', '0017360L', '0065780W', '0095140A', '0015550A', '0056310K']
ent = [i for i in first.index if first[i] > S[0] and last[i] == END and i not in MB]
nearnames = set(near.name)
rows = []
for i in ent:
    others = sum(w[fd].at[i, END] for fd in ACTIVE)
    rows.append(dict(prov=i, name=loc.at[i, 'name'], cat=loc.at[i, 'cat'], near=loc.at[i, 'name'] in nearnames,
                     mbp=w['MBP'].at[i, END], others_yes=others))
r = pd.DataFrame(rows)
r['mbp_odd_out'] = (r.mbp == 0) & (r.others_yes >= MIN_OTHERS)
r['mbp_only'] = (r.mbp == 1) & (r.others_yes == 0)
mb_last = mbfull[mbfull.snapshot == mbfull.snapshot.max()].set_index('prov').agree
r['mbp_oct26'] = r.prov.map(mb_last)
def fisher(a, b, c, d):  # one-sided: P(X >= a) for near-odd-out
    n1, n2, k = a + b, c + d, a + c; N = n1 + n2
    return sum(comb(n1, x) * comb(n2, k - x) for x in range(a, min(n1, k) + 1)) / comb(N, k)
pd.set_option('display.width', 250)
for grp, sub in [('overnight surgical C-F', r[r.cat.isin(list('CDEF'))]), ('day hospitals G', r[r.cat == 'G']), ('all', r)]:
    a = int(sub[sub.near].mbp_odd_out.sum()); b = int((~sub[sub.near].mbp_odd_out).sum())
    c = int(sub[~sub.near].mbp_odd_out.sum()); d = int((~sub[~sub.near].mbp_odd_out).sum())
    print(f'{grp}: Medibank odd-one-out near {a}/{a+b}, elsewhere {c}/{c+d}; one-sided Fisher p = {fisher(a,b,c,d):.3f}; '
          f'Medibank-only near {int(sub[sub.near].mbp_only.sum())}, elsewhere {int(sub[~sub.near].mbp_only.sum())}')
odd = r[r.mbp_odd_out].sort_values(['near', 'cat'], ascending=[False, True])
print(odd.to_string(index=False)); r.to_csv(f'{out}/fund_odd_one_out_{TAG}.csv', index=False)
