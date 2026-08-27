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
 for p,r in [(r"Zauberjuwel","Zauberstein"),(r"Zauber-Edelsteine","Zaubersteine"),(r"Zauber-Edelstein","Zauberstein"),(r"Zauberedelsteine","Zaubersteine"),(r"Zauberedelstein","Zauberstein"),(r"Zaubergems","Zaubersteine"),(r"Zaubergem","Zauberstein"),(r"Zauber-Juwel","Zauberstein"),(r"Schergen","Diener"),(r"Handlanger","Diener"),(r"Lakaien","Diener"),(r"Statuswerte","Attribute"),(r"Statuswert","Attribut")]:out=re.sub(p,r,out)
 if re.search(r"\btraits?\b",en,re.I):out=re.sub(r"Eigenschaften","Merkmale",out);out=re.sub(r"Eigenschaft","Merkmal",out)
 # Content consistency decisions.
 if en.startswith('[font_14]"Spell Potency" refers to the strength of a spell'):
  out=out.replace('"Zauberwirksamkeit"','"Zaubermacht"').replace('Wirksamkeit eines Zaubers','Zaubermacht eines Zaubers').replace('Wirksamkeitsstufe','Zaubermachtstufe').replace('Statusänderungen','Attributsänderungen')
 if en.startswith("Creatures have five primary stats:"):out=out.replace("Wirksamkeit von Zaubern","Zaubermacht")
 if en.startswith("Part of the spell's potency is based on the caster's {STAT_speed}"):out=out.replace("Wirksamkeit des Zaubers","Zaubermacht des Zaubers")
 if en.startswith("Part of the spell's potency is based on the caster's {STAT_attack}"):out=out.replace("Wirksamkeit des Zaubers","Zaubermacht des Zaubers")
 if en=="Enemies lose fewer stats from stat-reducing effects.":out="Gegner verlieren durch attributsreduzierende Effekte weniger Attribute."
 if en=="Doubles the potency of these effects.":out="Verdoppelt die Effektstärke dieser Effekte."
 if en=="Your creatures' minions have a 5% lower chance to go away.":out="Die Diener deiner Kreaturen haben eine um 5% geringere Chance zu verschwinden."
 # Preserve repaired damaged Codex pages.
 if en.startswith("Cards are extremely rare items that have a chance to drop from enemy creatures after battle."):
  out='Karten sind extrem seltene Gegenstände, die nach einem Kampf mit einer gewissen Wahrscheinlichkeit von feindlichen Kreaturen fallen gelassen werden. Jede Karte gehört zu einem "Karten-Set". Wenn du genügend Karten eines Karten-Sets sammelst, erhalten deine Kreaturen im Kampf einen passiven Bonus. Für jede einzelne Kreatur in Rodia gibt es eine Karte.\\n\\nDu kannst alle gesammelten Karten sowie die dafür freigeschalteten Boni ansehen, indem du im Hauptmenü die Option [menu_cards] Karten auswählst.\\n\\nDu kannst zwar doppelte Karten sammeln, diese gewähren jedoch nur die zusätzlichen Attributsboni, die sie normalerweise verleihen würden, und tragen nicht zu den Karten-Set-Boni bei.'
 return out
def false_token(en):return en.startswith("A random enemy recovers a large amount of {STAT_health}")
def main():
 ap=argparse.ArgumentParser();ap.add_argument("csv_file");ap.add_argument("--out",required=True);ap.add_argument("--chunk-size",type=int,default=100);ap.add_argument("--apply-safe-fixes",action="store_true");ap.add_argument("--fixed-file");a=ap.parse_args();o=Path(a.out);o.mkdir(parents=True,exist_ok=True)
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
   if re.search(r"\b"+re.escape(term)+r"\b",en,re.I)and want.lower()not in de.lower():issues.append(f"TERM:{term}->{want}")
  if issues:found.append((i,en,de,"; ".join(issues)))
 h=["line","english","german","issues","reviewed","replacement"]
 for n,s in enumerate(range(0,len(found),a.chunk_size),1):
  with(o/f"review_{n:03d}.csv").open("w",encoding="utf-8",newline="")as f:w=csv.writer(f);w.writerow(h);[w.writerow([ln,en,de,iss,"",""])for ln,en,de,iss in found[s:s+a.chunk_size]]
 (o/"SUMMARY.md").write_text(f"# Translation QA summary\n\n- Source: `{a.csv_file}`\n- Rows: {len(rows)}\n- Flagged: {len(found)}\n- Chunk size: {a.chunk_size}\n- Review files: {(len(found)+a.chunk_size-1)//a.chunk_size}\n",encoding="utf-8")
if __name__=="__main__":main()
