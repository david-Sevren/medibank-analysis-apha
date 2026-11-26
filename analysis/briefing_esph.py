"""East Sydney Private comparison used in the briefing (replaces APHA's withdrawn Aug 2025 54.89% figure).
Cross-section, as APHA framed it: every hospital listed within 30 km of East Sydney Private at each date
(East Sydney itself excluded), share with a Medibank agreement, Aug 2020 and Jul 2025.
Shown including and excluding the other Medibank-interest hospitals. Same method as analysis/recheck.py."""
import sys, numpy as np, pandas as pd
f = pd.read_csv(sys.argv[1], dtype={'prov': str}, parse_dates=['snapshot'])
MB = ['0017500W', '0037140T', '0017360L', '0065780W', '0095140A', '0015550A', '0056310K']
m = f[f.fund == 'MBP'] if 'fund' in f else f
c = m[m.prov == '0017500W'].iloc[0]
hav = lambda a, b: 12742 * np.arcsin(np.sqrt(np.sin(np.radians(a - c.lat) / 2) ** 2 + np.cos(np.radians(c.lat)) * np.cos(np.radians(a)) * np.sin(np.radians(b - c.lon) / 2) ** 2))
m = m.assign(km=hav(m.lat, m.lon))
for excl in (False, True):
    out = []
    for when in ['2020-08-01', '2025-07-01']:
        s = m[(m.snapshot == when) & (m.km <= 30) & (m.prov != '0017500W') & ~(m.prov.isin(MB) & excl)]
        out.append(f'{when[:7]}: {int(s.agree.sum())} of {len(s)} ({s.agree.mean():.1%})')
    print(('excl. other Medibank sites' if excl else 'incl. other Medibank sites') + ' | ' + ' -> '.join(out))
