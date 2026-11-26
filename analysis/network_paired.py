"""Paired comparison on the SAME new hospitals (listed >=12 months, still listed Oct 2026):
Medibank vs each fund. Exact McNemar (binomial on discordant pairs), two-sided."""
import sys, pandas as pd
from math import comb
a = pd.read_csv(sys.argv[1]); out = sys.argv[2]
a = a[a.months_listed >= 12]
rows = []
for grp, g in [('All new hospitals', a), ('Overnight surgical (C-F)', a[a.group == 'Overnight surgical (C-F)']), ('Day hospital (G)', a[a.group == 'Day hospital (G)'])]:
    for fd in ['BUP', 'HCF', 'NIB', 'HBF', 'AUF']:
        only_other = int(((g[f'{fd}_oct26'] == 1) & (g.MBP_oct26 == 0)).sum()); only_mbp = int(((g[f'{fd}_oct26'] == 0) & (g.MBP_oct26 == 1)).sum())
        n = only_other + only_mbp; k = min(only_other, only_mbp)
        p = min(1.0, 2 * sum(comb(n, i) for i in range(0, k + 1)) / 2 ** n) if n else 1.0
        rows.append(dict(group=grp, hospitals=len(g), comparator=fd, medibank_share=g.MBP_oct26.mean(), comparator_share=g[f'{fd}_oct26'].mean(),
                         comparator_only=only_other, medibank_only=only_mbp, exact_mcnemar_p=p))
r = pd.DataFrame(rows); r.to_csv(f'{out}/network_paired_tests.csv', index=False)
pd.set_option('display.width', 200); print(r.round(3).to_string(index=False))
