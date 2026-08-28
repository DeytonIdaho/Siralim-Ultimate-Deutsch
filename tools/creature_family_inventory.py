#!/usr/bin/env python3
import csv
from collections import defaultdict
from pathlib import Path

SRC=Path('creatures.csv')
OUT=Path('consistency_review/creature_families.csv')

with SRC.open(encoding='utf-8-sig',newline='') as f:
    r=csv.DictReader(f); rows=list(r)

# Base-race rows are the initial L_* entries before individual L_CRIT_* creatures.
base={}
for row in rows:
    tag=row.get('Tag','')
    if tag.startswith('L_CRIT_'): continue
    en=(row.get('English') or '').strip()
    de=(row.get('German') or '').strip()
    if en: base[en]=(tag,de)

families=defaultdict(list)
# Longest names first so multiword families (Pit Worm etc.) win.
base_names=sorted(base,key=lambda x:(len(x.split()),len(x)),reverse=True)
for n,row in enumerate(rows,2):
    tag=row.get('Tag',''); en=(row.get('English') or '').strip(); de=(row.get('German') or '').strip()
    if not tag.startswith('L_CRIT_'): continue
    matches=[]
    for fam in base_names:
        if en==fam or en.endswith(' '+fam) or en.startswith(fam+' '): matches.append(fam)
    if matches:
        fam=matches[0]; families[fam].append((n,tag,en,de))

OUT.parent.mkdir(exist_ok=True)
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.writer(f);w.writerow(['family_english','family_german','row','tag','english','german'])
    for fam in sorted(families):
        tag,debase=base[fam]
        for n,ctag,en,de in families[fam]:w.writerow([fam,debase,n,ctag,en,de])
print('families',len(families),'creatures',sum(map(len,families.values())))
