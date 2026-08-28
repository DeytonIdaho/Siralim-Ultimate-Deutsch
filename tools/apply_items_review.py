#!/usr/bin/env python3
import csv,re
from pathlib import Path
P=Path('items.csv')
EX={'Astro Soul':'Astroseele','Goldblight Claymore':'Goldfluch-Claymore','Vivifier Horseshoe':'Belebendes Hufeisen','Perdition Helmet':'Perdition-Helm','Executioner Prism':'Henker-Prisma','Palace Pinion':'Palast-Schwinge','Dreadful Ashes':'Schreckliche Asche','Change Figment':'Wandel-Trugbild','Hebron\'s Broken Plate':'Hebrons zerbrochene Platte','Apprentice Plasma':'Lehrlingsplasma','Sludgechemist Gel':'Schleimchemiker-Gel','Abyssal Phylactery':'Abyssales Phylakterium','Rose Amber':'Rosenbernstein','Freak Stake':'Freak-Pfahl','Villous Carrot':'Haarige Karotte','Die Fragments':'Würfelfragmente','Contrary Clock':'Widersinnige Uhr','Sigil of the Arbiter':'Siegel des Schlichters','Reaver (Alternate)':'Reaver (Alternativ)','Aeolian':'Aeolian','Perdition':'Perdition','Void Queen':'Leerenkönigin','Spotted':'Gefleckt','Master of Arbiters':'Meister der Schlichter'}
RACE={'Voidlord':'Leerenfürst','Nix':'Nix','Pit Worm':'Grubenwurm','Rift Dancer':'Dimensionsläufer','Hemomancer':'Blutmagier','Fiend':'Unhold','Gargantuan':'Gargantuan','Forsaken':'Verlassener','Gemling':'Edelsteinjüngling','Arbiter':'Schlichter','Lucanian':'Lucanian','Eggxotic':'Eggxotic'}
MASTER={'Fiends':'Unholde','Forsakens':'Verlassene','Gargantuans':'Gargantuans','Gemlings':'Edelsteinjünglinge','Hemomancers':'Blutmagier','Nixes':'Nix','Ophans':'Ophans','Pit Worms':'Grubenwürmer','Rift Dancers':'Dimensionsläufer','Voidlords':'Leerenfürsten','Arbiters':'Schlichter','Lucanians':'Lucanians','Eggxotics':'Eggxotics'}
def main():
 with P.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fs=r.fieldnames or[];lo={x.lower():x for x in fs};e=next(lo[x] for x in ('english','en','source','original') if x in lo);d=next(lo[x] for x in ('german','de','deutsch','translation') if x in lo);rows=list(r)
 n=0
 for row in rows:
  en=row[e];old=row[d];new=EX.get(en,old)
  # Reaver is an intentionally retained class name.
  if en.startswith('Reaver (Tier '):new=en.replace('Tier','Stufe')
  if en=="Reaver's Skull":new='Reavers Schädel'
  # Creature sigils follow established creature terminology.
  if en.startswith('Sigil of the '):
   race=en[len('Sigil of the '):]
   if race in RACE:new='Siegel des '+RACE[race]
   if race=='Mimic':new='Siegel des Mimics'
   if race=='Cockatrice':new='Siegel der Cockatrice'
  if en.startswith('Master of '):
   race=en[len('Master of '):]
   if race in MASTER:new='Meister der '+MASTER[race]
  # Item family: Orb is a named object, unlike the random-name word fragment later in the file.
  if en.endswith(' Orb') and en!='Orb':
   stem=en[:-4];m={'Raptor':'Raptor','Disciple':'Jünger','Zealot':'Eiferer','Mirage':'Trugbild','Delusion':'Illusion','Celestial':'Himmels','Spider':'Spinnen','Viper':'Vipern','Spellbinder':'Zauberbinder'}
   if stem in m:new=m[stem]+'-Orb'
  # Preserve bottle pun/fantasy names.
  if en.startswith('Bottle of '):new='Flasche '+en[len('Bottle of '):]
  # Crippler family consistency.
  crip={'Life':'Lebensschwächer','Death':'Todesschwächer','Chaos':'Chaosschwächer','Sorcery':'Zaubereischwächer','Nature':'Naturschwächer'}
  if en.endswith(' Crippler') and en[:-9] in crip:new=crip[en[:-9]]
  new=new.replace('Translator: ','').replace('Entfesselter Schlange','Entfesselte Schlange').replace('Ritualistischer Totem','Ritualisten-Totem').replace('Unaufhörlicher Spucke','Unaufhörliche Spucke').replace('Chromas Befleckte Juwel','Chromas beflecktes Juwel').replace('Kühnes Bernstein','Kühner Bernstein').replace('Krallendes Kamm','Krallender Kamm')
  # Mechanical Gear family.
  if en.endswith(' Gear') and en not in ('Technomancer Gear',):new=new.replace('Ausrüstung','Getriebe')
  # Rules terminology in item descriptions.
  if 'Stat Potency' in en:new=new.replace('Statuswirksamkeit','Attributswirksamkeit')
  if 'stat changes' in en:new=new.replace('Statusänderungen','Attributsänderungen')
  if "Nether Slot" in en:new=new.replace('Äther-Sockel','Nether-Sockel')
  if en=='{1} I':new='{1} I'
  # God names remain proper names.
  if en.startswith('Emblem of '):
   god=en[len('Emblem of '):]
   if god in ('Aeolian','Perdition','Mortem','Tenebris'):new='Emblem von '+god
  if new!=old:row[d]=new;n+=1
 with P.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 print(f'items review package: {n} rows changed')
if __name__=='__main__':main()
