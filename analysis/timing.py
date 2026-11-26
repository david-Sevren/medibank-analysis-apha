"""When did Medibank's contracting change? (1) gains/losses per year by fund and hospital type;
(2) new-hospital cohorts by year first listed: Medibank uptake within 12 months (Medibank's own dates)
and every fund's status at Oct 2026 on the same hospitals."""
import sys, numpy as np, pandas as pd
f = pd.read_csv(sys.argv[1], dtype={'prov': str}, parse_dates=['snapshot']); out = sys.argv[2]
FUNDS = ['MBP', 'BUP', 'HCF', 'NIB', 'HBF', 'AUF']
S = sorted(f.snapshot.unique()); F0, END = S[0], S[-1]
loc = f.sort_values('snapshot').groupby('prov')[['name', 'cat']].last()
G = lambda c: 'C-F' if c in 'CDEF' else ('G' if c == 'G' else 'A-B/other')
loc['g'] = loc.cat.map(G)
W = {fd: f[f.fund == fd].pivot(index='prov', columns='snapshot', values='agree') for fd in FUNDS}
pres = W['MBP'].notna(); first = pres.idxmax(axis=1); last = pres[pres.columns[::-1]].idxmax(axis=1)
# (1) changes per period: all agreement gains (existing and new hospitals' first agreement) and losses
ev = []
for fd in FUNDS:
    w = W[fd]
    for a, b in zip(S[:-1], S[1:]):
        both = w[[a, b]].dropna()
        for i in both.index[both[a] != both[b]]:
            ev.append(dict(fund=fd, prov=i, q=b, kind='gain' if both.at[i, b] == 1 else 'loss', new=first[i] > F0, g=loc.at[i, 'g']))
ev = pd.DataFrame(ev); ev['half'] = ev.q.dt.year.astype(str) + np.where(ev.q.dt.month <= 6, 'H1', 'H2')
t = ev[ev.kind == 'gain'].pivot_table(index='half', columns='fund', values='prov', aggfunc='count', fill_value=0)[FUNDS]
print('GAINS per half-year (all hospitals):'); print(t.to_string())
m = ev[(ev.fund == 'MBP')].pivot_table(index='half', columns=['kind', 'g'], values='prov', aggfunc='count', fill_value=0)
print('\nMedibank gains/losses per half-year by type:'); print(m.to_string())
ev.to_csv(f'{out}/timing_status_events.csv', index=False)
# (2) cohorts
ent = [i for i in first.index if first[i] > F0]
rows = []
for i in ent:
    s = W['MBP'].loc[i].dropna(); g = s[s == 1]
    lag = (g.index[0] - first[i]).days / 30.44 if len(g) else np.nan
    r = dict(prov=i, name=loc.at[i, 'name'], g=loc.at[i, 'g'], first=first[i], year=first[i].year, still=last[i] == END,
             mbp_within12=int(len(g) > 0 and lag <= 12) if (END - first[i]).days >= 365 else np.nan, mbp_lag_m=lag)
    for fd in FUNDS: r[f'{fd}_oct26'] = W[fd].at[i, END] if last[i] == END else np.nan
    rows.append(r)
c = pd.DataFrame(rows); c.to_csv(f'{out}/timing_cohorts.csv', index=False)
pd.set_option('display.width', 220)
for lab, sub in [('ALL', c), ('C-F', c[c.g == 'C-F']), ('G', c[c.g == 'G'])]:
    agg = sub.groupby('year').agg(n=('prov', 'size'), still=('still', 'sum'), mbp_within12=('mbp_within12', 'mean'), mbp_med_lag=('mbp_lag_m', 'median'),
                                  **{f'{fd}': (f'{fd}_oct26', 'mean') for fd in FUNDS})
    agg['others_avg_BUP_HCF_NIB'] = sub.groupby('year')[['BUP_oct26', 'HCF_oct26', 'NIB_oct26']].mean().mean(axis=1)
    print(f'\nCOHORTS by year first listed: {lab}'); print(agg.round(2).to_string())
