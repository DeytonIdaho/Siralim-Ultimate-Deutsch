#!/usr/bin/env python3
from __future__ import annotations
import csv,re
from pathlib import Path
PATH=Path('ui.csv')

def cols(fields):
    low={f.lower():f for f in fields};en=next((low[x] for x in ('english','en','source','original','text_en','description_en') if x in low),None);de=next((low[x] for x in ('german','de','deutsch','translation','text_de','description_de') if x in low),None)
    if not en or not de:raise SystemExit('EN/DE columns not found')
    return en,de

EXACT={
 '[fae_dreamcatch] Dream Catchers Grant a Minion':'[fae_dreamcatch] Traumfänger gewähren einen Diener',
 '[fc_grave] Mummy Graves Afflict Enemies With a Debuff':'[fc_grave] Mumiengräber belegen Feinde mit einem Debuff',
 '[bns_relic] Relics Grant Crystal':'[bns_relic] Relikte gewähren Kristalle',
 '[cr_potion] Potions Grant a Minion':'[cr_potion] Tränke gewähren einen Diener',
 '[lobab_robes] Arbiter Robes Drop Treasure':'[lobab_robes] Schlichtergewänder lassen Schätze fallen',
 '[lobab_robes] 25% Chance to Receive Emblem From Arbiter Robes':'[lobab_robes] 25% Chance, ein Emblem von Schlichtergewändern zu erhalten',
 '[cr_cache] Caches Kill Random Enemy In Next Battle':'[cr_cache] Caches töten im nächsten Kampf einen zufälligen Gegner',
 '[fae_fae] Fae Drop Treasure':'[fae_fae] Fae lassen Schätze fallen',
 '[ot_orb] Mysterious Orbs Reward 1 Emblem':'[ot_orb] Mysteriöse Kugeln gewähren 1 Emblem',
 '[bg_trap] +50% Favor From Traps':'[bg_trap] +50% Gunst durch Fallen',
 '[bg_trap] Traps Grant Essence':'[bg_trap] Fallen gewähren Essenz',
 '[bg_trap] Traps Damage Enemies':'[bg_trap] Fallen fügen Feinden Schaden zu',
 '[fdp_musiccrystals] Music Crystals Are More Rewarding':'[fdp_musiccrystals] Musiksteine sind lohnender',
 '[cj_fruity] Vomiting Fruit Is More Rewarding':'[cj_fruity] Erbrechende Früchte sind lohnender',
 '[ot_vines] Snaptrap Vines Drop Treasure':'[ot_vines] Schnappfallen-Ranken lassen Schätze fallen',
 'Ruthless':'Unbarmherzig',
 'Choose your Advanced New Game options.':'Wähle deine Optionen für Neues Spiel Plus.',
 'Select a creature to summon. Cost: [resource_essence] 1000':'Wähle eine Kreatur zum Beschwören aus. Kosten: [resource_essence] 1000',
}

def fix(en,de):
    if en in EXACT:return EXACT[en]
    out=de
    # Damage Enemies is verbal in English: translate structurally, never by blind capitalization.
    m=re.fullmatch(r'(\[[^]]+\]) (.+) Damage Enemies',en)
    if m:
        prefix=m.group(1)
        # Preserve the translated subject from the existing German where possible.
        subject=re.sub(r'^\[[^]]+\]\s*','',out)
        subject=re.split(r'\s+(?:schaden|Schaden|fügen|fuegen)\b',subject,maxsplit=1)[0].strip()
        if subject:return f'{prefix} {subject} fügen Feinden Schaden zu'
    # Noun damage contexts can safely use capitalized Schaden.
    if re.search(r'\b(?:damage|Damage)\b',en) and 'Damage Enemies' not in en:
        out=re.sub(r'\bschaden\b','Schaden',out)
    out=out.replace('Richterroben','Schlichterroben').replace('Richtergewänder','Schlichtergewänder')
    out=out.replace('Statuswert-Verstärkungen','Attributsboni').replace('Statuswertverstärkung','Attributsbonus')
    for a,b in [(' Sind ',' sind '),(' Ist ',' ist '),(' Im Nächsten Kampf',' im nächsten Kampf'),(' Zufälligen ',' zufälligen '),(' Zufälliger ',' zufälliger '),(' Mit Einem ',' mit einem '),(' Belegen ',' belegen '),(' Gewähre ',' gewähren '),(' Auf',' auf')]:out=out.replace(a,b)
    if '"Ruthless"' in en:out=out.replace('"Gnadenlos"','"Unbarmherzig"')
    out=out.replace('Geschichten-Überspringen-Modus','Modus „Story überspringen“')
    return out

def main():
    with PATH.open(encoding='utf-8-sig',newline='') as f:rd=csv.DictReader(f);fields=rd.fieldnames or[];ec,dc=cols(fields);rows=list(rd)
    changed=0
    for row in rows:
        old=row.get(dc,'');new=fix(row.get(ec,''),old)
        if new!=old:row[dc]=new;changed+=1
    with PATH.open('w',encoding='utf-8',newline='') as f:wr=csv.DictWriter(f,fieldnames=fields);wr.writeheader();wr.writerows(rows)
    print(f'ui review package: {changed} rows changed')
if __name__=='__main__':main()
