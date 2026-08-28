#!/usr/bin/env python3
"""Apply confirmed cross-file consistency fixes. Exact English keys only where possible."""
import csv
from pathlib import Path
EXACT={
 'After the bearer {ACTION_attacks}, this relic {ACTION_attacks} the enemy as well.':'Nachdem der Träger {ACTION_attacks}, {ACTION_attacks} dieses Relikt den Feind ebenfalls.',
 'Enemies gain 50% less benefit from stat-boosting effects.':'Gegner erhalten 50% weniger Nutzen aus attributssteigernden Effekten.',
 'Master of Arbiters':'Meister der Schlichter','Master of Eggxotics':'Meister der Eggxotics','Master of Fiends':'Meister der Unholde',
 'Master of Gargantuans':'Meister der Gargantuans','Master of Gemlings':'Meister der Edelsteinjünglinge','Master of Hemomancers':'Meister der Blutmagier',
 'Master of Lucanians':'Meister der Lucanians','Master of Luckmantrias':'Meister der Luckmantrias','Master of Nixes':'Meister der Nix',
 'Master of Ophans':'Meister der Ophans','Master of Pit Worms':'Meister der Grubenwürmer','Master of Wights':'Meister der Gruftschrate',
 'Your creatures take 10% less damage while they\'re {ACTION_provoking}.':'Deine Kreaturen erleiden 10% weniger Schaden, während sie {ACTION_provoking} sind.',
 '[bg_squash] Vomiting Squash Is More Rewarding':'[bg_squash] Kotzender Kürbis ist lohnender',
 'You gain 5% more Notoriety from the Gambling Dwarves.':'Du erhältst 5% mehr Berüchtigung von den Glücksspiel-Zwergen.',
 'Your creatures have a 3% chance to ignore incoming debuffs.':'Deine Kreaturen haben eine 3% Chance, eingehende Debuffs zu ignorieren.',
 # Exact duplicates: select one canonical form.
 'Aeolian':'Aeolisch','Arm of Loid':'Arm des Loid','Celestial Orb':'Himmlische Kugel','Death Orb':'Todeskugel',
 'Head of Lost Construct':'Kopf des verlorenen Konstrukts','Imp Impington':'Imp Impington','Nether Orb':'Nether-Kugel',
 'Overkill':'Overkill','Perdition':'Verdammnis','The Swamplands':'Die Sümpfe','Unsullied Meadows':'Unbefleckte Auen',
 'Tigerseye Catbuncle':'Tigeraugen-Katbunkel','Undead Army':'Armee der Untoten','none':'keine',
 'Pay your respects to fallen {CASTLENAME} knights and magi in this Realm.':'Erweise den gefallenen Rittern und Magiern von {CASTLENAME} in diesem Reich deinen Respekt.',
}
GERMAN_REPL=(('Der nachwuchs ','Der Nachwuchs '),('der nachwuchs ','der Nachwuchs '))
def cols(fs):
 lo={x.lower():x for x in fs};return next((lo[x] for x in ('english','en','source','original','text_en','description_en') if x in lo),None),next((lo[x] for x in ('german','de','deutsch','translation','text_de','description_de') if x in lo),None)
def main():
 total=0
 for p in sorted(Path('.').glob('*.csv')):
  with p.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fs=r.fieldnames or [];e,d=cols(fs);rows=list(r)
  if not e or not d:continue
  n=0
  for row in rows:
   old=row.get(d,'') or '';new=EXACT.get(row.get(e,'') or '',old)
   for a,b in GERMAN_REPL:new=new.replace(a,b)
   if new!=old:row[d]=new;n+=1
  if n:
   with p.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
   print(f'{p}: {n} consistency fixes');total+=n
 print(f'total consistency fixes: {total}')
if __name__=='__main__':main()
