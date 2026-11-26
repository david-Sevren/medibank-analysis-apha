"""Briefing headline figures with Medibank's own part-owned hospitals EXCLUDED from every comparison.
New hospitals = first listed after Aug 2020, still listed Oct 2026, listed >= 12 months."""
import sys, os, itertools, numpy as np, pandas as pd
from math import comb
f = pd.read_csv(sys.argv[1], dtype={'prov': str}, parse_dates=['snapshot']); out = sys.argv[2]
tab = f'{out}/briefing'; os.makedirs(tab, exist_ok=True)  # supporting tables for every briefing figure
FUNDS = ['MBP', 'BUP', 'HCF', 'NIB', 'HBF', 'AUF']
MB = ['0017500W', '0037140T', '0017360L', '0065780W', '0095140A', '0015550A', '0056310K']
S = sorted(f.snapshot.unique()); F0, END = S[0], S[-1]
loc = f.sort_values('snapshot').groupby('prov')[['name', 'state', 'cat']].last()
W = {fd: f[f.fund == fd].pivot(index='prov', columns='snapshot', values='agree') for fd in FUNDS}
pres = W['MBP'].notna(); first = pres.idxmax(axis=1); last = pres[pres.columns[::-1]].idxmax(axis=1)
out_lines = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out_lines.append(s)
P('Network size (all hospitals, incl. Medibank sites), Aug 2020 -> Oct 2026:')
for fd in FUNDS: P(f'  {fd}: {int(W[fd][F0].sum())} -> {int(W[fd][END].sum())} ({int(W[fd][END].sum() - W[fd][F0].sum()):+d})')
P('Network size EXCLUDING the 7 Medibank-interest hospitals:')
for fd in FUNDS:
    w = W[fd].drop(index=MB, errors='ignore'); P(f'  {fd}: {int(w[F0].sum())} -> {int(w[END].sum())} ({int(w[END].sum() - w[F0].sum()):+d})')
pd.DataFrame([{'fund': fd, 'aug2020_all': int(W[fd][F0].sum()), 'oct2026_all': int(W[fd][END].sum()),
               'aug2020_excl_mb_sites': int(W[fd].drop(index=MB, errors='ignore')[F0].sum()),
               'oct2026_excl_mb_sites': int(W[fd].drop(index=MB, errors='ignore')[END].sum())} for fd in FUNDS]
             ).assign(change_excl_mb_sites=lambda x: x.oct2026_excl_mb_sites - x.aug2020_excl_mb_sites).to_csv(f'{tab}/network_counts.csv', index=False)
new = [i for i in first.index if first[i] > F0 and last[i] == END and (END - first[i]).days >= 365 and i not in MB]
d = pd.DataFrame({fd: W[fd].loc[new, END] for fd in FUNDS}); d['cat'] = loc.loc[new, 'cat']; d['year'] = first[new].dt.year
d['grp'] = d.cat.map(lambda c: 'C-F' if c in 'CDEF' else ('G' if c == 'G' else 'A-B'))
P(f'New hospitals listed 12+ months, excl. Medibank sites: {len(new)}')
P('  agreements Oct 2026:', {fd: f'{int(d[fd].sum())} ({d[fd].mean():.0%})' for fd in FUNDS})
for g in ['C-F', 'G', 'A-B']:
    s = d[d.grp == g]; P(f'  {g} (n={len(s)}):', {fd: f'{int(s[fd].sum())} ({s[fd].mean():.0%})' for fd in FUNDS})
pd.DataFrame([{'group': g, 'n': len(s), **{f'{fd}_agreements': int(s[fd].sum()) for fd in FUNDS}, **{f'{fd}_share': round(s[fd].mean(), 4) for fd in FUNDS}}
              for g, s in [('All new hospitals', d), ('C-F overnight surgical', d[d.grp == 'C-F']), ('G day', d[d.grp == 'G']), ('A-B mental health / rehab', d[d.grp == 'A-B'])]]
             ).to_csv(f'{tab}/new_hospitals_by_type.csv', index=False)
P('Paired, same hospitals (exact McNemar):'); prow = []
for fd in FUNDS[1:]:
    a = int(((d[fd] == 1) & (d.MBP == 0)).sum()); b = int(((d[fd] == 0) & (d.MBP == 1)).sum()); n = a + b
    p = min(1, 2 * sum(comb(n, i) for i in range(min(a, b) + 1)) / 2 ** n) if n else 1
    P(f'  {fd}: {fd}-only {a}, Medibank-only {b}, p={p:.4f}'); prow.append({'comparator': fd, 'comparator_only': a, 'medibank_only': b, 'exact_mcnemar_p': p})
pd.DataFrame(prow).to_csv(f'{tab}/paired_tests.csv', index=False)
P('By year first listed (Oct 2026 status): n, Medibank, Bupa/HCF/nib avg')
d['comp'] = d[['BUP', 'HCF', 'NIB']].mean(axis=1)
yrows = []
for y, s in d.groupby('year'):
    P(f'  {y}: n={len(s)} MBP {s.MBP.mean():.0%} comp {s.comp.mean():.0%} gap {100*(s.comp.mean()-s.MBP.mean()):+.0f}')
    yrows.append({'year_first_listed': y, 'n': len(s), 'medibank_share': round(s.MBP.mean(), 4), 'bupa_hcf_nib_avg_share': round(s.comp.mean(), 4),
                  **{f'{fd}_share': round(s[fd].mean(), 4) for fd in FUNDS}})
pd.DataFrame(yrows).to_csv(f'{tab}/year_cohorts_chart_data.csv', index=False)
pre, post = d[d.year < 2023], d[d.year >= 2023]
P(f'  listed before 2023: n={len(pre)} MBP {pre.MBP.mean():.0%} comp {pre.comp.mean():.0%} | 2023 on: n={len(post)} MBP {post.MBP.mean():.0%} comp {post.comp.mean():.0%}')
g = (d.comp - d.MBP).values; m = (d.year >= 2023).values; obs = g[m].mean() - g[~m].mean()
rng = np.random.default_rng(11); perm = np.array([(lambda q: g[q].mean() - g[~q].mean())(rng.permutation(m)) for _ in range(50000)])
P(f'  change in gap {obs*100:+.1f} pts, permutation p={(perm >= obs - 1e-12).mean():.4f} (fixed 2023 split)')
dates = first[new].values; splits = sorted(set(dates))[1:]
def best(gv): return max(gv[dates >= s].mean() - gv[dates < s].mean() for s in splits if 4 <= (dates >= s).sum() <= len(gv) - 4)
b0 = best(g); pm = np.mean([best(rng.permutation(g)) >= b0 - 1e-12 for _ in range(4000)])
P(f'  scan over every split: best change {b0*100:+.1f} pts, scan-adjusted p={pm:.3f}')
onc = d[loc.loc[new, 'name'].str.contains('CANCER|ONCOLOG|HAEMATOLOG|GENESISCARE|INFUSION|CHEMO', case=False).values]
P(f'Oncology / infusion day units among new hospitals: {len(onc)}', {fd: int(onc[fd].sum()) for fd in FUNDS})
nonc = d.drop(index=onc.index); P(f'Excluding them (n={len(nonc)}):', {fd: f'{nonc[fd].mean():.0%}' for fd in FUNDS})
n26 = [i for i in first.index if first[i].year == 2026 and last[i] == END and i not in MB]
c26 = pd.DataFrame({fd: W[fd].loc[n26, END] for fd in FUNDS}); c26['comp'] = c26[['BUP', 'HCF', 'NIB']].mean(axis=1)
P(f'Hospitals first listed in 2026 (under 12 months, excl. Medibank sites): n={len(n26)} MBP {int(c26.MBP.sum())} ({c26.MBP.mean():.0%}) Bupa/HCF/nib avg {c26.comp.mean():.0%}')
c26.assign(name=loc.loc[n26, 'name'], state=loc.loc[n26, 'state'], cat=loc.loc[n26, 'cat'], first_listed=first[n26].dt.date).to_csv(f'{tab}/cohort_2026_under_12_months.csv', index_label='prov')
d.assign(name=loc.loc[new, 'name'], state=loc.loc[new, 'state'], first_listed=first[new].dt.date, oncology_infusion=d.index.isin(onc.index).astype(int)
         ).drop(columns='comp')[['name', 'state', 'cat', 'grp', 'first_listed', 'year', 'oncology_infusion'] + FUNDS].sort_values(['first_listed', 'name']
         ).to_csv(f'{tab}/new_hospitals_81.csv', index_label='prov')
P('Medibank-interest hospitals, Oct 2026 status:')
for i in MB: P(f'  {loc.at[i,"name"]}:', {fd: (None if pd.isna(W[fd].at[i, END]) else int(W[fd].at[i, END])) for fd in FUNDS})
pd.DataFrame([{'prov': i, 'name': loc.at[i, 'name'], **{fd: (None if pd.isna(W[fd].at[i, END]) else int(W[fd].at[i, END])) for fd in FUNDS}} for i in MB]
             ).to_csv(f'{tab}/medibank_sites_status_oct2026.csv', index=False)
open(f'{out}/briefing_figures.txt', 'w').write('\n'.join(out_lines))
