"""Test for a change in Medibank's new-hospital contracting relative to Bupa/HCF/nib, by date first listed.
Hospital-level gap = mean(BUP,HCF,NIB at Oct 2026) - MBP at Oct 2026; still listed, listed >=12 months.
(a) exact permutation: listed before 2023 vs 2023 onward; (b) scan of every split quarter (reported with
a permutation p that accounts for scanning: max-statistic over all splits)."""
import sys, numpy as np, pandas as pd
c = pd.read_csv(sys.argv[1], parse_dates=['first']); out = sys.argv[2]
END = pd.Timestamp('2026-10-01')
c = c[c.still & ((END - c['first']).dt.days >= 365)].copy()
c['comp'] = c[['BUP_oct26', 'HCF_oct26', 'NIB_oct26']].mean(axis=1); c['gap'] = c.comp - c.MBP_oct26
rng = np.random.default_rng(7)
def split_stat(mask, g): return g[mask].mean() - g[~mask].mean()
res = []
for lab, sub in [('All new hospitals', c), ('Overnight surgical (C-F)', c[c.g == 'C-F']), ('Day hospitals (G)', c[c.g == 'G'])]:
    g = sub.gap.values; d = sub['first'].values
    post = sub['first'] >= '2023-01-01'
    obs = split_stat(post.values, g)
    perm = np.array([split_stat(rng.permutation(post.values), g) for _ in range(20000)])
    p_fixed = (perm >= obs - 1e-12).mean()
    splits = sorted(sub['first'].unique())[1:]
    def best(gv):
        vals = [(split_stat(d >= s, gv), s) for s in splits if 4 <= (d >= s).sum() <= len(gv) - 4]
        return max(vals)
    bstat, bsplit = best(g)
    pmax = np.mean([best(rng.permutation(g))[0] >= bstat - 1e-12 for _ in range(3000)])
    res.append(dict(group=lab, n=len(sub), n_pre2023=int((~post).sum()), n_2023on=int(post.sum()),
                    mbp_pre=sub[~post].MBP_oct26.mean(), comp_pre=sub[~post].comp.mean(),
                    mbp_post=sub[post].MBP_oct26.mean(), comp_post=sub[post].comp.mean(),
                    gap_pre_pp=sub[~post].gap.mean() * 100, gap_post_pp=sub[post].gap.mean() * 100,
                    change_pp=obs * 100, perm_p_2023_split=p_fixed,
                    best_split=pd.Timestamp(bsplit).date(), best_change_pp=bstat * 100, scan_adjusted_p=pmax))
r = pd.DataFrame(res); r.to_csv(f'{out}/timing_break_tests.csv', index=False)
pd.set_option('display.width', 250); print(r.round(3).to_string(index=False))
