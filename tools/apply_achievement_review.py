#!/usr/bin/env python3
from __future__ import annotations
import csv,re
from pathlib import Path
PATH=Path('achievements.csv')

def cols(fields):
 low={f.lower():f for f in fields};en=next((low[x] for x in ('english','en','source','original','text_en','description_en') if x in low),None);de=next((low[x] for x in ('german','de','deutsch','translation','text_de','description_de') if x in low),None)
 if not en or not de:raise SystemExit('EN/DE columns not found')
 return en,de

RACES={'Amphisbaenas':'Amphisbaena','Apises':'Apis','Arbiters':'Schlichter','Basilisks':'Basilisken','Cockatrices':'Cockatrice','Cerberuses':'Zerberusse','Diabolic Hordes':'Diabolische Horden','Doom Fortresses':'Festungen des Untergangs','Doomguards':'Doomgarden','Dumplings':'Knödel','Efreets':'Efreet','Fiends':'Unholde','Forsakens':'Verlassene','Gargantuans':'Gargantuans','Giants':'Riesen','Gemlings':'Edelsteinjünglinge','Hounds':'Hunde','Mimics':'Mimiks','Ophans':'Ophans','Paragons':'Paragons','Pilwizes':'Pilwiz','Rift Dancers':'Dimensionsläufer','Godspawns':'Gottesbrut','Animations':'Animationen','Beacons':'Leuchtfeuer','Cherubs':'Cherubim','Chimeras':'Chimären','Clockworks':'Uhrwerke','Electropods':'Elektropoden','Fae':'Fae','Krakens':'Kraken','Luckmantrias':'Luckmantria','Modrons':'Modron','Mythicants':'Mythicant','Nephilims':'Nephilim','Nihilists':'Nihilisten','Spellmanes':'Zaubermähnen','Uraloses':'Uralos','Warhogs':'Kriegseber','Calumniers':'Calumnier','Cataclysms':'Kataklysmen','Effigies':'Abbilder','Lucanians':'Lucanian','Marionettes':'Marionetten','Robodomis':'Robodomi','Spacecats':'Weltraumkatzen','Spelljugglers':'Zauberjongleure','Elementasaurs':'Elementasaurier','Mirelings':'Mireling','Underdwellers':'Unterirdischen','Eggxotics':'Eggxotic','Denizens':'Bewohner'}
FANTASY={'Amphisbaenas','Apises','Cockatrices','Doomguards','Efreets','Forsakens','Gargantuans','Gemlings','Mimics','Ophans','Paragons','Pilwizes','Godspawns','Fae','Luckmantrias','Modrons','Mythicants','Nephilims','Uraloses','Calumniers','Lucanians','Robodomis','Mirelings','Eggxotics'}
RELICS={'Mutatias':'{RELIC_ALEXANDRIA}','Ribcracker':'{RELIC_ARIAMAKI}','Brambleskin':'{RELIC_GENAROS}','Ripplevein':'{RELIC_MUSE}','Fatum and Fortuna':'{RELIC_RECLUSA}','5740-NG':'{RELIC_ROBO}'}

def race_title(src,roman):
 name=RACES[src]
 return f'Meister: {name} {roman}' if src in FANTASY else f'Meister der {name} {roman}'
def race_defeat(src,n):
 name=RACES[src]
 return f'Besiege den Meister der Rasse {name} {n}-mal.' if src in FANTASY else f'Besiege den Meister der {name} {n}-mal.'

def fix(en,de):
 out=de
 m=re.fullmatch(r'The Competent (\{SPECX_[^}]+\}) ([IVX]+)',en)
 if m:return f'Meisterschaft: {m.group(1)} {m.group(2)}'
 m=re.fullmatch(r'Becoming an? (\{SPECX_[^}]+\})',en)
 if m:return f'Spezialisierung: {m.group(1)}'
 m=re.fullmatch(r'Ascended (\{SPECX_[^}]+\})',en)
 if m:return f'Aufstieg: {m.group(1)}'
 m=re.fullmatch(r'Unlock the (\{SPECX_[^}]+\}) specialization\.',en)
 if m:return f'Schalte die Spezialisierung {m.group(1)} frei.'
 m=re.fullmatch(r'Complete ([0-9,]+) Realm Quests using the (\{SPECX_[^}]+\}) specialization\.',en)
 if m:return f'Schließe {m.group(1).replace(",", ".")} Reichsquests mit der Spezialisierung {m.group(2)} ab.'
 m=re.fullmatch(r'Defeat all the gods at Difficulty 10 or higher to Ascend the (\{SPECX_[^}]+\}) specialization\.',en)
 if m:return f'Besiege alle Götter auf Schwierigkeitsstufe 10 oder höher, um mit der Spezialisierung {m.group(1)} aufzusteigen.'
 m=re.fullmatch(r'Slayer of (.+) ([IVX]+)',en)
 if m:return f'Bezwinger von {m.group(1)} {m.group(2)}'
 m=re.fullmatch(r'Favored by (.+) ([IVX]+)',en)
 if m:return f'Begünstigt von {m.group(1)} {m.group(2)}'
 m=re.fullmatch(r'Reach Favor Rank ([0-9]+) with (.+)\.',en)
 if m:return f'Erreiche Gunstrang {m.group(1)} bei {m.group(2)}.'
 m=re.fullmatch(r'Donate resources at (.+?)(?:\'s|’) [Aa]ltar ([0-9,]+) times\.',en)
 if m:return f'Spende {m.group(2).replace(",", ".")}-mal Ressourcen am Altar von {m.group(1)}.'
 m=re.fullmatch(r'Empowering (.+) ([IVX]+)',en)
 if m and m.group(1) in RELICS:return f'{RELICS[m.group(1)]} verstärken {m.group(2)}'
 m=re.fullmatch(r'Earning (.+)',en)
 if m and m.group(1) in RELICS:return f'{RELICS[m.group(1)]} freischalten'
 m=re.fullmatch(r'Empower (\{RELIC_[^}]+\}) (?:up )?to [Rr]ank ([0-9]+)\.',en)
 if m:return f'Verstärke {m.group(1)} bis Rang {m.group(2)}.'
 m=re.fullmatch(r'Unlock (\{RELIC_[^}]+\}) in the Reliquarium\.',en)
 if m:return f'Schalte {m.group(1)} im Reliquiar frei.'
 m=re.fullmatch(r'Master of (.+) ([IVX]+)',en)
 if m and m.group(1) in RACES:return race_title(m.group(1),m.group(2))
 m=re.fullmatch(r'Defeat the Master of (.+) ([0-9]+) times?\.',en)
 if m and m.group(1) in RACES:return race_defeat(m.group(1),m.group(2))
 # Safe generic count normalization: only English rows explicitly using N time/times.
 m=re.fullmatch(r'Defeat (.+) ([0-9]+) times?\.',en)
 if m:return f'Besiege {m.group(1)} {m.group(2)}-mal.'
 exact={"What's In a Name?":"Was steckt in einem Namen?",'Rename your castle.':'Benenne deine Burg um.','Ultimate Experimentation':'Ultimative Experimente','Something Stinks':'Etwas stinkt','Skin Collector I':'Skin-Sammler I'}
 if en in exact:return exact[en]
 out=out.replace('Reliquarium','Reliquiar').replace('Statuswert-steigernde','attributssteigernde').replace('Statuswerte steigernde','attributssteigernde').replace('Reichstiefe','Reichtiefe')
 m=re.fullmatch(r'Glamourous ([IVX]+)',en)
 if m:return f'Glamourös {m.group(1)}'
 m=re.fullmatch(r'Collect ([0-9,]+) Glamour\.',en)
 if m:return f'Sammle {m.group(1).replace(",", ".")} Glamour.'
 return out

def main():
 with PATH.open(encoding='utf-8-sig',newline='') as f:rd=csv.DictReader(f);fields=rd.fieldnames or[];ec,dc=cols(fields);rows=list(rd)
 changed=0
 for row in rows:
  old=row.get(dc,'');new=fix(row.get(ec,''),old)
  if new!=old:row[dc]=new;changed+=1
 with PATH.open('w',encoding='utf-8',newline='') as f:wr=csv.DictWriter(f,fieldnames=fields);wr.writeheader();wr.writerows(rows)
 print(f'achievement review package: {changed} rows changed')
if __name__=='__main__':main()
