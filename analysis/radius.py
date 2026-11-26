"""Regional contracting analysis around Medibank-interest hospitals.

For each Medibank-interest hospital (centre) and event date:
  - neighbours = other hospitals within R km (excludes all Medibank-interest hospitals)
  - category filter: surgical centres compare against non-psych, non-rehab hospitals (cats C-G);
    mental health centres compare against psych hospitals (cat A). 'all' = no filter.
  - cross-section: share of neighbours with a Medibank agreement at each snapshot
  - stable cohort: neighbours present at both baseline and end snapshot; change in share
  - control: same stable-cohort change for every hospital outside the radius (national)
  - placebo: same calculation centred on every other hospital in the dataset; percentile rank
Outputs CSVs to outputs/.
"""
import sys
import numpy as np, pandas as pd

panel_path, outdir = sys.argv[1], sys.argv[2]
p = pd.read_csv(panel_path, dtype={'prov': str, 'postcode': str}, parse_dates=['snapshot'])
SNAPS = sorted(p.snapshot.unique())
END = SNAPS[-1]

MB = {  # provider: (label, kind)
    '0017500W': ('East Sydney Private', 'surgical'),
    '0037140T': ('Adeney Private', 'surgical'),
    '0017360L': ('Macquarie Uni Hospital (TOI)', 'surgical'),
    '0065780W': ('Western Hospital', 'surgical'),
    '0095140A': ('Deakin Private (iMH)', 'mental'),
    '0015550A': ('Hirondelle (iMH)', 'mental'),
    '0056310K': ('Nundah (iMH)', 'mental'),
}
# Adeney and Nundah did not exist before opening; use the site coordinates from the file.
EVENTS = [  # (prov, event label, event date)
    ('0017500W', 'Medibank buys 49% (Aug 2020)', '2020-08-01'),
    ('0037140T', 'JV announced (Mar 2021)', '2021-03-15'),
    ('0037140T', 'Hospital opens (Feb 2025)', '2025-02-10'),
    ('0017360L', 'TOI JV announced (Sep 2022)', '2022-09-06'),
    ('0017360L', 'TOI opens (Jan 2024)', '2024-01-29'),
    ('0065780W', 'JV takes over (Nov 2024)', '2024-11-01'),
    ('0095140A', 'Opens under iMH (Mar 2023)', '2023-03-03'),
    ('0015550A', 'iMH JV formed (Mar 2023)', '2023-03-15'),
    ('0015550A', 'Reopens as mental health (Jan 2024)', '2024-01-15'),
    ('0056310K', 'Opens (Jan 2025)', '2025-01-15'),
]
RADII = [10, 25, 50, 100, 150]

loc = p.sort_values('snapshot').groupby('prov')[['name', 'lat', 'lon', 'state', 'postcode', 'cat']].last()
# Use the most recent category for filtering (Hirondelle is mis-coded B in the file; it is a centre, not a neighbour).
wide = p.pivot(index='prov', columns='snapshot', values='agree')


def hav(lat1, lon1, lat2, lon2):
    r = 6371.0
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 2 * r * np.arcsin(np.sqrt(a))


def baseline_for(ev):
    ev = pd.Timestamp(ev)
    before = [s for s in SNAPS if s <= ev]
    return before[-1] if before else SNAPS[0]


def eligible(kind, filt):
    if filt == 'all':
        return loc.index
    if kind == 'surgical':
        return loc.index[~loc.cat.isin(['A', 'B'])]
    return loc.index[loc.cat.eq('A')]


def cohort_change(ids, base, end=END):
    sub = wide.loc[wide.index.intersection(ids), [base, end]].dropna()
    if len(sub) == 0:
        return np.nan, np.nan, 0, 0, 0
    return sub[base].mean(), sub[end].mean(), len(sub), int(((sub[base] == 1) & (sub[end] == 0)).sum()), int(((sub[base] == 0) & (sub[end] == 1)).sum())


mb_ids = set(MB)
pool_all = loc.index.difference(list(mb_ids))
results, series, placebo_rows = [], [], []

for prov, evlabel, evdate in EVENTS:
    label, kind = MB[prov]
    c = loc.loc[prov]
    d = pd.Series(hav(c.lat, c.lon, loc.lat.values, loc.lon.values), index=loc.index)
    base = baseline_for(evdate)
    for filt in ['relevant', 'all']:
        pool = pool_all.intersection(eligible(kind, filt))
        areas = [(f'{r} km', d[pool][d[pool] <= r].index) for r in RADII]
        areas.append(('same postcode', pool[loc.loc[pool, 'postcode'].eq(c.postcode)]))
        areas.append(('same state', pool[loc.loc[pool, 'state'].eq(c.state)]))
        for area, ids in areas:
            b, e, n, lost, gained = cohort_change(ids, base)
            ctrl = pool.difference(ids)
            cb, ce, cn, _, _ = cohort_change(ctrl, base)
            # cross-section at baseline and end (includes entrants / exits)
            xb = wide.loc[ids, base].dropna(); xe = wide.loc[ids, END].dropna()
            results.append(dict(centre=label, event=evlabel, baseline=base.date(), filter=filt, area=area,
                                cohort_n=n, cohort_base=b, cohort_end=e, cohort_chg_pp=(e - b) * 100 if n else np.nan,
                                lost=lost, gained=gained, ctrl_n=cn, ctrl_chg_pp=(ce - cb) * 100,
                                diff_pp=((e - b) - (ce - cb)) * 100 if n else np.nan,
                                xsec_base_n=len(xb), xsec_base=xb.mean() if len(xb) else np.nan,
                                xsec_end_n=len(xe), xsec_end=xe.mean() if len(xe) else np.nan))
            if filt == 'relevant' and area in ('25 km', '50 km', '100 km'):
                for s in SNAPS:
                    x = wide.loc[ids, s].dropna(); y = wide.loc[ctrl, s].dropna()
                    series.append(dict(centre=label, event=evlabel, area=area, snapshot=s.date(),
                                       local_n=len(x), local_rate=x.mean() if len(x) else np.nan,
                                       national_rate=y.mean()))
        # placebo: every hospital in the dataset (excluding MB sites) as a pseudo-centre, same window and filter
        if filt == 'relevant':
            for r in [25, 50, 100]:
                real = [x for x in results if x['centre'] == label and x['event'] == evlabel and x['filter'] == filt and x['area'] == f'{r} km'][0]
                vals = []
                for q in pool_all:
                    dq = pd.Series(hav(loc.at[q, 'lat'], loc.at[q, 'lon'], loc.lat.values, loc.lon.values), index=loc.index)
                    ids = dq[pool][dq[pool] <= r].index.difference([q])
                    b, e, n, _, _ = cohort_change(ids, base)
                    if n >= max(5, real['cohort_n'] * 0.5):
                        vals.append((e - b) * 100)
                vals = np.array(vals)
                pct = (vals <= real['cohort_chg_pp']).mean() * 100 if len(vals) else np.nan
                placebo_rows.append(dict(centre=label, event=evlabel, radius_km=r, real_chg_pp=real['cohort_chg_pp'],
                                         real_n=real['cohort_n'], placebo_centres=len(vals),
                                         placebo_median_pp=np.median(vals) if len(vals) else np.nan,
                                         pct_of_placebos_as_bad_or_worse=pct))

pd.DataFrame(results).to_csv(f'{outdir}/radius_results.csv', index=False)
pd.DataFrame(series).to_csv(f'{outdir}/radius_series.csv', index=False)
pd.DataFrame(placebo_rows).to_csv(f'{outdir}/placebo.csv', index=False)
print('done', len(results), len(series), len(placebo_rows))
