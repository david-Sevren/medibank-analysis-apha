"""Build an auditable workbook: hospital-level sheets + summary formulas (COUNTIFS) over them."""
import sys, pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
f = pd.read_csv(sys.argv[1], dtype={'prov': str, 'postcode': str}, parse_dates=['snapshot']); out = sys.argv[2]
MB = ['0017500W', '0037140T', '0017360L', '0065780W', '0095140A', '0015550A', '0056310K']  # Medibank-interest hospitals, excluded from summary figures
FUNDS = ['MBP', 'BUP', 'HCF', 'NIB', 'HBF', 'AUF']
NAMES = {'MBP': 'Medibank', 'BUP': 'Bupa', 'HCF': 'HCF', 'NIB': 'nib', 'HBF': 'HBF', 'AUF': 'Australian Unity'}
S = sorted(f.snapshot.unique()); F0, END = S[0], S[-1]
loc = f.sort_values('snapshot').groupby('prov')[['name', 'state', 'postcode', 'cat']].last()
grp = lambda c: 'Overnight surgical (C-F)' if c in 'CDEF' else ('Day hospital (G)' if c == 'G' else ('Mental health / rehab (A-B)' if c in 'AB' else 'Uncategorised'))
loc['group'] = loc.cat.map(grp)
W = {fd: f[f.fund == fd].pivot(index='prov', columns='snapshot', values='agree') for fd in FUNDS}
pres = W['MBP'].notna(); first = pres.idxmax(axis=1); last = pres[pres.columns[::-1]].idxmax(axis=1)

wb = Workbook(); B = Font(bold=True); H = PatternFill('solid', fgColor='EEEEEE')
def header(ws, cols, row=1):
    for j, c in enumerate(cols, 1):
        x = ws.cell(row=row, column=j, value=c); x.font = B; x.fill = H; x.alignment = Alignment(wrap_text=True, vertical='top')
def widths(ws, w):
    for j, v in enumerate(w, 1): ws.column_dimensions[get_column_letter(j)].width = v

# ---- Sheet: Network (every hospital, status Aug 2020 and Oct 2026) ----
net = wb.create_sheet('Network Aug20 v Oct26')
cols = ['Provider no.', 'Hospital', 'State', 'Postcode', '2nd-tier cat', 'Group', 'Listed Aug 2020', 'Listed Oct 2026'] + \
       [f'{NAMES[fd]} Aug 2020' for fd in FUNDS] + [f'{NAMES[fd]} Oct 2026' for fd in FUNDS] + ['Medibank-interest hospital']
header(net, cols)
ids = sorted(set(W['MBP'].index[W['MBP'][F0].notna()]) | set(W['MBP'].index[W['MBP'][END].notna()]), key=lambda i: loc.at[i, 'name'].lower())
for r, i in enumerate(ids, 2):
    row = [i, loc.at[i, 'name'], loc.at[i, 'state'], loc.at[i, 'postcode'], loc.at[i, 'cat'], loc.at[i, 'group'],
           int(pd.notna(W['MBP'].at[i, F0])), int(pd.notna(W['MBP'].at[i, END]))]
    row += [None if pd.isna(W[fd].at[i, F0]) else int(W[fd].at[i, F0]) for fd in FUNDS]
    row += [None if pd.isna(W[fd].at[i, END]) else int(W[fd].at[i, END]) for fd in FUNDS] + [int(i in MB)]
    for j, v in enumerate(row, 1): net.cell(row=r, column=j, value=v)
NET_N = len(ids) + 1; net.freeze_panes = 'C2'; widths(net, [12, 40, 7, 9, 8, 26, 9, 9] + [11] * 13)

# ---- Sheet: New hospitals (first listed after Aug 2020, still listed Oct 2026) ----
nh = wb.create_sheet('New hospitals')
cols = ['Provider no.', 'Hospital', 'State', 'Postcode', '2nd-tier cat', 'Group', 'First listed', 'Months listed at Oct 2026', 'Listed 12+ months'] + \
       [f'{NAMES[fd]} agreement Oct 2026' for fd in FUNDS] + [f'{NAMES[fd]} first shown with agreement' for fd in FUNDS] + ['Year first listed', 'Medibank agreement within 12 months of listing (listed 12+ months only)', 'Medibank-interest hospital']
header(nh, cols)
nids = sorted([i for i in first.index if first[i] > F0 and last[i] == END], key=lambda i: (first[i], loc.at[i, 'name'].lower()))
for r, i in enumerate(nids, 2):
    m = round((END - first[i]).days / 30.44, 1)
    row = [i, loc.at[i, 'name'], loc.at[i, 'state'], loc.at[i, 'postcode'], loc.at[i, 'cat'], loc.at[i, 'group'], first[i].date(), m, f'=IF(H{r}>=12,1,0)']
    row += [int(W[fd].at[i, END]) for fd in FUNDS]
    for fd in FUNDS:
        s = W[fd].loc[i].dropna(); g = s[s == 1]; row.append(g.index[0].date() if len(g) else None)
    row += [f'=YEAR(G{r})', f'=IF(H{r}<12,"",IF(AND(P{r}<>"",P{r}-G{r}<=366),1,0))', int(i in MB)]
    for j, v in enumerate(row, 1):
        c = nh.cell(row=r, column=j, value=v)
        if j == 7 or 16 <= j <= 21: c.number_format = 'mmm yyyy'
NH_N = len(nids) + 1; nh.freeze_panes = 'C2'; widths(nh, [12, 44, 7, 9, 8, 26, 11, 10, 9] + [11] * 12 + [9, 14, 11])

# ---- Sheet: Status changes (every gain / loss among continuing hospitals) ----
sc = wb.create_sheet('Status changes')
header(sc, ['Fund', 'Fund name', 'Provider no.', 'Hospital', 'State', 'Group', 'Quarter starting', 'Change', 'Medibank-interest hospital'])
r = 2
for fd in FUNDS:
    w = W[fd]
    for a, b in zip(S[:-1], S[1:]):
        both = w[[a, b]].dropna()
        for i in both.index[(both[a] != both[b])]:
            for j, v in enumerate([fd, NAMES[fd], i, loc.at[i, 'name'], loc.at[i, 'state'], loc.at[i, 'group'], b.date(),
                                   'Gained' if both.at[i, b] == 1 else 'Lost', int(i in MB)], 1):
                c = sc.cell(row=r, column=j, value=v)
                if j == 7: c.number_format = 'mmm yyyy'
            r += 1
SC_N = r - 1; sc.freeze_panes = 'A2'; widths(sc, [7, 16, 12, 44, 7, 26, 11, 9, 11])

# ---- Sheet: Summary (formulas only) ----
sm = wb.create_sheet('Summary', 0)
sm['A1'] = 'Is Medibank growing its hospital network as fast as other funds?'; sm['A1'].font = Font(bold=True, size=13)
sm['A2'] = 'Every figure below is a formula over the hospital-level sheets in this workbook. Click a cell to see how it is worked out.'
sm['A3'] = "Medibank's seven part-owned hospitals are flagged in each sheet's last column and left out of every figure below, matching the briefing."
NETR = f"'Network Aug20 v Oct26'"; NHR = "'New hospitals'"; SCR = "'Status changes'"
row = 4; sm.cell(row=row, column=1, value='1. Network size: hospitals with an agreement').font = B; row += 1
header(sm, ['Fund', 'Agreements Aug 2020', 'Agreements Oct 2026', 'Change', 'Share of listed Aug 2020', 'Share of listed Oct 2026', 'Change (pts)'], row); row += 1
for k, fd in enumerate(FUNDS):
    ca = get_column_letter(9 + k); co = get_column_letter(15 + k)
    sm.cell(row=row, column=1, value=NAMES[fd])
    sm.cell(row=row, column=2, value=f'=SUMIFS({NETR}!{ca}2:{ca}{NET_N},{NETR}!U2:U{NET_N},0)')
    sm.cell(row=row, column=3, value=f'=SUMIFS({NETR}!{co}2:{co}{NET_N},{NETR}!U2:U{NET_N},0)')
    sm.cell(row=row, column=4, value=f'=C{row}-B{row}')
    sm.cell(row=row, column=5, value=f'=B{row}/SUMIFS({NETR}!G2:G{NET_N},{NETR}!U2:U{NET_N},0)').number_format = '0.0%'
    sm.cell(row=row, column=6, value=f'=C{row}/SUMIFS({NETR}!H2:H{NET_N},{NETR}!U2:U{NET_N},0)').number_format = '0.0%'
    sm.cell(row=row, column=7, value=f'=(F{row}-E{row})*100').number_format = '+0.0;-0.0'
    row += 1
row += 1; sm.cell(row=row, column=1, value='2. Where the change came from (Aug 2020 to Oct 2026)').font = B; row += 1
header(sm, ['Fund', 'Agreements gained (existing hospitals)', 'Agreements lost (existing hospitals)', 'New hospitals with agreement Oct 2026',
            'New hospitals listed 12+ months', 'Share of those with agreement'], row); row += 1
for k, fd in enumerate(FUNDS):
    cn = get_column_letter(10 + k)
    sm.cell(row=row, column=1, value=NAMES[fd])
    sm.cell(row=row, column=2, value=f'=COUNTIFS({SCR}!A2:A{SC_N},"{fd}",{SCR}!H2:H{SC_N},"Gained",{SCR}!I2:I{SC_N},0)')
    sm.cell(row=row, column=3, value=f'=COUNTIFS({SCR}!A2:A{SC_N},"{fd}",{SCR}!H2:H{SC_N},"Lost",{SCR}!I2:I{SC_N},0)')
    sm.cell(row=row, column=4, value=f'=SUMIFS({NHR}!{cn}2:{cn}{NH_N},{NHR}!X2:X{NH_N},0)')
    sm.cell(row=row, column=5, value=f'=SUMIFS({NHR}!I2:I{NH_N},{NHR}!X2:X{NH_N},0)')
    sm.cell(row=row, column=6, value=f'=SUMIFS({NHR}!{cn}2:{cn}{NH_N},{NHR}!I2:I{NH_N},1,{NHR}!X2:X{NH_N},0)/E{row}').number_format = '0.0%'
    row += 1
row += 1; sm.cell(row=row, column=1, value='3. New hospitals listed 12+ months: share with an agreement at Oct 2026, by type').font = B; row += 1
groups = ['Overnight surgical (C-F)', 'Day hospital (G)', 'Mental health / rehab (A-B)']
header(sm, ['Fund'] + groups, row); row += 1; g_first = row
for k, fd in enumerate(FUNDS):
    cn = get_column_letter(10 + k); sm.cell(row=row, column=1, value=NAMES[fd])
    for j, g in enumerate(groups, 2):
        sm.cell(row=row, column=j, value=f'=SUMIFS({NHR}!{cn}2:{cn}{NH_N},{NHR}!F2:F{NH_N},"{g}",{NHR}!I2:I{NH_N},1,{NHR}!X2:X{NH_N},0)/COUNTIFS({NHR}!F2:F{NH_N},"{g}",{NHR}!I2:I{NH_N},1,{NHR}!X2:X{NH_N},0)').number_format = '0%'
    row += 1
sm.cell(row=row, column=1, value='Hospitals in group')
for j, g in enumerate(groups, 2): sm.cell(row=row, column=j, value=f'=COUNTIFS({NHR}!F2:F{NH_N},"{g}",{NHR}!I2:I{NH_N},1,{NHR}!X2:X{NH_N},0)')
row += 1; sm.cell(row=row, column=1, value='Medibank rank (1 = highest of 6)')
for j in range(2, 5):
    cl = get_column_letter(j); sm.cell(row=row, column=j, value=f'=RANK({cl}{g_first},{cl}{g_first}:{cl}{g_first+5},0)')
row += 2; sm.cell(row=row, column=1, value='4. Same hospitals, head to head: new hospitals listed 12+ months').font = B; row += 1
header(sm, ['Comparator', 'Comparator has agreement, Medibank does not', 'Medibank has agreement, comparator does not', 'Exact McNemar p (from analysis/briefing_figures.py)'], row); row += 1
pt = pd.read_csv(f'{out}/briefing/paired_tests.csv').set_index('comparator')
for k, fd in enumerate(FUNDS[1:], 1):
    cn = get_column_letter(10 + k)
    sm.cell(row=row, column=1, value=NAMES[fd])
    sm.cell(row=row, column=2, value=f'=COUNTIFS({NHR}!I2:I{NH_N},1,{NHR}!{cn}2:{cn}{NH_N},1,{NHR}!J2:J{NH_N},0,{NHR}!X2:X{NH_N},0)')
    sm.cell(row=row, column=3, value=f'=COUNTIFS({NHR}!I2:I{NH_N},1,{NHR}!{cn}2:{cn}{NH_N},0,{NHR}!J2:J{NH_N},1,{NHR}!X2:X{NH_N},0)')
    pv = float(pt.at[fd, 'exact_mcnemar_p']); sm.cell(row=row, column=4, value='<0.001' if pv < 0.001 else round(pv, 3))
    row += 1
row += 1; sm.cell(row=row, column=1, value='5. When did it change? New hospitals by year first listed (agreement status at Oct 2026)').font = B; row += 1
header(sm, ['Year first listed', 'New hospitals', 'Medibank', 'Bupa / HCF / nib average', 'Gap (pts)', 'Medibank agreement within 12 months of listing'], row); row += 1
for yr in range(2021, 2027):
    V = f"{NHR}!V2:V{NH_N}"
    sm.cell(row=row, column=1, value=yr)
    sm.cell(row=row, column=2, value=f'=COUNTIFS({V},A{row},{NHR}!X2:X{NH_N},0)')
    sm.cell(row=row, column=3, value=f'=AVERAGEIFS({NHR}!J2:J{NH_N},{V},A{row},{NHR}!X2:X{NH_N},0)').number_format = '0%'
    sm.cell(row=row, column=4, value=f'=AVERAGE(AVERAGEIFS({NHR}!K2:K{NH_N},{V},A{row},{NHR}!X2:X{NH_N},0),AVERAGEIFS({NHR}!L2:L{NH_N},{V},A{row},{NHR}!X2:X{NH_N},0),AVERAGEIFS({NHR}!M2:M{NH_N},{V},A{row},{NHR}!X2:X{NH_N},0))').number_format = '0%'
    sm.cell(row=row, column=5, value=f'=(D{row}-C{row})*100').number_format = '+0;-0;0'
    sm.cell(row=row, column=6, value=f'=IFERROR(AVERAGEIFS({NHR}!W2:W{NH_N},{V},A{row},{NHR}!X2:X{NH_N},0),"too recent")').number_format = '0%'
    row += 1
for t in ['Hospitals listed 12+ months, first listed before 2023 (22): Medibank 41% vs Bupa/HCF/nib 42% (no gap). First listed from 2023 (59): 27% vs 52%. Permutation p = 0.009 for a 2023 split (analysis/briefing_figures.py).',
          'Testing every possible split date gives p = 0.039, so the break survives not knowing the date in advance. 2026 listings (under 12 months) are too recent to judge; Medibank currently leads on them (9 of 25, 36%, vs 21%).']:
    sm.cell(row=row, column=1, value=t); row += 1
row += 1; sm.cell(row=row, column=1, value='6. Near Medibank part-owned hospitals vs elsewhere').font = B; row += 1
for t in ['No measurable difference. Medibank drops existing agreements at the same rate within 50 km of its part-owned hospitals as elsewhere (4.3 vs 4.6 per 100 hospitals), the same as HCF.',
          'On comparable new overnight surgical hospitals, Medibank lags competitors near its sites (1 of 5 within 25 km) and elsewhere (Newcastle, Wollongong); the near-site difference is not statistically significant (exact permutation p = 0.11).',
          'Source: repo medibank-analysis-apha, 06-findings/01 to 03.']:
    sm.cell(row=row, column=1, value=t); row += 1
widths(sm, [30, 22, 22, 22, 22, 22, 14])

# ---- Sheet: Read me ----
rm = wb.create_sheet('Read me', 1)
lines = [
 ('Purpose', 'Tests whether Medibank has grown its hospital agreement network as fast as other major funds, and whether it behaves differently near the hospitals it part-owns.'),
 ('Source', 'Hospital agreement status by fund, 27 quarterly snapshots from 1 Aug 2020 to 1 Oct 2026 (export supplied by David du Plessis, 27 Nov 2026; file agreements_by_fund_2020-2026.csv). Fund codes: MBP Medibank, BUP Bupa, HCF, NIB nib, HBF, AUF Australian Unity (one AHSA fund).'),
 ('Unit', 'One row per hospital (Commonwealth hospital provider number). Agreement = 1 means the fund is shown with a hospital purchaser-provider agreement for that quarter.'),
 ('Network sheet', 'Every hospital listed in Aug 2020 or Oct 2026, with each fund\'s status at both dates. Blank = hospital not listed at that date.'),
 ('New hospitals sheet', 'Every hospital first listed after Aug 2020 and still listed in Oct 2026. "First shown with agreement" is the first quarter the fund is shown with an agreement.'),
 ('Status changes sheet', 'Every quarter-to-quarter change in agreement status for hospitals listed in both quarters.'),
 ('Medibank-interest hospitals', 'East Sydney Private, Adeney Private, Macquarie University Hospital (The Orthopaedic Institute), Western Hospital, iMH Deakin, Hirondelle (iMH Chatswood) and iMH Nundah. Flagged 1 in the last column of each hospital sheet and left out of every Summary figure.'),
 ('Checks done', 'Medibank rows match a separate Medibank-only export on 17,032 of 17,032 rows. No fund duplicates another (each differs on 11 to 14% of rows). 100 zero-length rows removed (end date before start date).'),
 ('Caution 1: timing', 'Funds report changes in batches (e.g. Bupa +66 in Jul 2024, nib +46 in Jul 2025). "First shown with agreement" dates show when a change was reported, not when a contract was signed. The summary uses status at Oct 2026 for that reason.'),
 ('Caution 2: Australian Unity', 'Australian Unity\'s property trust owns Wyvern Private and Sunshine Private. Its contracting is not a neutral comparator for those hospitals.'),
 ('Caution 3: counts not size', 'Agreements are counted per hospital, not weighted by beds or activity.'),
 ('Caution 4: source', 'The fund identity of the export rests on its source. It should be confirmed against each fund\'s published agreement hospital list before publication.'),
 ('Full method and code', 'Private GitHub repo david-Sevren/medibank-analysis-apha: analysis/network_growth.py, network_paired.py, build_audit_workbook.py; findings in 06-findings/.'),
]
for r, (a, b) in enumerate(lines, 1):
    rm.cell(row=r, column=1, value=a).font = B; c = rm.cell(row=r, column=2, value=b); c.alignment = Alignment(wrap_text=True, vertical='top')
widths(rm, [24, 110])
del wb['Sheet']
wb.save(f'{out}/medibank_network_audit.xlsx'); print('rows: network', NET_N - 1, 'new', NH_N - 1, 'changes', SC_N - 1)
