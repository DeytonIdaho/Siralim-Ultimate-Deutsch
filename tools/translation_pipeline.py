#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,re
from collections import Counter
from pathlib import Path
TOKEN_RE=re.compile(r"(?:\{[^{}]+\}|\[[^\[\]]+\]|<[^<>]+>|%\w|\\n)")
TERMS={"Creature":"Kreatur","Creatures":"Kreaturen","Trait":"Merkmal","Traits":"Merkmale","Minion":"Diener","Spell Gem":"Zauberstein","Spell Gems":"Zaubersteine"}
def norm(s):return(s or"").strip()
def toks(s):return Counter(TOKEN_RE.findall(s or""))
def cols(fs):
 low={f.lower():f for f in fs}
 def p(ns):
  for n in ns:
   if n in low:return low[n]
 a=p(["english","en","source","original","text_en","description_en"]);b=p(["german","de","deutsch","translation","text_de","description_de"])
 if not a or not b:raise SystemExit("EN/DE columns not found")
 return a,b
def fix(en,de):
 out=de or""
 for p,r in [(r"Zauberjuwel","Zauberstein"),(r"Zauber-Edelsteine","Zaubersteine"),(r"Zauber-Edelstein","Zauberstein"),(r"Zauberedelsteine","Zaubersteine"),(r"Zauberedelstein","Zauberstein"),(r"Zaubergems","Zaubersteine"),(r"Zaubergem","Zauberstein"),(r"Zauber-Juwel","Zauberstein")]:out=re.sub(p,r,out)
 if "Trait Material" in en:out=out.replace("Eigenschaftsmaterialien","Merkmalsmaterialien").replace("Eigenschaftsmaterial","Merkmalsmaterial")
 # Reviewed master names: proper names must not be dictionary-translated.
 if Path(getattr(fix,'current_file','')).stem=='masters':
  proper={'Furnace, Brother of Furness':'Furnace, Bruder von Furness','Graft':'Graft','Shun':'Shun','Thesauram':'Thesauram','Birch':'Birch','Lake':'Lake','Jerky':'Jerky','Luv':'Luv','Doctor Feelgood':'Doctor Feelgood','Remane':'Remane','Breeze':'Breeze','Chum':'Chum','Slash':'Slash'}
  if en in proper:out=proper[en]
  master_exact={
   "Aspects are one with nature. They exhibit a level of focus that is unmatched by any other creature in Rodia, allowing them to dodge even the most powerful of attacks. Your creatures don't stand a chance!":"Aspekte sind eins mit der Natur. Sie besitzen eine Konzentration, die von keiner anderen Kreatur in Rodia erreicht wird, und können dadurch selbst den mächtigsten Angriffen ausweichen. Deine Kreaturen haben keine Chance!",
   "Banshees have access to empowered versions of different Spell Gems. If you don't manage to seal their gems early on in battle, you'll be sorry!\\n\\nWith that said, it's time to du-du-du-du-du-duel!":"Banshees haben Zugriff auf verstärkte Versionen verschiedener Zaubersteine. Wenn es dir nicht gelingt, ihre Zaubersteine früh im Kampf zu versiegeln, wirst du es bereuen!\\n\\nAlso dann: Zeit für ein Du-du-du-du-du-duell!",
   "Make no mistake: Cockatrices are weird. But isn't everyone a little odd in their own way? Cockatrices like to make other creatures feel welcome no matter who they are. Such inclusion translates into brilliant teamwork in battle as well. Let me show you!":"Täusche dich nicht: Cockatrices sind seltsam. Aber ist nicht jeder auf seine eigene Art ein bisschen merkwürdig? Cockatrices geben anderen Kreaturen unabhängig von ihrer Herkunft das Gefühl, willkommen zu sein. Diese Offenheit führt auch im Kampf zu hervorragender Teamarbeit. Lass es mich dir zeigen!",
   "Paragons are interesting creatures in the sense that they affect all the creatures on the battlefield - friend and foe alike. It takes some serious strategy to utilize their full potential, but hey, that's the kind of guy I am so it all works out. Your creatures don't stand a chance against the likes of me!":"Paragons sind interessante Kreaturen, denn sie beeinflussen alle Kreaturen auf dem Schlachtfeld – Freund und Feind gleichermaßen. Es braucht einiges an Strategie, um ihr volles Potenzial auszuschöpfen, aber hey, genau dafür bin ich der Richtige. Deine Kreaturen haben gegen mich keine Chance!",
   "Ophans are proficient Life-based spellcasters that specialize in restorative magic. They look really damn cool, too.\\n\\nOrphans, you say? No, not orphans - Ophans! I will punish you for your stupidity!":"Ophans sind versierte Zauberwirker der Lebensklasse, die sich auf heilende Magie spezialisiert haben. Außerdem sehen sie verdammt cool aus.\\n\\nWaisen, sagst du? Nein, nicht Waisen – Ophans! Für diese Dummheit werde ich dich bestrafen!",
   "Brownies might not seem very dangerous on their own, but get enough of them together and you'll be in for a nasty surprise! Let's have a quick duel so I can show you!":"Brownies mögen allein nicht besonders gefährlich wirken, aber wenn genug von ihnen zusammenkommen, erwartet dich eine böse Überraschung! Lass uns ein kurzes Duell austragen, dann zeige ich es dir!",
  }
  if en in master_exact:out=master_exact[en]
  out=out.replace("Eure Kreaturen","Deine Kreaturen").replace("eure Kreaturen","deine Kreaturen")
 # Previous reviewed fixes.
 if en.startswith("The most ambitious project was directed by Zonte's master"):out=out.replace("Der ehrgeizigste Projekt","Das ehrgeizigste Projekt")
 perk_exact={"Your creatures' attacks cannot be dodged.":"Den Angriffen deiner Kreaturen kann nicht ausgewichen werden.","Your creatures' stat changes persist through death.":"Attributsänderungen deiner Kreaturen bleiben auch nach dem Tod bestehen.","Your creatures' stats are no longer reset after they're killed.":"Die Attribute deiner Kreaturen werden nach ihrem Tod nicht mehr zurückgesetzt.","At the start of battle, your Animatus gains a copy of your fifth creature's innate trait.":"Zu Beginn des Kampfes erhält dein Animatus eine Kopie des angeborenen Merkmals deiner fünften Kreatur.","At the start of battle, your {RACE_Godspawn} creatures gain their respective {RACE_Avatar}'s trait.":"Zu Beginn des Kampfes erhalten deine {RACE_Godspawn}-Kreaturen das Merkmal ihres jeweiligen {RACE_Avatar}s.","The first 3 times your creatures are resurrected, they gain a random trait that belongs to their race.":"Die ersten 3 Male, wenn deine Kreaturen wiederbelebt werden, erhalten sie ein zufälliges Merkmal ihrer Rasse.","You have a 100% increased chance to find Skins. This perk is always active, even if your specialization is not {SPEC_DEPRIVED}.":"Du hast eine um 100% erhöhte Chance, Skins zu finden. Dieser Vorteil ist immer aktiv, auch wenn deine Spezialisierung nicht {SPEC_DEPRIVED} ist.","Your creatures' [slot_trick] Trick Slots that apply buffs and debuffs affect 1 additional creature.":"Die [slot_trick]-Trick-Slots deiner Kreaturen, die Buffs und Debuffs anwenden, betreffen 1 zusätzliche Kreatur.","After your creatures manually {ACTION_cast} an {SPELL_equipment}, they {ACTION_cast} a Living Lance spell. The type of Living Lance spell is based on the caster's class.":"Nachdem deine Kreaturen manuell ein {SPELL_equipment} {ACTION_cast}, {ACTION_cast} sie einen Zauber der Lebenden Lanze. Die Art des Zaubers der Lebenden Lanze richtet sich nach der Klasse des Zauberwirkers.","After start-of-battle effects are determined, your creatures' [temporary] Ethereal {SPELL_alcohol}s gain the 'Chance to Attack', 'Chance to Defend', and 'Chance to Provoke' properties.":"Nachdem die Effekte zu Kampfbeginn bestimmt wurden, erhalten die [temporary] Ätherischen {SPELL_alcohol}s deiner Kreaturen die Eigenschaften 'Chance auf Angriff', 'Chance auf Verteidigung' und 'Chance auf Provokation'.","After your creatures are killed, one of your other creatures casts the top-most [icons,1980]Dark Crystal Spell Gem they have equipped.":"Nachdem eine deiner Kreaturen getötet wurde, wirkt eine deiner anderen Kreaturen den obersten ausgerüsteten [icons,1980]Dunkler-Kristall-Zauberstein."}
 if en in perk_exact:out=perk_exact[en]
 if Path(getattr(fix,'current_file','')).stem=='perks':
  out=out.replace("Eure Kreaturen","Deine Kreaturen").replace("eure Kreaturen","deine Kreaturen").replace("Kräutling","Herbling").replace("Statusänderungen","Attributsänderungen").replace("statussteigernden","attributssteigernden").replace("Kreaturen'","Kreaturen").replace("Trickkarten","Trick-Slots").replace("Zauberflickerei","Zauberheilung")
  if "{SPELL_ultimate}" in en or re.search(r'\b(?:Spell )?Gems?\b',en):out=out.replace("Edelsteine","Zaubersteine").replace("Edelstein(e)","Zauberstein(e)").replace("Edelstein","Zauberstein")
 # Retain repaired lore texts already applied in source files; no further changes needed here.
 return out

def narrative_file(path):return Path(path).stem in {"personality","dialog","dialog_story","lore"}
def exception(path,en,term):
 stem=Path(path).stem
 if narrative_file(path) and term in("Creature","Creatures"):return True
 if stem=="personality" and term in("Trait","Traits") and en=="(It seems to be excessively confident in itself. Always a good trait to have in a creature.)":return True
 if stem=="lore" and term in("Trait","Traits") and "Trait Material" not in en:return True
 return False
def false_token(en):return en.startswith("A random enemy recovers a large amount of {STAT_health}")
def main():
 ap=argparse.ArgumentParser();ap.add_argument("csv_file");ap.add_argument("--out",required=True);ap.add_argument("--chunk-size",type=int,default=100);ap.add_argument("--apply-safe-fixes",action="store_true");ap.add_argument("--fixed-file");a=ap.parse_args();o=Path(a.out);o.mkdir(parents=True,exist_ok=True);fix.current_file=a.csv_file
 with open(a.csv_file,encoding="utf-8-sig",newline="")as f:rd=csv.DictReader(f);fs=rd.fieldnames or[];ec,dc=cols(fs);rows=list(rd)
 if a.apply_safe_fixes:
  for r in rows:r[dc]=fix(r.get(ec,""),r.get(dc,""))
  with Path(a.fixed_file or a.csv_file).open("w",encoding="utf-8",newline="")as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 found=[]
 for i,r in enumerate(rows,2):
  en,de=norm(r.get(ec)),norm(r.get(dc));issues=[]
  if en and not de:issues.append("MISSING_TRANSLATION")
  if toks(en)!=toks(de) and not false_token(en):issues.append("TOKEN_MISMATCH")
  for term,want in TERMS.items():
   if term in("Trait","Traits")and re.search(r"\bpropert(?:y|ies)\b",en,re.I):continue
   if exception(a.csv_file,en,term):continue
   if re.search(r"\b"+re.escape(term)+r"\b",en,re.I)and want.lower()not in de.lower():issues.append(f"TERM:{term}->{want}")
  if issues:found.append((i,en,de,"; ".join(issues)))
 h=["line","english","german","issues","reviewed","replacement"]
 for n,s in enumerate(range(0,len(found),a.chunk_size),1):
  with(o/f"review_{n:03d}.csv").open("w",encoding="utf-8",newline="")as f:w=csv.writer(f);w.writerow(h);[w.writerow([ln,en,de,iss,"",""])for ln,en,de,iss in found[s:s+a.chunk_size]]
 (o/"SUMMARY.md").write_text(f"# Translation QA summary\n\n- Source: `{a.csv_file}`\n- Rows: {len(rows)}\n- Flagged: {len(found)}\n- Chunk size: {a.chunk_size}\n- Review files: {(len(found)+a.chunk_size-1)//a.chunk_size}\n",encoding="utf-8")
if __name__=="__main__":main()
