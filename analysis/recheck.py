"""Independent re-derivation of headline numbers straight from the raw xlsx (no shared code with radius.py/detail.py)."""
import sys, math, openpyxl, datetime as dt
wb = openpyxl.load_workbook(sys.argv[1], read_only=True); ws = wb.active
rows = list(ws.iter_rows(values_only=True))[1:]
P = lambda s: dt.datetime.strptime(s, '%b %d, %Y')
data = {}  # (prov, fromdate) -> (agree, lat, lon)
for name, f, t, lat, lon, st, pc, prov, cat, ag in rows:
    f2, t2 = P(f), P(t)
    if t2 < f2: continue
    data[(prov, f2)] = (ag, lat, lon, (cat or '?')[0])
def km(a, b, c, d):
    a, b, c, d = map(math.radians, (a, b, c, d))
    return 12742 * math.asin(math.sqrt(math.sin((c - a) / 2) ** 2 + math.cos(a) * math.cos(c) * math.sin((d - b) / 2) ** 2))
def share(centre, when, r, excl_psych_rehab=False):
    lat0, lon0 = [v[1:3] for k, v in data.items() if k[0] == centre][0]
    xs = [v[0] for k, v in data.items() if k[1] == when and k[0] != centre and km(lat0, lon0, v[1], v[2]) <= r
          and not (excl_psych_rehab and v[3] in 'AB')]
    return sum(xs), len(xs)
D = dt.datetime
for when in [D(2020, 8, 1), D(2025, 7, 1)]:
    print('ESPH 30km all cats', when.date(), share('0017500W', when, 30))
nat = lambda when: (sum(v[0] for k, v in data.items() if k[1] == when), sum(1 for k in data if k[1] == when))
for w in [D(2020, 8, 1), D(2023, 4, 1), D(2026, 7, 1), D(2026, 10, 1)]: print('national', w.date(), nat(w), round(nat(w)[0] / nat(w)[1] * 100, 2))
for p in ['0037140T', '0095140A', '0056310K', '0017500W', '0017360L', '0065780W', '0015550A']:
    print(p, [v[0] for k, v in sorted(data.items()) if k[0] == p])
