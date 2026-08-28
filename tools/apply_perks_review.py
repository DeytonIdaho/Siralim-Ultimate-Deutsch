#!/usr/bin/env python3
import csv
from pathlib import Path
P=Path('perks.csv')

# Conservative terminology/grammar normalization from the complete 1-1323 review.
REPL=(
 ('jedes Mal, das ','jedes Mal, wenn '),
 ('für jedes Mal, das ','für jedes Mal, wenn '),
 ('eine zufällige Merkmal','ein zufälliges Merkmal'),
 ('zufällige Merkmale','zufällige Merkmale'),
 ('Stat-Slots','Attribut-Slots'),
 ('Statusgrenzen','Attributgrenzen'),
 ('Werte (außer {STAT_health})','Attribute (außer {STAT_health})'),
 ('Eigenschaft für jede Stufe','Attribut für jede Stufe'),
 ('Effektstärke aller {CONDNAME_DEBUFF_BURNED}-Debuff ','Effektstärke aller {CONDNAME_DEBUFF_BURNED}-Debuffs '),
 ('{CONDNAME_DEBUFF_POISON}-Debuff der Feinde','{CONDNAME_DEBUFF_POISON}-Debuffs der Feinde'),
 ('Vorteilspunkte','Talentpunkte'),
)

# Exact corrections where the review identified a clear mistranslation.
EX={
 "Your creatures' extra casts no longer consume additional {STAT_charges}.":
 'Zusätzliche Zauberwirkungen deiner Kreaturen verbrauchen keine zusätzlichen {STAT_charges} mehr.',
 "Increases your creatures' maximum stat limits before they are subjected to diminishing returns by <10>%.":
 'Erhöht die maximalen Attributgrenzen deiner Kreaturen, bevor abnehmende Erträge einsetzen, um <10>%.',
 "At the start of your Herbling's turn, it gains <1>% of each stat for each Tier it has.":
 'Zu Beginn des Zuges deines Herblings erhält es <1>% jedes Attributs für jede Stufe, die es hat.',
}

def main():
 with P.open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f);fs=r.fieldnames or[];lo={x.lower():x for x in fs}
  e=next(lo[x] for x in ('english','en','source','original') if x in lo)
  d=next(lo[x] for x in ('german','de','deutsch','translation') if x in lo)
  rows=list(r)
 n=0
 for row in rows:
  old=row[d];new=EX.get(row[e],old)
  for a,b in REPL:new=new.replace(a,b)
  if new!=old:row[d]=new;n+=1
 with P.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 print(f'perks review package: {n} rows changed')
if __name__=='__main__':main()
