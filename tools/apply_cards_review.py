#!/usr/bin/env python3
import csv,re
from pathlib import Path
P=Path('cards.csv')
def main():
 with P.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fs=r.fieldnames or[];lo={x.lower():x for x in fs};e=next(lo[x] for x in ('english','en','source','original') if x in lo);d=next(lo[x] for x in ('german','de','deutsch','translation') if x in lo);rows=list(r)
 n=0
 for row in rows:
  en=row[e];old=row[d];new=old
  if 'Your creatures' in en:
   new=new.replace('Eure Kreaturen','Deine Kreaturen').replace('eure Kreaturen','deine Kreaturen')
  if 'stat-boosting effects' in en:
   new=re.sub(r'(?:Attribute-verstärkende|statusverbessernde|statussteigernde|wertsteigernde) Effekte','attributssteigernde Effekte',new,flags=re.I)
  if 'stat-reducing effects' in en:
   new=re.sub(r'(?:wertreduzierende|statussenkende|attributsenkende) Effekte','attributssenkende Effekte',new,flags=re.I)
  if "Artifacts' Stat Slots" in en:new=new.replace('Statusplätzen','Attributsplätze').replace('Statusplätze','Attributsplätze')
  if 'Ultimate Spell Gems' in en or '{SPELL_ultimate} Gems' in en:new=new.replace('Edelsteine','Zaubersteine')
  if 'Sealed Spell Gem' in en:
   new=new.replace('Versiegelten Zauberstein','versiegelten Zauberstein').replace('Versiegelte Zauberstein','versiegelten Zauberstein').replace('Versiegeltes Zauberstein','versiegelten Zauberstein')
   new=new.replace('jedes versiegelten','jeden versiegelten').replace('jedes Versiegelte','jeden versiegelten')
  new=re.sub(r'\b([0-9]+) Mal\b',r'\1-mal',new)
  new=new.replace('wird einer seiner Zaubersteine Versiegelt','wird einer seiner Zaubersteine versiegelt')
  new=new.replace('Schaden an Feinde ','Schaden an Feinden ').replace('Schaden an benachbarte Kreaturen','Schaden an benachbarten Kreaturen')
  new=new.replace('Maximales {STAT_health}','maximales {STAT_health}')
  if new!=old:row[d]=new;n+=1
 with P.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 print(f'cards review package: {n} rows changed')
if __name__=='__main__':main()
