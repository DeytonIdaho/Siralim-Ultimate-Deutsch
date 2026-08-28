#!/usr/bin/env python3
import csv,re
from pathlib import Path
P=Path('creatures.csv')
EX={'Forsaken':'Verlassener','Pit Worm':'Grubenwurm','Nix':'Nix','Gargantuan':'Gargantuan','Arbiter':'Schlichter','Eggxotic':'Eggxotic','Lucanian':'Lucanian','Ugat':'Ugat','Aeolian':'Aeolian','Apis Endurer':'Apis-Erdulder','Skull Devil':'Schädelteufel','Treat Imling':'Treat-Imling','Sticky Snaptrap':'Klebrige Schnappfalle'}
def main():
 with P.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fs=r.fieldnames or[];lo={x.lower():x for x in fs};e=next(lo[x] for x in ('english','en','source','original') if x in lo);d=next(lo[x] for x in ('german','de','deutsch','translation') if x in lo);rows=list(r)
 n=0
 for row in rows:
  en=row[e];old=row[d];new=EX.get(en,old)
  if 'Pit Worm' in en:new=new.replace('Grubendrachen','Grubenwurm').replace('Grubendrache','Grubenwurm').replace('Grubenkreatur','Grubenwurm')
  if 'Rift Dancer' in en:
   prefix=en.rsplit(' Rift Dancer',1)[0]
   new=('Dimensionsläufer' if not prefix else prefix+'-Dimensionsläufer')
  if 'Nix ' in en:new=new.replace('Nichts-','Nix-').replace('Nichts ','Nix ')
  if 'Gargantuan' in en:
   adj=en.rsplit(' Gargantuan',1)[0]
   amap={'Monstrous':'Monströser','Sturdy':'Robuster','Shackled':'Gefesselter','Daunting':'Bedrohlicher','Fearsome':'Furchterregender','Forest':'Wald-','Gruesome':'Grausiger','Volcanic':'Vulkanischer'}
   if adj in amap:new=(amap[adj]+'Gargantuan' if amap[adj].endswith('-') else amap[adj]+' Gargantuan')
  if 'Gemling' in en:
   new=new.replace('Edelsteinjüngling','Edelsteinjüngling')
   if en!='Gemling':
    stem=en.rsplit(' Gemling',1)[0]
    sm={'Crystaldune':'Kristalldünen','Eternaldew':'Ewigstau','Nightvelvet':'Nachtsamt','Rockmoss':'Felsmoos','Stillfire':'Stillfeuer','Whitestar':'Weißstern'}
    if stem in sm:new=sm[stem]+'-Edelsteinjüngling'
  if 'Hemomancer' in en:new=new.replace('Hämomant','Blutmagier').replace('Hämomanten','Blutmagier')
  if 'Voidlord' in en:new=new.replace('Leerefürst','Leerenfürst')
  if en=='Unguided Judge':new='Ungeführter Richter'
  if en=='Nix Guardian':new='Nix-Wächter'
  if new!=old:row[d]=new;n+=1
 with P.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 print(f'creatures review package: {n} rows changed')
if __name__=='__main__':main()
