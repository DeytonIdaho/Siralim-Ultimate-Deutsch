#!/usr/bin/env python3
import csv
from pathlib import Path

# Exact, reviewed fixes only. All other fields/rows remain untouched.
TAG_FIXES = {
    'L_ATTACKS': 'Greift an',
    'L_DEFENDING': 'Verteidigend',
    'L_CAST': 'Wirken',
    'L_CASTING': 'Wirkend',
    'L_CASTS': 'Wirkt',
    'L_CHARGE': 'Ladung',
}
EXACT_ENGLISH_FIXES = {
    'ui.csv': {'Cast': 'Wirken'},
    'traits.csv': {'Charge': 'Ladung'},
}

def process(path: Path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        rows = list(reader)
    lower = {x.lower(): x for x in fields}
    tag_col = lower.get('tag')
    en_col = lower.get('english')
    de_col = lower.get('german')
    if not de_col:
        return 0, []
    changes = []
    for i, row in enumerate(rows, 2):
        new = None
        reason = None
        if path.name == 'vocabulary.csv' and tag_col and row.get(tag_col) in TAG_FIXES:
            new = TAG_FIXES[row[tag_col]]
            reason = row[tag_col]
        elif path.name in EXACT_ENGLISH_FIXES and en_col and row.get(en_col, '').strip() in EXACT_ENGLISH_FIXES[path.name]:
            key = row[en_col].strip()
            new = EXACT_ENGLISH_FIXES[path.name][key]
            reason = f'English={key}'
        if new is not None and row.get(de_col) != new:
            old = row.get(de_col, '')
            row[de_col] = new
            changes.append((path.name, i, reason, old, new))
    if changes:
        with path.open('w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
            w.writeheader(); w.writerows(rows)
    return len(changes), changes

def main():
    all_changes = []
    for name in ('vocabulary.csv','ui.csv','traits.csv'):
        n, changes = process(Path(name)); all_changes.extend(changes)
        print(f'{name}: {n} changes')
    for c in all_changes: print('FIX', *c, sep=' | ')
    # Expected: 6 vocabulary tags, 2 Cast rows in ui.csv, 1 Charge row in traits.csv.
    if len(all_changes) != 9:
        raise SystemExit(f'ABORT: expected exactly 9 changes, got {len(all_changes)}')

if __name__ == '__main__': main()
