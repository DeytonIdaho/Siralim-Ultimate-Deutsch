#!/usr/bin/env python3
import csv,re
from pathlib import Path
P=Path('bosses.csv')
def main():
 with P.open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f);fs=r.fieldnames or[];lo={x.lower():x for x in fs};e=next(lo[x] for x in ('english','en','source','original') if x in lo);d=next(lo[x] for x in ('german','de','deutsch','translation') if x in lo);rows=list(r)
 n=0
 for row in rows:
  en=row[e];old=row[d];new=old
  if 'Rift Dancer' in en:new=new.replace('Rissspringer','Dimensionsläufer').replace('Rift-Tänzer','Dimensionsläufer').replace('Risstänzer','Dimensionsläufer')
  if 'Pit Worm' in en:new=new.replace('Grubendrache','Grubenwurm')
  if 'Forsaken' in en:new=new.replace('Verstoßene','Verlassene').replace('Verstoßener','Verlassener')
  if 'Fiend' in en:new=new.replace('Ungeheuer','Unhold')
  if 'Mindwurm' in en:new=new.replace('Gedankenwurm','Mindwurm')
  if 'The Ancestor' in en:new=new.replace('Ahnherrn','Ahn').replace('Ahnherr','Ahn').replace('Ahnen','Ahn').replace('Ahne','Ahn')
  if 'Spellmane' in en:new=new.replace('dem Zaubermähne','der Zaubermähne')
  # Consistent proper-name rendering.
  new=new.replace('Nether-Kugel','Nether-Orb').replace('Netherkugel','Nether-Orb')
  # Clear narration slips, not deliberate formal dialogue.
  if en.startswith('('):
   new=new.replace('als ihr euch nähert','als du dich näherst').replace('Als ihr euch nähert','Als du dich näherst')
  if new!=old:row[d]=new;n+=1
 with P.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 print(f'boss review package: {n} rows changed')
if __name__=='__main__':main()
