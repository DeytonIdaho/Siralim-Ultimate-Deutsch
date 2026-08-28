#!/usr/bin/env python3
import csv,re
from pathlib import Path
P=Path('codex.csv')
EX={'Stat Slots':'Attributsplätze','Ethereal Gems':'Ätherische Zaubersteine','Casting':'Zauberwirken','Provoking':'Provozieren','Socketing':'Einsetzen','Stats':'Attribute','Chance to leave at start of master\'s turn: {1}%':'Chance, zu Beginn des Zuges des Meisters zu verschwinden: {1}%','none':'keine'}
ITEM='Ausrüstungssets ermöglichen es dir, Gruppen von Artefakten und Zaubersteinen einfach zu speichern und zu laden. Du kannst diese Ausrüstungssets verwenden, um deine Kreaturen schnell mit verschiedenen Artefakten und Zaubersteinen auszurüsten.\n\nUm ein Ausrüstungsset zu erstellen, öffne das Menü und wähle „Kreaturen“. Wähle anschließend eine Kreatur und dann „Ausrüstungssets verwalten“. Es erscheint ein neues Menü, in dem du die derzeit ausgerüsteten Gegenstände dieser Kreatur über „Zuweisen“ einem Ausrüstungsset zuordnen kannst. Später kannst du mit der Option „Ausrüsten“ schnell die in diesem Ausrüstungsset enthaltenen Gegenstände anlegen.'
def main():
 with P.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fs=r.fieldnames or[];lo={x.lower():x for x in fs};e=next(lo[x] for x in ('english','en','source','original') if x in lo);d=next(lo[x] for x in ('german','de','deutsch','translation') if x in lo);rows=list(r)
 n=0
 for row in rows:
  en=row[e];old=row[d];new=EX.get(en,old)
  if en.startswith('Item Sets allow you to easily save'):new=ITEM
  new=new.replace('Statusplätze','Attributsplätze').replace('Statusmaterialien','Attributsmaterialien').replace('Stat-Materialien','Attributsmaterialien').replace('Wert-Sockel','Attributsplätze').replace('Statusbonus','Attributsbonus').replace('Statusboost','Attributsbonus')
  new=new.replace('Ätherische Edelsteine','Ätherische Zaubersteine')
  new=new.replace('eine Merkmal','ein Merkmal').replace('eine zusätzliche Merkmal','ein zusätzliches Merkmal')
  new=re.sub(r'\beinen Artefakt\b','ein Artefakt',new)
  if "Spell Gem's class is changed" in en:new='Die Klasse des Zaubersteins wird zu '+en.split(' to ',1)[1].rstrip('.')+'.'
  if en=='Creature: none':new='Kreatur: keine'
  if new!=old:row[d]=new;n+=1
 with P.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 print(f'codex review package: {n} rows changed')
if __name__=='__main__':main()
