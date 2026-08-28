#!/usr/bin/env python3
import csv,re
from pathlib import Path
P=Path('dialog_story.csv')
def main():
 with P.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fs=r.fieldnames or[];lo={x.lower():x for x in fs};e=next(lo[x] for x in ('english','en','source','original') if x in lo);d=next(lo[x] for x in ('german','de','deutsch','translation') if x in lo);rows=list(r)
 n=0
 for row in rows:
  en=row[e];old=row[d];new=old
  # Established relic terminology; preserve grammar around the term.
  new=re.sub(r'Ultimativ(?:e|en|er|em|es)? Nether-(?:Kugel|kugel|Orb)',lambda m:'Ultimativen Nether-Orb' if m.group(0).startswith('Ultimativen') else ('Ultimativer Nether-Orb' if m.group(0).startswith('Ultimativer') else 'Ultimative Nether-Orb'),new)
  new=new.replace('Ultimative Netherkugel','Ultimativer Nether-Orb').replace('Ultimativen Netherkugel','Ultimativen Nether-Orb')
  for x in ('Niederen Nether-Kugeln','Niederen Netherkugeln','Niederen Netherperlen','Niederen Ätherorben','Kleineren Netherorbs'):new=new.replace(x,'Niederen Nether-Orbs')
  new=new.replace('Niedere Nether-Kugeln','Niedere Nether-Orbs').replace('Niederen Nether-Kugel','Niederen Nether-Orb')
  new=new.replace('Nether-Kugeln','Nether-Orbs').replace('Netherkugeln','Nether-Orbs')
  # Named lesser orbs.
  new=new.replace('Naturkugel','Natur-Orb').replace('Naturorb','Natur-Orb').replace('Magie-Kugel','Zauberei-Orb').replace('Zaubererkugel','Zauberei-Orb').replace('Zauberei-Kugel','Zauberei-Orb').replace('Zauberkunst-Orb','Zauberei-Orb')
  # Established realm terminology.
  new=new.replace('Unbefleckten Auen','Unbefleckten Wiesen').replace('Unbefleckte Auen','Unbefleckte Wiesen')
  new=new.replace('Ewigkeits Ende','Ende der Ewigkeit')
  # Clear factual/grammar error: Kiichi is explicitly female.
  if 'Kiichi' in en:new=new.replace('Als er deine Ankunft bemerkt','Als sie deine Ankunft bemerkt')
  # Reconstruct only clearly truncated story lines.
  if en.startswith('(You try to say, "Yes! Of course I know of Nex.'):
   new='(Du versuchst zu sagen: „Ja! Natürlich kenne ich Nex. Sie sind unser engster Verbündeter, und wir tauschen oft Eingemachtes miteinander“, aber du kannst immer noch nicht sprechen.)'
  if en.startswith("Everett:\n{PLAYERNAME}, I'd offer to make the pilgrimage across Rodia"):
   new='Everett:\n{PLAYERNAME}, ich würde anbieten, an deiner Stelle durch Rodia zu reisen und die Götter zu warnen, aber wir wissen beide, dass du für diese Aufgabe besser geeignet bist. Diplomatie war noch nie meine Stärke. Außerdem werden die Götter dich als Herrscher von Siralim deutlich ernster nehmen als mich.'
  if en.startswith('(That\'s easy. "A map", you attempt to answer'):
   new='(Das ist einfach. „Eine Karte“, versuchst du mit einem selbstgefälligen Grinsen zu antworten, doch stattdessen weht dir eine Handvoll Sand in den Mund.)'
  if new!=old:row[d]=new;n+=1
 with P.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 print(f'dialog story gentle review: {n} rows changed')
if __name__=='__main__':main()
