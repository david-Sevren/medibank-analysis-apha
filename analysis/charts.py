"""Small-multiple chart: Medibank agreement share among hospitals within 50 km of each surgical site vs rest of Australia."""
import sys, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt, matplotlib.dates as md
s = pd.read_csv(sys.argv[1], parse_dates=['snapshot']); out = sys.argv[2]
SUB = sys.argv[3] if len(sys.argv) > 3 else 'surgical and day hospitals only; all listed hospitals at each snapshot'
YMIN, YMAX = (float(sys.argv[4]), float(sys.argv[5])) if len(sys.argv) > 5 else (55, 92)
keep = [('East Sydney Private', 'Medibank buys 49% (Aug 2020)', [('2020-08-01', 'Stake taken')]),
        ('Adeney Private', 'JV announced (Mar 2021)', [('2021-03-15', 'JV announced'), ('2025-02-10', 'Opens')]),
        ('Macquarie Uni Hospital (TOI)', 'TOI JV announced (Sep 2022)', [('2022-09-06', 'JV announced'), ('2024-01-29', 'Opens')]),
        ('Western Hospital', 'JV takes over (Nov 2024)', [('2024-11-01', 'JV takes over')])]
BLUE, ORANGE, INK, INK2, GRID = '#257de0', '#f47230', '#191919', '#666666', '#e6e6e6'
fig, axes = plt.subplots(2, 2, figsize=(12, 7.5), sharey=True)
for ax, (c, ev, marks) in zip(axes.flat, keep):
    d = s[(s.centre == c) & (s.event == ev) & (s.area == '50 km')]
    ax.plot(d.snapshot, d.local_rate * 100, color=BLUE, lw=2, marker='o', ms=4, label='Within 50 km (excl. Medibank sites)')
    ax.plot(d.snapshot, d.national_rate * 100, color=ORANGE, lw=2, label='Rest of Australia')
    for dt, lab in marks:
        ax.axvline(pd.Timestamp(dt), color=INK2, lw=1, ls='--')
        ax.text(pd.Timestamp(dt), YMIN + 0.5, ' ' + lab, color=INK2, fontsize=8, va='bottom')
    n0, n1 = int(d.local_n.iloc[0]), int(d.local_n.iloc[-1])
    ax.set_title(f'{c}  (n = {n0} to {n1} hospitals)', fontsize=10, color=INK, loc='left')
    ax.set_ylim(YMIN, YMAX); ax.grid(axis='y', color=GRID, lw=0.8); ax.set_axisbelow(True)
    for sp in ['top', 'right']: ax.spines[sp].set_visible(False)
    for sp in ['left', 'bottom']: ax.spines[sp].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=8); ax.xaxis.set_major_formatter(md.DateFormatter('%Y'))
axes[0, 0].set_ylabel('% of hospitals with a Medibank agreement', fontsize=9, color=INK2)
axes[1, 0].set_ylabel('% of hospitals with a Medibank agreement', fontsize=9, color=INK2)
h, l = axes[0, 0].get_legend_handles_labels()
fig.legend(h, l, loc='upper center', bbox_to_anchor=(0.5, 0.925), ncol=2, frameon=False, fontsize=9)
fig.suptitle('Medibank agreement share near its part-owned surgical hospitals, Aug 2020 to Oct 2026\n(' + SUB + ')', fontsize=11, color=INK, y=0.995)
fig.tight_layout(rect=[0, 0, 1, 0.89]); fig.savefig(out, dpi=150)
