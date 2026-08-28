#!/usr/bin/env python3
import csv
from pathlib import Path
P=Path('lore.csv')
def main():
 with P.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fs=r.fieldnames or[];lo={x.lower():x for x in fs};e=next(lo[x] for x in ('english','en','source','original') if x in lo);d=next(lo[x] for x in ('german','de','deutsch','translation') if x in lo);rows=list(r)
 n=0
 for row in rows:
  en=row[e];old=row[d];new=old
  # Established world/item terminology.
  new=new.replace('Ewigkeits Ende','Ende der Ewigkeit')
  new=new.replace('Nether-Kugeln','Nether-Orbs').replace('Netherkugeln','Nether-Orbs').replace('Nether-Kugel','Nether-Orb').replace('Netherkugel','Nether-Orb')
  # Established creature terminology, only where old machine variants are unambiguous.
  new=new.replace('Leerefürsten','Leerenfürsten').replace('Leerefürst','Leerenfürst')
  new=new.replace('Riss-Tänzer','Dimensionsläufer').replace('Rifttänzer','Dimensionsläufer')
  new=new.replace('Hämomanten','Blutmagier').replace('Hämomant','Blutmagier')
  # Arbiter is Schlichter throughout this project.
  new=new.replace('Schiedsrichter','Schlichter')
  # Clear grammar error.
  if en.startswith('The Torture Chamber is an underground complex'):new=new.replace('Der Folterkammer ist','Die Folterkammer ist')
  # Clearly truncated Tenbran/Perdition lore entry: reconstruct from the full English source.
  if en.startswith('Perdition created this creature at a time when he sorely missed his beloved sister.'):
   new='Perdition erschuf diese Kreatur zu einer Zeit, als er seine geliebte Schwester schmerzlich vermisste. Ohne es zu beabsichtigen, spiegelt Tenbran in seinem Gesicht den Gemütszustand wider, in dem sich der Gott des Limbus gerade befindet. Die beiden wurden sehr gute Freunde und diskutierten im Laufe der Jahre über unzählige Themen. Als seine Schwester Sevalah eintraf, betrachtete sie die Kreatur mit hochgezogener Augenbraue. „Ich sehe, du hast mich vermisst, kleiner Bruder“, sagte sie. Perdition lächelte und umarmte sie fest, während Tenbran die Szene mit einem Gesicht voller Trauer beobachtete, die nicht seine eigene war.'
  if new!=old:row[d]=new;n+=1
 with P.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 print(f'lore gentle review: {n} rows changed')
if __name__=='__main__':main()
