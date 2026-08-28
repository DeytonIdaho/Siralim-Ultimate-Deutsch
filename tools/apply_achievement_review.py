#!/usr/bin/env python3
from __future__ import annotations
import csv,re
from pathlib import Path

PATH=Path('achievements.csv')

def cols(fields):
    low={f.lower():f for f in fields}
    en=next((low[x] for x in ('english','en','source','original','text_en','description_en') if x in low),None)
    de=next((low[x] for x in ('german','de','deutsch','translation','text_de','description_de') if x in low),None)
    if not en or not de: raise SystemExit('EN/DE columns not found')
    return en,de

def roman(s): return s.strip()

# Reviewed race names. Invented Siralim names are deliberately preserved.
RACES={
 'Amphisbaenas':'Amphisbaena','Apises':'Apis','Arbiters':'Schlichter','Basilisks':'Basilisken',
 'Cockatrices':'Cockatrice','Cerberuses':'Zerberusse','Diabolic Hordes':'Diabolische Horden',
 'Doom Fortresses':'Festungen des Untergangs','Doomguards':'Doomgarden','Dumplings':'Knödel',
 'Efreets':'Efreet','Fiends':'Unholde','Forsakens':'Verlassene','Gargantuans':'Gargantuans',
 'Giants':'Riesen','Gemlings':'Edelsteinjünglinge','Hounds':'Hunde','Mimics':'Mimiks','Ophans':'Ophans',
 'Paragons':'Paragons','Pilwizes':'Pilwiz','Rift Dancers':'Dimensionsläufer','Godspawns':'Gottesbrut',
 'Animations':'Animationen','Beacons':'Leuchtfeuer','Cherubs':'Cherubim','Chimeras':'Chimären',
 'Clockworks':'Uhrwerke','Electropods':'Elektropoden','Fae':'Fae','Krakens':'Kraken','Luckmantrias':'Luckmantria',
 'Modrons':'Modron','Mythicants':'Mythicant','Nephilims':'Nephilim','Nihilists':'Nihilisten',
 'Spellmanes':'Zaubermähnen','Uraloses':'Uralos','Warhogs':'Kriegseber','Calumniers':'Calumnier',
 'Cataclysms':'Kataklysmen','Effigies':'Abbilder','Lucanians':'Lucanian','Marionettes':'Marionetten',
 'Robodomis':'Robodomi','Spacecats':'Weltraumkatzen','Spelljugglers':'Zauberjongleure',
 'Elementasaurs':'Elementasaurier','Mirelings':'Mireling','Underdwellers':'Unterirdische','Eggxotics':'Eggxotic',
 'Denizens':'Bewohner'
}

def fix(en,de):
    out=de
    # Specialization achievements: grammar-safe token based titles.
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

    # Slayer series: one title throughout.
    m=re.fullmatch(r'Slayer of (.+) ([IVX]+)',en)
    if m:return f'Bezwinger von {m.group(1)} {m.group(2)}'

    # God favor/donation series.
    m=re.fullmatch(r'Favored by (.+) ([IVX]+)',en)
    if m:return f'Begünstigt von {m.group(1)} {m.group(2)}'
    m=re.fullmatch(r'Reach Favor Rank ([0-9]+) with (.+)\.',en)
    if m:return f'Erreiche Gunstrang {m.group(1)} bei {m.group(2)}.'
    m=re.fullmatch(r'Donate resources at (.+?)(?:\'s|’) Altar ([0-9,]+) times\.',en)
    if m:return f'Spende {m.group(2).replace(",", ".")}-mal Ressourcen am Altar von {m.group(1)}.'

    # Relic achievements: keep the token/name authoritative instead of retranslating it per rank.
    m=re.fullmatch(r'Empowering (\{RELIC_[^}]+\}) ([IVX]+)',en)
    if m:return f'{m.group(1)} verstärken {m.group(2)}'
    m=re.fullmatch(r'Earning (\{RELIC_[^}]+\})',en)
    if m:return f'{m.group(1)} freischalten'
    m=re.fullmatch(r'Empower (\{RELIC_[^}]+\}) to Rank ([0-9]+)\.',en)
    if m:return f'Verstärke {m.group(1)} bis Rang {m.group(2)}.'
    m=re.fullmatch(r'Unlock (\{RELIC_[^}]+\}) in the Reliquarium\.',en)
    if m:return f'Schalte {m.group(1)} im Reliquiar frei.'

    # Master-of-race series. Preserve invented race names according to creatures review.
    m=re.fullmatch(r'Master of (.+) ([IVX]+)',en)
    if m and m.group(1) in RACES:return f'Meister der {RACES[m.group(1)]} {m.group(2)}'
    m=re.fullmatch(r'Defeat the Master of (.+) ([0-9]+) times?\.',en)
    if m and m.group(1) in RACES:return f'Besiege den Meister der {RACES[m.group(1)]} {m.group(2)}-mal.'

    # Reviewed individual fixes.
    exact={
      "What's In a Name?":"Was steckt in einem Namen?",
      'Rename your castle.':'Benenne deine Burg um.',
      'Ultimate Experimentation':'Ultimative Experimente',
      'Something Stinks':'Etwas stinkt',
      'Skin Collector I':'Skin-Sammler I',
    }
    if en in exact:return exact[en]

    # Global reviewed terminology in this file.
    out=out.replace('Reliquarium','Reliquiar').replace('Statuswert-steigernde','attributssteigernde').replace('Statuswerte steigernde','attributssteigernde')
    out=out.replace('Reichstiefe','Reichtiefe')

    # Glamourous series + the known X-value mistranslation.
    m=re.fullmatch(r'Glamourous ([IVX]+)',en)
    if m:return f'Glamourös {m.group(1)}'
    m=re.fullmatch(r'Collect ([0-9,]+) Glamour\.',en)
    if m:return f'Sammle {m.group(1).replace(",", ".")} Glamour.'
    return out

def main():
    if not PATH.exists(): raise SystemExit('achievements.csv not found')
    with PATH.open(encoding='utf-8-sig',newline='') as f:
        rd=csv.DictReader(f); fields=rd.fieldnames or []; ec,dc=cols(fields); rows=list(rd)
    changed=0
    for row in rows:
        old=row.get(dc,''); new=fix(row.get(ec,''),old)
        if new!=old: row[dc]=new; changed+=1
    with PATH.open('w',encoding='utf-8',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=fields); wr.writeheader(); wr.writerows(rows)
    print(f'achievement review package: {changed} rows changed')

if __name__=='__main__':main()
