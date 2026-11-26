"""Do funds differ in how quickly they contract NEW hospitals, near Medibank's part-owned surgical sites vs elsewhere?

Entrant = hospital first listed after the first snapshot.
Near    = within R km of a Medibank surgical site AND first listed after that site's event date
          (ESPH Aug 2020, Adeney JV Mar 2021, TOI JV Sep 2022, Western Nov 2024).
Metrics per fund: contracted at entry; contracted at last snapshot (if still listed);
                  contracted within 12 months (entrants observed for >= 12 months).
Difference-in-differences: (Medibank - other funds) near  minus  (Medibank - other funds) elsewhere.
Also: losses among continuing hospitals by fund, near vs elsewhere.
"""
import sys, numpy as np, pandas as pd

panel, out = sys.argv[1], sys.argv[2]
R = float(sys.argv[3]) if len(sys.argv) > 3 else 50
f = pd.read_csv(panel, dtype={'prov': str}, parse_dates=['snapshot'])
S = sorted(f.snapshot.unique()); FIRST, END = S[0], S[-1]
FUNDS = ['MBP', 'BUP', 'HCF', 'NIB', 'HBF', 'AUF']
loc = f.sort_values('snapshot').groupby('prov')[['name', 'lat', 'lon', 'state', 'cat']].last()
MB = ['0017500W', '0037140T', '0017360L', '0065780W', '0095140A', '0015550A', '0056310K']
SITES = {'0017500W': ('East Sydney Private', '2020-08-01'), '0037140T': ('Adeney', '2021-03-15'),
         '0017360L': ('TOI (Macquarie)', '2022-09-06'), '0065780W': ('Western Hospital', '2024-11-01')}
hav = lambda a, b, c, d: 12742 * np.arcsin(np.sqrt(np.sin(np.radians(c - a) / 2) ** 2 + np.cos(np.radians(a)) * np.cos(np.radians(c)) * np.sin(np.radians(d - b) / 2) ** 2))
w = {fd: f[f.fund == fd].pivot(index='prov', columns='snapshot', values='agree') for fd in FUNDS}
present = w['MBP'].notna()
first = present.idxmax(axis=1); last = present[present.columns[::-1]].idxmax(axis=1)

ent = loc.loc[first[first > FIRST].index].copy()
ent = ent[~ent.index.isin(MB)]
ent['first'] = first[ent.index]; ent['last'] = last[ent.index]
ent['site'] = ''; ent['km'] = np.nan
for c, (lab, ev) in SITES.items():
    d = pd.Series(hav(loc.at[c, 'lat'], loc.at[c, 'lon'], ent.lat.values, ent.lon.values), index=ent.index)
    hit = (d <= R) & (ent['first'] > pd.Timestamp(ev)) & (ent.km.isna() | (d < ent.km))
    ent.loc[hit, 'site'] = lab; ent.loc[hit, 'km'] = d[hit].round(1)
ent['near'] = ent.site != ''

def metrics(fd, ids):
    W = w[fd].loc[ids]
    at_entry = np.array([W.at[i, ent.at[i, 'first']] for i in ids])
    still = ent.loc[ids, 'last'] == END
    at_end = W.loc[still[still].index, END]
    obs12 = [i for i in ids if (END - ent.at[i, 'first']).days >= 365]
    within12 = [W.loc[i, [s for s in S if ent.at[i, 'first'] <= s <= ent.at[i, 'first'] + pd.Timedelta(days=365)]].max() for i in obs12]
    return dict(n=len(ids), at_entry=at_entry.mean() if len(ids) else np.nan, n_still=len(at_end), at_end=at_end.mean() if len(at_end) else np.nan,
                n_12m=len(obs12), within_12m=np.mean(within12) if obs12 else np.nan)

rows = []
for grp, mask in {'all categories': ent.index, 'overnight surgical (C-F)': ent.index[ent.cat.isin(list('CDEF'))],
                  'day hospitals (G)': ent.index[ent.cat.eq('G')]}.items():
    for where in ['near', 'elsewhere']:
        ids = [i for i in mask if ent.at[i, 'near'] == (where == 'near')]
        for fd in FUNDS:
            rows.append(dict(group=grp, where=where, fund=fd, **metrics(fd, ids)))
res = pd.DataFrame(rows); res.to_csv(f'{out}/fund_entrants_{int(R)}km.csv', index=False)

dd = []
for (grp), g in res.groupby('group'):
    for m in ['at_entry', 'at_end', 'within_12m']:
        t = g.pivot(index='where', columns='fund', values=m)
        others = t[[x for x in FUNDS if x != 'MBP']].mean(axis=1)
        gap = t['MBP'] - others
        dd.append(dict(group=grp, metric=m, mbp_near=t.at['near', 'MBP'], others_near=others['near'], mbp_else=t.at['elsewhere', 'MBP'],
                       others_else=others['elsewhere'], gap_near_pp=gap['near'] * 100, gap_else_pp=gap['elsewhere'] * 100,
                       did_pp=(gap['near'] - gap['elsewhere']) * 100))
dd = pd.DataFrame(dd); dd.to_csv(f'{out}/fund_entrants_did_{int(R)}km.csv', index=False)

# named near entrants: status by fund at entry and at end
nm = []
for i in ent.index[ent.near]:
    r = dict(site=ent.at[i, 'site'], km=ent.at[i, 'km'], name=ent.at[i, 'name'], cat=ent.at[i, 'cat'], first=ent.at[i, 'first'].date(),
             still_listed=ent.at[i, 'last'] == END)
    for fd in FUNDS:
        s = w[fd].loc[i].dropna(); g = s[s == 1]
        r[fd] = (('Y' if s.iloc[-1] == 1 else 'n') + (f" (from {g.index[0]:%b %y})" if len(g) else '')) if len(s) else ''
    nm.append(r)
nm = pd.DataFrame(nm).sort_values(['site', 'first']); nm.to_csv(f'{out}/fund_near_entrants_{int(R)}km.csv', index=False)

# losses among continuing hospitals by fund, near any surgical site vs elsewhere (all hospitals, not just entrants)
nearall = pd.Series(False, index=loc.index)
for c in SITES: nearall |= pd.Series(hav(loc.at[c, 'lat'], loc.at[c, 'lon'], loc.lat.values, loc.lon.values), index=loc.index) <= R
nearall[MB] = False
lr = []
for fd in FUNDS:
    W = w[fd]
    for where, ids in [('near', nearall[nearall].index), ('elsewhere', nearall[~nearall].index.difference(MB))]:
        X = W.loc[ids]; lost = gained = 0
        for a, b in zip(S[:-1], S[1:]):
            both = X[[a, b]].dropna(); lost += int(((both[a] == 1) & (both[b] == 0)).sum()); gained += int(((both[a] == 0) & (both[b] == 1)).sum())
        lr.append(dict(fund=fd, where=where, hospitals=len(ids), lost=lost, gained=gained,
                       lost_per_100=lost / len(ids) * 100, share_now=X[END].dropna().mean()))
lr = pd.DataFrame(lr); lr.to_csv(f'{out}/fund_losses_{int(R)}km.csv', index=False)

pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30)
print(f'Entrants: {len(ent)} | near {int(ent.near.sum())} | window {FIRST.date()} to {END.date()} | R={R} km')
print(res.round(2).to_string(index=False)); print(dd.round(1).to_string(index=False)); print(nm.to_string(index=False)); print(lr.round(2).to_string(index=False))
