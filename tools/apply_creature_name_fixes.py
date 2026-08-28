#!/usr/bin/env python3
import csv
from pathlib import Path

# Manually reviewed, tag-specific corrections only.
# Wight deliberately remains a distinct family from Revenant (Wiedergänger).
FIX={
'L_FAMILIAR':'Vertrauter','L_LEECH':'Blutegel','L_MIMIC':'Mimic','L_EFREET':'Ifrit','L_WIGHT':'Wight',
'L_CRIT_FLAMEGRIPCLUTCHER':'Flammengriff-Greifer',
'L_CRIT_SAVAGEBANSHEE':'Wilde Banshee','L_CRIT_IMPALERBANSHEE':'Pfähler-Banshee',
'L_CRIT_PULSEBAT':'Pulsfledermaus','L_CRIT_PELLUCIDBEACON':'Klares Leuchtfeuer',
'L_CRIT_CLOTHABOMINATION':'Stoff-Abscheulichkeit','L_CRIT_WILLOWCONSTRUCT':'Weidenkonstrukt',
'L_CRIT_CINDERDEVIL':'Glutteufel','L_CRIT_VEGETABLEDUMPLING':'Gemüseknödel',
'L_CRIT_HEMLOCKENT':'Hemlock-Ent','L_CRIT_FLOODFAMILIAR':'Flut-Vertrauter',
'L_CRIT_INKJETKRAKEN':'Tintenstrahl-Kraken','L_CRIT_GIFTMIMIC':'Geschenk-Mimic',
'L_CRIT_WOEFULSPECTRE':'Klagendes Gespenst','L_CRIT_HOLIDAYSPIRIT':'Feiertagsgeist',
'L_CRIT_QUARNOKTREMOR':'Quarnok-Beben','L_CRIT_GORLUMTREMOR':'Gorlum-Beben',
'L_CRIT_SKYWARDVULPES':'Himmels-Vulpes','L_CRIT_PLATEDWARHOG':'Gepanzerter Kriegseber',
'L_CRIT_UNDERDWELLERMISCHIEFMAKER':'Unterirdischer Unheilstifter','L_CRIT_UNDERDWELLERFEARMONGER':'Unterirdischer Angstmacher',
'L_CRIT_TERRORWIGHT':'Terror-Wight','L_CRIT_GRAVEBANEWIGHT':'Grabfluch-Wight','L_CRIT_RECLUSIVEWIGHT':'Zurückgezogener Wight','L_CRIT_ROOFSTALKERWIGHT':'Dachschleicher-Wight','L_CRIT_DREADWIGHT':'Schreckens-Wight','L_CRIT_TREPIDATIONWIGHT':'Angst-Wight','L_CRIT_FROSTBITEWIGHT':'Frostbiss-Wight','L_CRIT_HEADLESSWIGHT':'Kopfloser Wight','L_CRIT_HOLYWIGHT':'Heiliger Wight',
'L_CRIT_WILDFIREEFREET':'Wildfeuer-Ifrit','L_CRIT_VOLCANICEFREET':'Vulkanischer Ifrit','L_CRIT_FROSTFIREEFREET':'Frostfeuer-Ifrit','L_CRIT_OBSIDIANEFREET':'Obsidian-Ifrit','L_CRIT_DREADFULEFREET':'Schrecklicher Ifrit','L_CRIT_ASHBONEEFREET':'Aschenknochen-Ifrit','L_CRIT_FLAMETONGUEEFREET':'Flammenzungen-Ifrit',
'L_CRIT_DJINNEVOKER':'Djinn-Beschwörer','L_CRIT_VENGEFULDJINN':'Rachsüchtiger Djinn','L_CRIT_UNCHAINEDDJINN':'Entfesselter Djinn',
}
P=Path('creatures.csv')
with P.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fields=r.fieldnames or [];rows=list(r)
changed=[];seen=set()
for row in rows:
 tag=row.get('Tag','')
 if tag in FIX:
  seen.add(tag);old=row.get('German','');new=FIX[tag]
  if old!=new:row['German']=new;changed.append((tag,old,new))
missing=set(FIX)-seen
if missing:raise SystemExit('Missing reviewed tags: '+', '.join(sorted(missing)))
with P.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
print('changes',len(changed))
for x in changed:print('FIX | '+' | '.join(x))
