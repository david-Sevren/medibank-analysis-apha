"""Overnight surgical hospitals (second-tier C-F): named events near each surgical site, entrants, national clustering."""
import sys, numpy as np, pandas as pd
p = pd.read_csv(sys.argv[1], dtype={'prov': str}, parse_dates=['snapshot']); out = sys.argv[2]
S = sorted(p.snapshot.unique()); END = S[-1]
loc = p.sort_values('snapshot').groupby('prov')[['name', 'lat', 'lon', 'state', 'cat']].last()
w = p.pivot(index='prov', columns='snapshot', values='agree')
MB = ['0017500W', '0037140T', '0017360L', '0065780W', '0095140A', '0015550A', '0056310K']
CDEF = loc.index[loc.cat.isin(list('CDEF')) & ~loc.index.isin(MB)]
hav = lambda a, b, c, d: 12742 * np.arcsin(np.sqrt(np.sin(np.radians(c - a) / 2) ** 2 + np.cos(np.radians(a)) * np.cos(np.radians(c)) * np.sin(np.radians(d - b) / 2) ** 2))
sites = {'0017500W': 'East Sydney Private', '0037140T': 'Adeney Private', '0017360L': 'Macquarie Uni Hospital (TOI)', '0065780W': 'Western Hospital'}
first = w.notna().idxmax(axis=1); last = w.notna()[w.columns[::-1]].idxmax(axis=1)
rows = []
for c, lab in sites.items():
    d = pd.Series(hav(loc.at[c, 'lat'], loc.at[c, 'lon'], loc.lat.values, loc.lon.values), index=loc.index)
    for i in CDEF[d[CDEF] <= 50]:
        s = w.loc[i].dropna(); evs = []
        if first[i] > S[0]: evs.append((first[i], 'ENTERED ' + ('with' if s.iloc[0] == 1 else 'WITHOUT') + ' agreement'))
        prev = None
        for t, v in s.items():
            if prev is not None and v != prev: evs.append((t, 'LOST' if v == 0 else 'GAINED'))
            prev = v
        if last[i] < END: evs.append((last[i], 'EXITED (' + ('had' if s.iloc[-1] == 1 else 'no') + ' agreement)'))
        for t, e in evs:
            rows.append(dict(site=lab, km=round(d[i], 1), name=loc.at[i, 'name'], cat=loc.at[i, 'cat'], event=e, date=t.date(), agree_now=w.at[i, END]))
det = pd.DataFrame(rows).sort_values(['site', 'date']); det.to_csv(f'{out}/events_within_50km_CDEF.csv', index=False)
pd.set_option('display.width', 250); print(det.to_string(index=False))
# national clustering of losses among C-F
near = pd.Series(False, index=loc.index)
for c in sites: near |= pd.Series(hav(loc.at[c, 'lat'], loc.at[c, 'lon'], loc.lat.values, loc.lon.values), index=loc.index) <= 50
lost = []
for i in CDEF:
    s = w.loc[i].dropna()
    for (t0, a), (t1, b) in zip(list(s.items())[:-1], list(s.items())[1:]):
        if a == 1 and b == 0: lost.append((i, t1.date(), loc.at[i, 'name'], loc.at[i, 'state'], near[i]))
print('\nC-F hospitals near a Medibank surgical site:', round(near[CDEF].mean(), 3), 'of', len(CDEF))
print('C-F losses nationally:'); print(pd.DataFrame(lost, columns=['prov', 'date', 'name', 'state', 'near']).to_string(index=False))
ent = CDEF[first[CDEF] > S[0]]
e = pd.DataFrame({'near': near[ent], 'at_entry': [w.loc[i].dropna().iloc[0] for i in ent], 'now': w.loc[ent, END]})
print('\nC-F entrants:'); print(e.groupby('near').agg(n=('at_entry', 'size'), at_entry=('at_entry', 'mean'), now=('now', 'mean')).round(2))
nat = p[p.prov.isin(CDEF)].groupby('snapshot').agree.agg(['size', 'mean']); nat.to_csv(f'{out}/national_trend_CDEF.csv')
print(nat.iloc[[0, 8, 12, 18, 24, 25, 26]].round(3))
