#!/usr/bin/env python3
import csv,re
from pathlib import Path
P=Path('creatures.csv'); O=Path('consistency_review/creature_special_cases.csv')
terms=re.compile(r'(strix|drak|drach|todesfee|wicht|wiedergänger|aussauger|blutegel|dschinn|djinn|ifrit|efreet|unterweltler|unterirdisch|mimik|mimic|vertraut|greifer|klammer|banshee)',re.I)
with P.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);rows=list(r)
out=[]
for n,row in enumerate(rows,2):
 en=(row.get('English') or '').strip();de=(row.get('German') or '').strip();tag=row.get('Tag','')
 if terms.search(en) or terms.search(de):out.append((n,tag,en,de))
O.parent.mkdir(exist_ok=True)
with O.open('w',encoding='utf-8',newline='') as f:w=csv.writer(f);w.writerow(['row','tag','english','german']);w.writerows(out)
print('special cases',len(out))
