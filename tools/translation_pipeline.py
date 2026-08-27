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
 out=de or"";stem=Path(getattr(fix,'current_file','')).stem
 for p,r in [(r"Zauberjuwel","Zauberstein"),(r"Zauber-Edelsteine","Zaubersteine"),(r"Zauber-Edelstein","Zauberstein"),(r"Zauberedelsteine","Zaubersteine"),(r"Zauberedelstein","Zauberstein"),(r"Zaubergems","Zaubersteine"),(r"Zaubergem","Zauberstein"),(r"Zauber-Juwel","Zauberstein")]:out=re.sub(p,r,out)
 if "Trait Material" in en:out=out.replace("Eigenschaftsmaterialien","Merkmalsmaterialien").replace("Eigenschaftsmaterial","Merkmalsmaterial").replace("Eigenschaftsmaterie","Merkmalsmaterial")
 if stem in {'ui','vocabulary'}:
  # Mechanical UI terminology is strict.
  if re.search(r'\bTraits?\b',en):out=out.replace('Eigenschaft(en)','Merkmal(e)').replace('Eigenschaftsgewinne','Merkmalsgewinne').replace('Eigenschaftsdetails','Merkmalsdetails').replace('Eigenschaftsplatz','Merkmalsplatz').replace('Eigenschaften','Merkmale').replace('Eigenschaft','Merkmal')
  if re.search(r'\bSpell Gems?\b',en):out=out.replace('Zauberstein-Platz/Plätze','Zaubersteinplatz/-plätze').replace('Edelsteine','Zaubersteine').replace('Edelstein','Zauberstein')
  out=out.replace('keinen Attentatsmission','keine Attentatsmission')
  if en.startswith('Cards are extremely rare items that have a chance to drop from enemy creatures after battle.'):
   out='Karten sind extrem seltene Gegenstände, die nach einem Kampf mit einer gewissen Wahrscheinlichkeit von feindlichen Kreaturen fallen gelassen werden. Jede Karte gehört zu einem "Karten-Set". Sobald du genügend Karten eines Sets gesammelt hast, erhalten deine Kreaturen im Kampf einen passiven Bonus. Für jede einzelne Kreatur in Rodia gibt es eine Karte.\\n\\nAlle gesammelten Karten und die dadurch freigeschalteten Boni kannst du über die Option [menu_cards] Karten im Hauptmenü ansehen.'
 # Previous master corrections retained.
 if stem=='masters':
  proper={'Furnace, Brother of Furness':'Furnace, Bruder von Furness','Graft':'Graft','Shun':'Shun','Thesauram':'Thesauram','Birch':'Birch','Lake':'Lake','Jerky':'Jerky','Luv':'Luv','Doctor Feelgood':'Doctor Feelgood','Remane':'Remane','Breeze':'Breeze','Chum':'Chum','Slash':'Slash'}
  if en in proper:out=proper[en]
  out=out.replace("Eure Kreaturen","Deine Kreaturen").replace("eure Kreaturen","deine Kreaturen")
 if stem=='perks':
  out=out.replace("Eure Kreaturen","Deine Kreaturen").replace("eure Kreaturen","deine Kreaturen").replace("Kräutling","Herbling").replace("Statusänderungen","Attributsänderungen").replace("statussteigernden","attributssteigernden").replace("Kreaturen'","Kreaturen").replace("Trickkarten","Trick-Slots").replace("Zauberflickerei","Zauberheilung")
  if "{SPELL_ultimate}" in en or re.search(r'\b(?:Spell )?Gems?\b',en):out=out.replace("Edelsteine","Zaubersteine").replace("Edelstein(e)","Zauberstein(e)").replace("Edelstein","Zauberstein")
 return out

def narrative_file(path):return Path(path).stem in {"personality","dialog","dialog_story","lore","bosses"}
def exception(path,en,term):
 stem=Path(path).stem
 if narrative_file(path) and term in("Creature","Creatures"):return True
 if stem=="personality" and term in("Trait","Traits") and en=="(It seems to be excessively confident in itself. Always a good trait to have in a creature.)":return True
 if stem=="lore" and term in("Trait","Traits") and "Trait Material" not in en:return True
 return False
def false_token(en):
 return en.startswith("A random enemy recovers a large amount of {STAT_health}") or en.startswith('{CONDNAME_DEBUFF_CONFUSED} creatures have a 50% chance')
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
