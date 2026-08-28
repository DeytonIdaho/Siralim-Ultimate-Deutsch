#!/usr/bin/env python3
"""Apply confirmed cross-file consistency fixes."""
import csv,re
from pathlib import Path
ITEMSETS='Item Sets allow you to easily save and load groups of Artifacts and Spell Gems. You can use these Item Sets to quickly equip your creatures with different Artifacts and Spell Gems.\n\nTo create an Item Set, open the menu and select "Creatures", then select a creature and choose "Manage Item Sets". A new menu will appear that allows you to "Assign" that creature\'s currently equipped items to an Item Set. Later, you can use the "Equip" option to quickly equip the items contained in that Item Set.'
ITEMSETS_DE='Ausrüstungssets ermöglichen es dir, Gruppen von Artefakten und Zaubersteinen einfach zu speichern und zu laden. Du kannst diese Ausrüstungssets verwenden, um deine Kreaturen schnell mit verschiedenen Artefakten und Zaubersteinen auszurüsten.\n\nUm ein Ausrüstungsset zu erstellen, öffne das Menü und wähle „Kreaturen“. Wähle anschließend eine Kreatur und dann „Ausrüstungssets verwalten“. Es erscheint ein neues Menü, in dem du die derzeit ausgerüsteten Gegenstände dieser Kreatur über „Zuweisen“ einem Ausrüstungsset zuordnen kannst. Später kannst du mit der Option „Ausrüsten“ schnell die in diesem Ausrüstungsset enthaltenen Gegenstände anlegen.'
EXACT={
 ITEMSETS:ITEMSETS_DE,
 'Daybreaker':'Tagesbrecher',
 '{CONDNAME_DEBUFF_CONFUSED} creatures have a 50% chance to {ACTION_attack} or {ACTION_cast} harmful spells on their allies.':'{CONDNAME_DEBUFF_CONFUSED} Kreaturen haben eine 50% Chance, ihre Verbündeten zu {ACTION_attack} oder schädliche Zauber auf sie zu {ACTION_cast}.',
 'Arbiter':'Schlichter','Eternity\'s End':'Ewigkeits Ende','Faraway Enclave':'Entlegene Enklave','Frostbite Caverns':'Frosthöhlen','Master of Rift Dancers':'Meister der Dimensionsläufer','Master of Voidlords':'Meister der Leerenfürsten',
 "Target's buffs and debuffs are removed.":'Buffs und Debuffs des Ziels werden entfernt.',
 "As a Pyromancer, you'll make heavy use of the Burning debuff to deal damage to enemies over time. In addition, your own creatures will be afflicted with this debuff, but it will heal and empower them rather than dealing damage.":'Als Pyromantiker nutzt du den Brennen-Debuff intensiv, um Gegnern über Zeit Schaden zuzufügen. Zusätzlich werden auch deine eigenen Kreaturen mit diesem Debuff belegt, aber er heilt und stärkt sie, anstatt ihnen Schaden zuzufügen.',
 'Press {KEYE} to increase this perk\'s rank.':'Drücke {KEYE}, um den Rang dieses Talents zu erhöhen.',
 'After the bearer {ACTION_attacks}, this relic {ACTION_attacks} the enemy as well.':'Nachdem der Träger {ACTION_attacks}, {ACTION_attacks} dieses Relikt den Feind ebenfalls.','Enemies gain 50% less benefit from stat-boosting effects.':'Gegner erhalten 50% weniger Nutzen aus attributssteigernden Effekten.',
 'Master of Arbiters':'Meister der Schlichter','Master of Eggxotics':'Meister der Eggxotics','Master of Fiends':'Meister der Unholde','Master of Gargantuans':'Meister der Gargantuans','Master of Gemlings':'Meister der Edelsteinjünglinge','Master of Hemomancers':'Meister der Blutmagier','Master of Lucanians':'Meister der Lucanians','Master of Luckmantrias':'Meister der Luckmantrias','Master of Nixes':'Meister der Nix','Master of Ophans':'Meister der Ophans','Master of Pit Worms':'Meister der Grubenwürmer','Master of Wights':'Meister der Gruftschrate',
 'Your creatures take 10% less damage while they\'re {ACTION_provoking}.':'Deine Kreaturen erleiden 10% weniger Schaden, während sie {ACTION_provoking} sind.','[bg_squash] Vomiting Squash Is More Rewarding':'[bg_squash] Kotzender Kürbis ist lohnender','You gain 5% more Notoriety from the Gambling Dwarves.':'Du erhältst 5% mehr Berüchtigung von den Glücksspiel-Zwergen.','Your creatures have a 3% chance to ignore incoming debuffs.':'Deine Kreaturen haben eine 3% Chance, eingehende Debuffs zu ignorieren.',
 'Aeolian':'Aeolisch','Arm of Loid':'Arm des Loid','Celestial Orb':'Himmlische Kugel','Death Orb':'Todeskugel','Head of Lost Construct':'Kopf des verlorenen Konstrukts','Imp Impington':'Imp Impington','Nether Orb':'Nether-Kugel','Overkill':'Overkill','Perdition':'Verdammnis','The Swamplands':'Die Sümpfe','Unsullied Meadows':'Unbefleckte Auen','Tigerseye Catbuncle':'Tigeraugen-Katbunkel','Undead Army':'Armee der Untoten','none':'keine','Pay your respects to fallen {CASTLENAME} knights and magi in this Realm.':'Erweise den gefallenen Rittern und Magiern von {CASTLENAME} in diesem Reich deinen Respekt.',
 **{f'Master of Minions {r}':f'Meister der Diener {r}' for r in ('I','II','III','IV','V','VI','VII','VIII','IX','X')},'Minions':'Diener','Minion Master':'Dienermeister','Minion Master Staff':'Stab des Dienermeisters',"[realmprop_f_nominions] Can't Have Minions":'[realmprop_f_nominions] Keine Diener möglich','has > {1} minions':'hat > {1} Diener','has < {1} minions':'hat < {1} Diener',
 **{f'Debuff creatures {n} times.':f'Debuffe Kreaturen {n.replace(",", ".")} Mal.' for n in ('100','250','500','1,000','2,500','5,000','10,000','25,000','50,000','100,000')},**{f'Buff creatures {n} times.':f'Buffe Kreaturen {n.replace(",", ".")} Mal.' for n in ('100','250','500','1,000','2,500','5,000','10,000','25,000','50,000','100,000')},'{1}% Debuff Potency':'{1}% Debuff-Wirksamkeit','Perk Point':'Talentpunkt','Perk Points':'Talentpunkte','Perk Gained:\n{1}':'Talent erhalten:\n{1}',
}
GERMAN_REPL=(('Der nachwuchs ','Der Nachwuchs '),('der nachwuchs ','der Nachwuchs '),('Dienernn','Dienern'),('Merkmalenn','Merkmalen'),('Dieser Relikt','Dieses Relikt'),('einen Debuffs','einen Debuff'))
DEBUFF=re.compile(r'\bdebuffs?\b',re.I);BUFF=re.compile(r'\bbuffs?\b',re.I);MINION=re.compile(r'\bminions?\b',re.I);PERK=re.compile(r'\bperks?\b|\bperk[ -](?:points?|ranks?|menu|screen|list|tree)\b',re.I);NOTORIETY=re.compile(r'\bnotoriety\b',re.I)
def cols(fs):
 lo={x.lower():x for x in fs};return next((lo[x] for x in ('english','en','source','original','text_en','description_en') if x in lo),None),next((lo[x] for x in ('german','de','deutsch','translation','text_de','description_de') if x in lo),None)
def submany(de,pairs):
 for pat,val in pairs:de=re.sub(pat,val,de,flags=re.I)
 return de
def normalize_terms(en,de):
 if DEBUFF.search(en):de=submany(de,[(r'\bSchwächungszustände\b','Debuffs'),(r'\bSchwächungszustand\b','Debuff'),(r'\bSchwächungszaubern\b','Debuffs'),(r'\bSchwächungszauber\b','Debuff'),(r'\bSchwächungen\b','Debuffs'),(r'\bSchwächung\b','Debuff'),(r'\bMalusse\b','Debuffs'),(r'\bMalus\b','Debuff'),(r'\bschwäche\b','Debuffe'),(r'\bschwächen\b','debuffen'),(r'\bschwächt\b','debufft'),(r'\bgeschwächt\b','gedebufft')])
 if BUFF.search(en):de=submany(de,[(r'\bStärkungseffekte\b','Buffs'),(r'\bStärkungseffekt\b','Buff'),(r'\bStärkungszauber\b','Buff'),(r'\bVerstärkungen\b','Buffs'),(r'\bVerstärkung\b','Buff'),(r'\bVerbesserungen\b','Buffs'),(r'\bVerbesserung\b','Buff'),(r'\bStärkungen\b','Buffs'),(r'\bStärkung\b','Buff'),(r'\bverstärke\b','Buffe'),(r'\bverstärken\b','buffen'),(r'\bverstärkt\b','bufft'),(r'\bgestärkt\b','gebufft')])
 if MINION.search(en):de=submany(de,[(r'\bSchergen\b','Diener'),(r'\bLakaien\b','Diener')])
 if PERK.search(en):de=submany(de,[(r'\bSpezialisierungsvorteile\b','Spezialisierungstalente'),(r'\bSpezialisierungsvorteil\b','Spezialisierungstalent'),(r'\bVorteilspunkte\b','Talentpunkte'),(r'\bVorteilspunkt\b','Talentpunkt'),(r'\bFertigkeitspunkte\b','Talentpunkte'),(r'\bFertigkeitspunkt\b','Talentpunkt'),(r'\bVorteilsrang\b','Talentrang'),(r'\bVorteilen\b','Talenten'),(r'\bVorteile\b','Talente'),(r'\bVorteils\b','Talents'),(r'\bVorteil\b','Talent'),(r'\bFertigkeit\b','Talent')])
 if NOTORIETY.search(en):de=submany(de,[(r'\bBerüchtigtheit\b','Berüchtigung'),(r'\bAnsehen\b','Berüchtigung')])
 return de
def main():
 total=0
 for p in sorted(Path('.').glob('*.csv')):
  with p.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fs=r.fieldnames or [];e,d=cols(fs);rows=list(r)
  if not e or not d:continue
  n=0
  for row in rows:
   en=row.get(e,'') or '';old=row.get(d,'') or '';new=normalize_terms(en,EXACT.get(en,old))
   for a,b in GERMAN_REPL:new=new.replace(a,b)
   if new!=old:row[d]=new;n+=1
  if n:
   with p.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
   print(f'{p}: {n} consistency fixes');total+=n
 print(f'total consistency fixes: {total}')
if __name__=='__main__':main()
