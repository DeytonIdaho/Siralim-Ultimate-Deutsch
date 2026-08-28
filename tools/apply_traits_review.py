#!/usr/bin/env python3
import csv
from pathlib import Path

P=Path('traits.csv')

# High-confidence semantic/mechanical fixes identified during full human review.
EX={
 'Enemies with {CONDNAME_DEBUFF_FEAR} take 15% more damage for each {CLASS_Death} creature fighting on your side. This trait does not stack.':
 'Feinde mit {CONDNAME_DEBUFF_FEAR} erleiden 15% mehr Schaden für jede {CLASS_Death}-Kreatur, die auf deiner Seite kämpft. Dieses Merkmal ist nicht kumulativ.',
 'After your creatures gain a stat (other than {STAT_health}), they grant 25% of this stat to your other creatures as well. Your creatures gain 50% less stats. This trait does not stack.':
 'Nachdem deine Kreaturen ein Attribut erhalten (außer {STAT_health}), gewähren sie deinen anderen Kreaturen ebenfalls 25% dieses Attributs. Deine Kreaturen erhalten 50% weniger Attribute. Dieses Merkmal ist nicht kumulativ.',
 'This creature has 15% more stats (other than {STAT_health}) for each other creature with this trait fighting on your side.':
 'Diese Kreatur hat 15% mehr Attribute (außer {STAT_health}) für jede andere Kreatur mit diesem Merkmal, die an deiner Seite kämpft.',
}

# Safe German-only normalizations found repeatedly during the complete traits review.
REPL=(
 ('eine zufällige Merkmal','ein zufälliges Merkmal'),
 ('eine Merkmal','ein Merkmal'),
 ('jede Merkmal','jedes Merkmal'),
 ('dieselbe Merkmal','dasselbe Merkmal'),
 ('die Merkmal','das Merkmal'),
 ('mit dieses Merkmal','mit diesem Merkmal'),
 ('mit einem Debuffs','mit einem Debuff'),
 ('einen zufälligen Debuffs','einen zufälligen Debuff'),
 ('ihre angeborenes Merkmal','ihr angeborenes Merkmal'),
 ('die angeborenes Merkmal','das angeborene Merkmal'),
 ('in ihren angeborenen Merkmale','in ihren angeborenen Merkmalen'),
 ('jedes andere Kreatur','jede andere Kreatur'),
 ('können nicht Ausgewichen werden','ihnen kann nicht ausgewichen werden'),
 ('Armee von Diener','Armee von Dienern'),
)

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
 print(f'traits review package: {n} rows changed')
if __name__=='__main__':main()
