#!/usr/bin/env python3
import csv
from pathlib import Path
P=Path('spells.csv')

# Conservative final normalizations based on the completed spells review.
# Tokens/placeholders are deliberately untouched.
REPL=(
 ('jedes Mal, das ','jedes Mal, wenn '),
 ('für jedes Mal, das ','für jedes Mal, wenn '),
 ('eine zufällige Merkmal','ein zufälliges Merkmal'),
 ('einen zufälligen Debuffs','einen zufälligen Debuff'),
 ('mit einem Debuffs','mit einem Debuff'),
 ('Werte (außer {STAT_health})','Attribute (außer {STAT_health})'),
 ('Eigenschaften (außer {STAT_health})','Attribute (außer {STAT_health})'),
)

def main():
 with P.open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f);fs=r.fieldnames or[];lo={x.lower():x for x in fs}
  d=next(lo[x] for x in ('german','de','deutsch','translation') if x in lo)
  rows=list(r)
 n=0
 for row in rows:
  old=row[d];new=old
  for a,b in REPL:new=new.replace(a,b)
  if new!=old:row[d]=new;n+=1
 with P.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 print(f'spells review package: {n} rows changed')
if __name__=='__main__':main()
