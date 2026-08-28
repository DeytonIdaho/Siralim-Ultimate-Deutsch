#!/usr/bin/env python3
"""Apply confirmed cross-file consistency fixes."""
import csv,re
from pathlib import Path
EXACT={
 'After the bearer {ACTION_attacks}, this relic {ACTION_attacks} the enemy as well.':'Nachdem der Träger {ACTION_attacks}, {ACTION_attacks} dieses Relikt den Feind ebenfalls.',
 'Enemies gain 50% less benefit from stat-boosting effects.':'Gegner erhalten 50% weniger Nutzen aus attributssteigernden Effekten.',
 'Master of Arbiters':'Meister der Schlichter','Master of Eggxotics':'Meister der Eggxotics','Master of Fiends':'Meister der Unholde','Master of Gargantuans':'Meister der Gargantuans','Master of Gemlings':'Meister der Edelsteinjünglinge','Master of Hemomancers':'Meister der Blutmagier','Master of Lucanians':'Meister der Lucanians','Master of Luckmantrias':'Meister der Luckmantrias','Master of Nixes':'Meister der Nix','Master of Ophans':'Meister der Ophans','Master of Pit Worms':'Meister der Grubenwürmer','Master of Wights':'Meister der Gruftschrate',
 'Your creatures take 10% less damage while they\'re {ACTION_provoking}.':'Deine Kreaturen erleiden 10% weniger Schaden, während sie {ACTION_provoking} sind.',
 '[bg_squash] Vomiting Squash Is More Rewarding':'[bg_squash] Kotzender Kürbis ist lohnender','You gain 5% more Notoriety from the Gambling Dwarves.':'Du erhältst 5% mehr Berüchtigung von den Glücksspiel-Zwergen.','Your creatures have a 3% chance to ignore incoming debuffs.':'Deine Kreaturen haben eine 3% Chance, eingehende Debuffs zu ignorieren.',
 'Aeolian':'Aeolisch','Arm of Loid':'Arm des Loid','Celestial Orb':'Himmlische Kugel','Death Orb':'Todeskugel','Head of Lost Construct':'Kopf des verlorenen Konstrukts','Imp Impington':'Imp Impington','Nether Orb':'Nether-Kugel','Overkill':'Overkill','Perdition':'Verdammnis','The Swamplands':'Die Sümpfe','Unsullied Meadows':'Unbefleckte Auen','Tigerseye Catbuncle':'Tigeraugen-Katbunkel','Undead Army':'Armee der Untoten','none':'keine','Pay your respects to fallen {CASTLENAME} knights and magi in this Realm.':'Erweise den gefallenen Rittern und Magiern von {CASTLENAME} in diesem Reich deinen Respekt.',
 # Minion terminology
 **{f'Master of Minions {r}':f'Meister der Diener {r}' for r in ('I','II','III','IV','V','VI','VII','VIII','IX','X')},
 'Minions':'Diener','Minion Master':'Dienermeister','Minion Master Staff':'Stab des Dienermeisters',
 "[realmprop_f_nominions] Can't Have Minions":'[realmprop_f_nominions] Keine Diener möglich',
 'has > {1} minions':'hat > {1} Diener','has < {1} minions':'hat < {1} Diener',
 # Debuff verb achievements
 **{f'Debuff creatures {n} times.':f'Debuffe Kreaturen {n.replace(",", ".")} Mal.' for n in ('100','250','500','1,000','2,500','5,000','10,000','25,000','50,000','100,000')},
 '{1}% Debuff Potency':'{1}% Debuff-Wirksamkeit',
}
GERMAN_REPL=(('Der nachwuchs ','Der Nachwuchs '),('der nachwuchs ','der Nachwuchs '),('Dienernn','Dienern'))
# For rows whose English explicitly uses gameplay terms, normalize German terminology inside that row only.
DEBUFF_NOUN=re.compile(r'\bdebuffs?\b',re.I);BUFF_NOUN=re.compile(r'\bbuffs?\b',re.I);MINION_NOUN=re.compile(r'\bminions?\b',re.I)
def cols(fs):
 lo={x.lower():x for x in fs};return next((lo[x] for x in ('english','en','source','original','text_en','description_en') if x in lo),None),next((lo[x] for x in ('german','de','deutsch','translation','text_de','description_de') if x in lo),None)
def normalize_terms(en,de):
 # These replacements are deliberately scoped to rows where the corresponding English gameplay term exists.
 if DEBUFF_NOUN.search(en):
  de=re.sub(r'\bSchwächungen\b','Debuffs',de);de=re.sub(r'\bSchwächung\b','Debuff',de);de=re.sub(r'\bSchwächungszustände\b','Debuffs',de);de=re.sub(r'\bSchwächungszustand\b','Debuff',de);de=re.sub(r'\bSchwächungszaubern\b','Debuffs',de);de=re.sub(r'\bSchwächungszauber\b','Debuff',de);de=re.sub(r'\bMalusse\b','Debuffs',de);de=re.sub(r'\bMalus\b','Debuff',de)
  # Verb forms where English itself says debuff/debuffs as a verb.
  if re.search(r'\bdebuff\b',en,re.I): de=re.sub(r'\bschwächen\b','debuffen',de,flags=re.I);de=re.sub(r'\bschwäche\b','Debuffe',de,flags=re.I)
 if BUFF_NOUN.search(en):
  de=re.sub(r'\bStärkungen\b','Buffs',de);de=re.sub(r'\bStärkung\b','Buff',de)
  if re.search(r'\bbuff\b',en,re.I): de=re.sub(r'\bverstärken\b','buffen',de,flags=re.I)
 if MINION_NOUN.search(en):
  de=re.sub(r'\bSchergen\b','Diener',de);de=re.sub(r'\bLakaien\b','Diener',de)
 return de
def main():
 total=0
 for p in sorted(Path('.').glob('*.csv')):
  with p.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fs=r.fieldnames or [];e,d=cols(fs);rows=list(r)
  if not e or not d:continue
  n=0
  for row in rows:
   en=row.get(e,'') or '';old=row.get(d,'') or '';new=EXACT.get(en,old);new=normalize_terms(en,new)
   for a,b in GERMAN_REPL:new=new.replace(a,b)
   if new!=old:row[d]=new;n+=1
  if n:
   with p.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
   print(f'{p}: {n} consistency fixes');total+=n
 print(f'total consistency fixes: {total}')
if __name__=='__main__':main()
