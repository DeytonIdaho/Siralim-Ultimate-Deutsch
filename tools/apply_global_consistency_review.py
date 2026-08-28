#!/usr/bin/env python3
"""Apply confirmed cross-file consistency fixes."""
import csv,re
from pathlib import Path
ITEMSETS_DE='Ausrüstungssets ermöglichen es dir, Gruppen von Artefakten und Zaubersteinen einfach zu speichern und zu laden. Du kannst diese Ausrüstungssets verwenden, um deine Kreaturen schnell mit verschiedenen Artefakten und Zaubersteinen auszurüsten.\n\nUm ein Ausrüstungsset zu erstellen, öffne das Menü und wähle „Kreaturen“. Wähle anschließend eine Kreatur und dann „Ausrüstungssets verwalten“. Es erscheint ein neues Menü, in dem du die derzeit ausgerüsteten Gegenstände dieser Kreatur über „Zuweisen“ einem Ausrüstungsset zuordnen kannst. Später kannst du mit der Option „Ausrüsten“ schnell die in diesem Ausrüstungsset enthaltenen Gegenstände anlegen.'
EXACT={'Daybreaker':'Tagesbrecher','{CONDNAME_DEBUFF_CONFUSED} creatures have a 50% chance to {ACTION_attack} or {ACTION_cast} harmful spells on their allies.':'{CONDNAME_DEBUFF_CONFUSED} Kreaturen haben eine 50% Chance, ihre Verbündeten zu {ACTION_attack} oder schädliche Zauber auf sie zu {ACTION_cast}.','At the start of battle, this creature\'s spells with the "Cascading" property gain 4 additional maximum {STAT_charges} for each unique class among your creatures. Does not work on {SPELL_ultimate}s.':'Zu Kampfbeginn erhalten die Zauber dieser Kreatur mit der Eigenschaft „Kaskadierend“ 4 zusätzliche maximale {STAT_charges} für jede einzigartige Klasse unter deinen Kreaturen. Funktioniert nicht bei {SPELL_ultimate}s.','Arbiter':'Schlichter','Eternity\'s End':'Ewigkeits Ende','Faraway Enclave':'Entlegene Enklave','Frostbite Caverns':'Frosthöhlen','Master of Rift Dancers':'Meister der Dimensionsläufer','Master of Voidlords':'Meister der Leerenfürsten',"Target's buffs and debuffs are removed.":'Buffs und Debuffs des Ziels werden entfernt.','Press {KEYE} to increase this perk\'s rank.':'Drücke {KEYE}, um den Rang dieses Talents zu erhöhen.','Master of Arbiters':'Meister der Schlichter','Perk Point':'Talentpunkt','Perk Points':'Talentpunkte','Perk Gained:\n{1}':'Talent erhalten:\n{1}',**{f'Master of Minions {r}':f'Meister der Diener {r}' for r in ('I','II','III','IV','V','VI','VII','VIII','IX','X')},**{f'Debuff creatures {n} times.':f'Debuffe Kreaturen {n.replace(",", ".")} Mal.' for n in ('100','250','500','1,000','2,500','5,000','10,000','25,000','50,000','100,000')},**{f'Buff creatures {n} times.':f'Buffe Kreaturen {n.replace(",", ".")} Mal.' for n in ('100','250','500','1,000','2,500','5,000','10,000','25,000','50,000','100,000')}}
GERMAN_REPL=(('Dienernn','Dienern'),('Merkmalenn','Merkmalen'),('Dieser Relikt','Dieses Relikt'),('einen Debuffs','einen Debuff'))
DEBUFF=re.compile(r'\bdebuffs?\b',re.I);BUFF=re.compile(r'\bbuffs?\b',re.I);MINION=re.compile(r'\bminions?\b',re.I);PERK=re.compile(r'\bperks?\b|\bperk[ -](?:points?|ranks?|menu|screen|list|tree)\b',re.I);NOTORIETY=re.compile(r'\bnotoriety\b',re.I)
def cols(fs):
 lo={x.lower():x for x in fs};return next((lo[x] for x in ('english','en','source','original','text_en','description_en') if x in lo),None),next((lo[x] for x in ('german','de','deutsch','translation','text_de','description_de') if x in lo),None)
def submany(de,pairs):
 for pat,val in pairs:de=re.sub(pat,val,de,flags=re.I)
 return de
def normalize_terms(en,de):
 if DEBUFF.search(en):de=submany(de,[(r'\bSchwächungszustände\b','Debuffs'),(r'\bSchwächungszustand\b','Debuff'),(r'\bSchwächungen\b','Debuffs'),(r'\bSchwächung\b','Debuff'),(r'\bMalusse\b','Debuffs'),(r'\bMalus\b','Debuff'),(r'\bschwäche\b','Debuffe'),(r'\bschwächen\b','debuffen'),(r'\bschwächt\b','debufft'),(r'\bgeschwächt\b','gedebufft')])
 if BUFF.search(en):de=submany(de,[(r'\bVerstärkungen\b','Buffs'),(r'\bVerstärkung\b','Buff'),(r'\bVerbesserungen\b','Buffs'),(r'\bVerbesserung\b','Buff'),(r'\bStärkungen\b','Buffs'),(r'\bStärkung\b','Buff'),(r'\bverstärke\b','Buffe'),(r'\bverstärken\b','buffen'),(r'\bverstärkt\b','bufft'),(r'\bgestärkt\b','gebufft')])
 if MINION.search(en):de=submany(de,[(r'\bSchergen\b','Diener'),(r'\bLakaien\b','Diener')])
 if PERK.search(en):de=submany(de,[(r'\bSpezialisierungsvorteile\b','Spezialisierungstalente'),(r'\bSpezialisierungsvorteil\b','Spezialisierungstalent'),(r'\bVorteilspunkte\b','Talentpunkte'),(r'\bVorteilspunkt\b','Talentpunkt'),(r'\bFertigkeitspunkte\b','Talentpunkte'),(r'\bFertigkeitspunkt\b','Talentpunkt'),(r'\bVorteilsrang\b','Talentrang'),(r'\bVorteilen\b','Talenten'),(r'\bVorteile\b','Talente'),(r'\bVorteils\b','Talents'),(r'\bVorteil\b','Talent'),(r'\bFertigkeit\b','Talent')])
 if NOTORIETY.search(en):de=submany(de,[(r'\bBerüchtigtheit\b','Berüchtigung'),(r'\bAnsehen\b','Berüchtigung')])
 return de
def is_itemsets(en):
 # Robust semantic key: avoids differences in CRLF/LF, literal \n, quotes, or whitespace.
 s=re.sub(r'\s+',' ',en.replace('\\n',' ').replace('\r',' ').replace('\n',' ')).strip()
 return s.startswith('Item Sets allow you to easily save and load groups of Artifacts and Spell Gems.') and 'Manage Item Sets' in s and 'Assign' in s and 'Equip' in s
def main():
 total=0
 for p in sorted(Path('.').glob('*.csv')):
  with p.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fs=r.fieldnames or [];e,d=cols(fs);rows=list(r)
  if not e or not d:continue
  n=0
  for row in rows:
   en=row.get(e,'') or '';old=row.get(d,'') or ''
   new=ITEMSETS_DE if is_itemsets(en) else EXACT.get(en,old);new=normalize_terms(en,new)
   for a,b in GERMAN_REPL:new=new.replace(a,b)
   if new!=old:row[d]=new;n+=1
  if n:
   with p.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
   print(f'{p}: {n} consistency fixes');total+=n
 print(f'total consistency fixes: {total}')
if __name__=='__main__':main()
