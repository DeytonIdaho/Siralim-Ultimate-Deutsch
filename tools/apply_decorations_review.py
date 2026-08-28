#!/usr/bin/env python3
import csv
from pathlib import Path
P=Path('decorations.csv')
EX={'Grim Arbiter':'Finsterer Schlichter','Rift Dancer Plush':'Dimensionsläufer-Plüschtier','Gargantuan Plush':'Gargantuan-Plüschtier','Hemomancer Plush':'Blutmagier-Plüschtier','Fiend Plush':'Unhold-Plüschtier','Death Throne':'Todesthron','Nature Column':'Natursäule','Sorcery Column':'Zaubereisäule','Nature Table':'Naturtisch','Life Table':'Lebenstisch','Death Table':'Todestisch','Birthday Table':'Geburtstagstisch','Basic Table':'Einfacher Tisch','Tenebris\' Table':'Tenebris’ Tisch','Celestial Altar':'Himmlischer Altar','Realm Altar of Perdition':'Reichsaltar von Perdition','Torun\'s Floor Tile':'Toruns Bodenfliese'}
AREA={'Path of the Damned':'Pfad der Verdammten','Swamplands':'Sumpflande','Unsullied Meadows':'Unbefleckte Wiesen','Frostbite Caverns':'Frostbiss-Höhlen','Faraway Enclave':'Ferne Enklave','The Barrens':'Ödlande','Blood Grove':'Bluthain'}
OBJ={'Floor Tile':'Bodenfliese','Mushrooms':'Pilze','Stones':'Steine','Tomb':'Grabmal','Skulls':'Schädel','Flower':'Blume','Tree':'Baum','Log':'Baumstamm','Twigs':'Zweige','Mossy Stones':'moosige Steine','Bones':'Knochen','Skull':'Schädel','Railing':'Geländer','Treasure':'Schatz','Temple':'Tempel','Lodge':'Hütte','Obelisk':'Obelisk','Hyacinth':'Hyazinthe','Flytrap':'Venusfliegenfalle','Mushroom':'Pilz','Fern':'Farn','Berry Bush':'Beerenstrauch','Bush':'Busch','Reeds':'Schilf','Rock':'Felsen','Tent':'Zelt','Gems':'Edelsteine','Feather':'Feder','Totem (Corrupted)':'Totem (verdorben)','Totem':'Totem','Pinwheel':'Windrad','Water':'Wasser','Effigy':'Bildnis','Haybale':'Heuballen','Flowers (A)':'Blumen (A)','Flowers (B)':'Blumen (B)','Sunflower':'Sonnenblume','Sunflowers':'Sonnenblumen','Quicksand':'Treibsand','Oasis':'Oase','Driftwood':'Treibholz','Flowers':'Blumen','Cactus (Tall)':'Kaktus (hoch)','Cactus (Short)':'Kaktus (klein)','Slabs':'Steinplatten','Tumbleweed':'Steppenläufer','Skeleton':'Skelett','Ozymandias':'Ozymandias','Rocks':'Felsen','Squash (1)':'Kürbis (1)','Squash (2)':'Kürbis (2)','Squash (3)':'Kürbis (3)','Firewood':'Brennholz','Pipes':'Rohre','Cave':'Höhle','Trap':'Falle','Stone':'Stein','Big Stone':'Großer Stein','Giant Mushroom':'Riesenpilz','Giant Tree':'Riesenbaum','Campfire':'Lagerfeuer','Flag':'Flagge','Igloo':'Iglu','Frozen Yeti':'Gefrorener Yeti','Grave':'Grab','Diamond':'Diamant','Snowman':'Schneemann','Well':'Brunnen','Puddle':'Pfütze','Debris':'Trümmer','Skeletal Hand':'Skeletthand','Pine Tree':'Kiefer','Snowcap':'Schneekappe','Hut':'Hütte','Juju':'Juju','Conch':'Muschel','Pineapple':'Ananas','Crab':'Krabbe','Dragon Eggs':'Dracheneier','Shipwreck':'Schiffswrack','Plank':'Planke','Grass':'Gras','Planks':'Planken','Starfish':'Seestern'}
def area_name(en):
 for a,de in AREA.items():
  if en.startswith(a+' '):
   obj=en[len(a)+1:]
   if obj in OBJ:return f'{de}: {OBJ[obj]}'
 return None
def main():
 with P.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fs=r.fieldnames or[];lo={x.lower():x for x in fs};e=next(lo[x] for x in ('english','en','source','original') if x in lo);d=next(lo[x] for x in ('german','de','deutsch','translation') if x in lo);rows=list(r)
 n=0
 for row in rows:
  en=row[e];old=row[d];new=EX.get(en,old)
  if 'Perdition' in en:
   new=new.replace('Untergang','Perdition').replace('Verdammnis','Perdition').replace('Verderben','Perdition')
   if en.startswith("Perdition's "):
    obj=en[len("Perdition's "):];mp={'Banner':'Banner','Big Rug':'großer Teppich','Lantern':'Laterne','Chair':'Stuhl','Pillar':'Säule','Long Rug':'langer Teppich','Table':'Tisch','Throne':'Thron','Floor Tile':'Bodenfliese'}
    if obj in mp:new='Perditions '+mp[obj]
  if en=="Aeolian's Pillar":new='Aeolians Säule'
  if en.startswith("Tenebris' Pillar"):new=new.replace('Säule der Finsternis','Tenebris’ Säule')
  new=new.replace('Translator: ','')
  a=area_name(en)
  if a:new=a
  if en.endswith(' Floor Tile') and not a:new=f'{en[:-11]}: Bodenfliese'
  if en=='Swamplands Im Cave':new='Sumpflande: Höhle'
  if en=='Temple Rainbow Well':new='Tempel: Regenbogenbrunnen'
  if new!=old:row[d]=new;n+=1
 with P.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 print(f'decorations review package: {n} rows changed')
if __name__=='__main__':main()
