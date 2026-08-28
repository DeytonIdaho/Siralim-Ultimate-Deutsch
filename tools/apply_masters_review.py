#!/usr/bin/env python3
import csv
from pathlib import Path
P=Path('masters.csv')
def main():
 with P.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fs=r.fieldnames or[];lo={x.lower():x for x in fs};e=next(lo[x] for x in ('english','en','source','original') if x in lo);d=next(lo[x] for x in ('german','de','deutsch','translation') if x in lo);rows=list(r)
 n=0
 for row in rows:
  en=row[e];old=row[d];new=old
  if en=='Dice':new='Dice'
  if en=='Slippy':new='Slippy'
  if en.startswith('Hemomancers '):new=new.replace('Hämomanten','Blutmagier')
  if en.startswith('Nixes '):new=new.replace('Nixen','Nix')
  if en.startswith('Lucanians '):
   new=new.replace('Lucanianer','Lucanians').replace('lucanischen Legion','Lucanian-Legion').replace('Lucanian-Gefährten','Lucanian-Gefährten')
  if en.startswith('Mirelings '):new=new.replace('Mirelinge','Mirelings').replace('Mireling-Stamm','Mireling-Stamm')
  if new!=old:row[d]=new;n+=1
 with P.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 print(f'masters review package: {n} rows changed')
if __name__=='__main__':main()
