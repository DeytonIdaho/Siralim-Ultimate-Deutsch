#!/usr/bin/env python3
import csv
from pathlib import Path
P=Path('battle.csv')
EX={
'More Intense\nBurn!':'Intensivere\nVerbrennung!','More Intense\nPoison!':'Intensiveres\nGift!','More Intense\nBomb!':'Intensivere\nBombe!',
'Ethereal Gems\nSealed':'Ätherische Zaubersteine\nVersiegelt','Ethereal Gems\nReplaced':'Ätherische Zaubersteine\nErsetzt',
'Defense/Speed Set To\nMinimum':'Verteidigung/Geschwindigkeit auf\nMinimum gesetzt','Stats Set To\nMinimum':'Attribute auf\nMinimum gesetzt','Stats Set To\n{1}':'Attribute auf\n{1} gesetzt',
'Spells Are\nFree':'Zauber sind\nkostenlos','Too Many\nGems':'Zu viele\nZaubersteine','Gained Trait:\n{1}':'Merkmal erhalten:\n{1}',
'Your {1} cannot manually perform actions because it has the "Another Man\'s Trash" trait.':'Dein {1} kann keine Aktionen manuell ausführen, da es das Merkmal „Eines anderen Mannes Müll“ besitzt.',
'Your {1} cannot cast spells manually because its trait prevents it from doing so.':'Dein {1} kann keine Zauber manuell wirken, da sein Merkmal es daran hindert.',
'Your {1} cannot cast spells (other than Arrow spells) manually because its trait prevents it from doing so.':'Dein {1} kann keine Zauber (außer Pfeilzauber) manuell wirken, da sein Merkmal es daran hindert.',
'{1} has already been damaged too many times this turn.':'{1} hat in diesem Zug bereits zu oft Schaden erlitten.',
}
def main():
 with P.open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f);fs=r.fieldnames or[];lo={x.lower():x for x in fs};e=next(lo[x] for x in ('english','en','source','original') if x in lo);d=next(lo[x] for x in ('german','de','deutsch','translation') if x in lo);rows=list(r)
 n=0
 for row in rows:
  en=row[e];old=row[d];new=EX.get(en,old)
  new=new.replace('Stats Auf','Attribute auf').replace('Stats auf','Attribute auf').replace('Zauber Sind','Zauber sind').replace('Zu Viele','Zu viele')
  if new!=old:row[d]=new;n+=1
 with P.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 print(f'battle review package: {n} rows changed')
if __name__=='__main__':main()
