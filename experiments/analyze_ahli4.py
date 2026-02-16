"""Analyze Ahli-4 quality by comparing against Ahli-1 and Ahli-2."""
from collections import Counter

orig = {
    'CS-MIN-011': {'ahli1':'D','ahli2':'A','ahli3':'C'},
    'CS-MIN-004': {'ahli1':'B','ahli2':'B','ahli3':'C'},
    'CS-JAW-006': {'ahli1':'A','ahli2':'C','ahli3':'A'},
    'CS-LIN-052': {'ahli1':'D','ahli2':'D','ahli3':'C'},
    'CS-NAS-066': {'ahli1':'A','ahli2':'C','ahli3':'A'},
    'CS-BAL-002': {'ahli1':'C','ahli2':'C','ahli3':'A'},
    'CS-NAS-010': {'ahli1':'A','ahli2':'A','ahli3':'A'},
    'CS-LIN-017': {'ahli1':'A','ahli2':'A','ahli3':'C'},
    'CS-MIN-013': {'ahli1':'B','ahli2':'B','ahli3':'B'},
    'CS-BAL-014': {'ahli1':'B','ahli2':'B','ahli3':'C'},
    'CS-JAW-015': {'ahli1':'C','ahli2':'C','ahli3':'C'},
    'CS-LIN-016': {'ahli1':'C','ahli2':'C','ahli3':'A'},
    'CS-LIN-018': {'ahli1':'C','ahli2':'C','ahli3':'A'},
    'CS-MIN-005': {'ahli1':'B','ahli2':'C','ahli3':'A'},
    'CS-MIN-015': {'ahli1':'C','ahli2':'B','ahli3':'A'},
    'CS-NAS-041': {'ahli1':'A','ahli2':'C','ahli3':'C'},
}

ahli4 = {
    'CS-MIN-011':'B','CS-MIN-004':'C','CS-JAW-006':'A','CS-LIN-052':'C',
    'CS-NAS-066':'A','CS-BAL-002':'C','CS-NAS-010':'A','CS-LIN-017':'A',
    'CS-MIN-013':'D','CS-BAL-014':'C','CS-JAW-015':'C','CS-LIN-016':'A',
    'CS-MIN-005':'A','CS-MIN-015':'A','CS-NAS-041':'C','CS-LIN-018':'C',
}

cats = ['A','B','C','D']

def kappa(r1, r2):
    n = len(r1)
    po = sum(1 for a, b in zip(r1, r2) if a == b) / n
    f1, f2 = Counter(r1), Counter(r2)
    pe = sum((f1.get(c, 0)/n) * (f2.get(c, 0)/n) for c in cats)
    if pe >= 1.0:
        return 1.0
    return (po - pe) / (1 - pe)

ids = sorted(ahli4.keys())
a1 = [orig[c]['ahli1'] for c in ids]
a2 = [orig[c]['ahli2'] for c in ids]
a3 = [orig[c]['ahli3'] for c in ids]
a4 = [ahli4[c] for c in ids]

print('=== AHLI-4 (Dr. Eko Susilo, M.Hum) QUALITY ANALYSIS ===')
print(f'Overlapping cases: {len(ids)}')
print()

for nm, r in [('Ahli-1 (Dr. Hendra)', a1), ('Ahli-2 (Dr. Indra)', a2), ('Ahli-3 (removed)', a3)]:
    ag = sum(1 for x, y in zip(r, a4) if x == y)
    k = kappa(r, a4)
    interp = 'slight' if k < 0.20 else 'fair' if k < 0.40 else 'moderate' if k < 0.60 else 'substantial'
    if k < 0:
        interp = 'WORSE than chance'
    print(f'  Ahli-4 vs {nm:25s}: {ag:2d}/16 ({ag/16*100:5.1f}%) | Kappa={k:+.3f} ({interp})')

ag12 = sum(1 for x, y in zip(a1, a2) if x == y)
k12 = kappa(a1, a2)
print(f'  Ahli-1 vs Ahli-2 (reference)     : {ag12:2d}/16 ({ag12/16*100:5.1f}%) | Kappa={k12:+.3f}')

print()
print('=== CASE-BY-CASE COMPARISON ===')
print(f'{"Case":15s}  A1  A2  A3  A4  A4=A1 A4=A2 A4=A3')
for c in ids:
    v1, v2, v3, v4 = orig[c]['ahli1'], orig[c]['ahli2'], orig[c]['ahli3'], ahli4[c]
    m1 = 'Y' if v4 == v1 else '.'
    m2 = 'Y' if v4 == v2 else '.'
    m3 = 'Y' if v4 == v3 else '.'
    print(f'{c:15s}   {v1}   {v2}   {v3}   {v4}    {m1}     {m2}     {m3}')

print()
print('=== CONSENSUS-BREAKING ANALYSIS ===')
breaks = []
for c in ids:
    if orig[c]['ahli1'] == orig[c]['ahli2'] and ahli4[c] != orig[c]['ahli1']:
        breaks.append((c, orig[c]['ahli1'], ahli4[c]))
print(f'Ahli-4 BREAKS Ahli-1+Ahli-2 consensus in {len(breaks)}/{len(ids)} cases:')
for c, cons, v4 in breaks:
    print(f'  {c}: consensus={cons} -> Ahli-4={v4}')

print()
print('=== LABEL DISTRIBUTION ===')
for nm, r in [('Ahli-1', a1), ('Ahli-2', a2), ('Ahli-3', a3), ('Ahli-4', a4)]:
    d = Counter(r)
    print(f'  {nm:8s}: A={d.get("A",0)} B={d.get("B",0)} C={d.get("C",0)} D={d.get("D",0)}')
