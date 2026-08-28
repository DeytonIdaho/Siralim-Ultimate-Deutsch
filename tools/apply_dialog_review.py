#!/usr/bin/env python3
import csv
from pathlib import Path
P=Path('dialog.csv')
def main():
 with P.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fs=r.fieldnames or[];lo={x.lower():x for x in fs};e=next(lo[x] for x in ('english','en','source','original') if x in lo);d=next(lo[x] for x in ('german','de','deutsch','translation') if x in lo);rows=list(r)
 n=0
 for row in rows:
  en=row[e];old=row[d];new=old
  if en.startswith('Spicy:'):new=new.replace('Scharf:','Spicy:').replace('Bruder Scharf','Bruder Spicy')
  if 'Rosebud the Disgruntled Arena Master:' in en:
   for x in ('Rosebud der mürrische Arenameister:','Rosebud der verdrießliche Arenameister:','Rosebud der missmutige Arenamaster:','Rosebud der mürrische Arenamaster:'):new=new.replace(x,'Rosebud der missmutige Arenameister:')
  if en.startswith('Abomination Plush:'):
   for x in ('Abominations-Plüschtier:','Abomination-Plüschtier:','Abscheulichkeits-Plüsch:'):new=new.replace(x,'Abscheulichkeits-Plüschtier:')
  if en=='Please finalize your bets now.':new='Bitte schließt jetzt eure Wetten ab.'
  if en=="Your {1}'s personality is now {2}.":new='Die Persönlichkeit von {1} ist jetzt {2}.'
  if en.startswith('This creature has already used 15 scrolls.'):new='Diese Kreatur hat bereits 15 Schriftrollen verwendet. Sie kann keine weiteren benutzen.'
  if en=='The totem is no longer corrupted!':new='Das Totem ist nicht länger verdorben!'
  if en.startswith('Voice of Friden:') and 'Brilliant!' in en:new=new.replace('Brilliant!','Brillant!')
  if 'Rune of Prophecies' in en:new=new.replace('Runenzeichen der Prophezeiungen','Rune der Prophezeiungen')
  if en.startswith('Everett:\nHail,'):new='Everett:\nSei gegrüßt, {PLAYERNAME}. Ich hoffe, es geht dir heute gut!'
  if en.startswith('Lord Zantai:'):
   new=new.replace('Mach dich bereit!','Macht Euch bereit!').replace('euch vernichten','Euch vernichten')
  if new!=old:row[d]=new;n+=1
 with P.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 print(f'dialog review package: {n} rows changed')
if __name__=='__main__':main()
