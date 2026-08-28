#!/usr/bin/env python3
import csv
from pathlib import Path

def apply(path, fixes):
 p=Path(path)
 with p.open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f);fs=r.fieldnames or[];lo={x.lower():x for x in fs};e=next(lo[x] for x in ('english','en','source','original') if x in lo);d=next(lo[x] for x in ('german','de','deutsch','translation') if x in lo);rows=list(r)
 n=0
 for row in rows:
  en=row[e];old=row[d];new=fixes.get(en,old)
  if new!=old:row[d]=new;n+=1
 with p.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 print(f'{path}: {n} rows changed')

def main():
 misc={'Imp Impington':'Imp Impington','Imp Impington Reborn':'Imp Impington Reborn'}
 skins={
 'Imp Impington':'Imp Impington',
 'Frostbite Caverns':'Frostbiss-Höhlen','Unsullied Meadows':'Unbefleckte Wiesen','Faraway Enclave':'Ferne Enklave','Eternity\'s End':'Ende der Ewigkeit','The Swamplands':'Sumpflande',
 'Halloween Aeolian':'Halloween Aeolian','Halloween Friden':'Halloween Friden','Halloween Perdition':'Halloween Perdition','Halloween Vertraag':'Halloween Vertraag',
 'Springtime Aeolian':'Frühlings-Aeolian','Springtime Lister':'Frühlings-Lister','Christmas Perdition':'Weihnachts-Perdition',
 'Reaver':'Reaver','Follower of Perdition':'Anhänger von Perdition','Nether Orb':'Nether-Orb',
 'Complete Form':'Vollständige Form','Initiate':'Eingeweihter','One Braincell':'Eine Gehirnzelle'
 }
 apply('misc.csv',misc);apply('skins.csv',skins)
if __name__=='__main__':main()
