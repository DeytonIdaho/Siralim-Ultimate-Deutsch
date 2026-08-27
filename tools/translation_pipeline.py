#!/usr/bin/env python3
"""Siralim Ultimate German translation QA and reviewed fixes."""
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
 for p,r in [(r"Zauber-Edelsteine","Zaubersteine"),(r"Zauber-Edelstein","Zauberstein"),(r"Zauberedelsteine","Zaubersteine"),(r"Zauberedelstein","Zauberstein"),(r"Zaubergems","Zaubersteine"),(r"Zaubergem","Zauberstein"),(r"Zauber-Juwel","Zauberstein"),(r"Schergenmeister","Dienermeister"),(r"Schergen","Diener"),(r"Lakaien","Diener"),(r"Lakai","Diener"),(r"Schwächungseffekt","Debuff"),(r"Statuswerte","Attribute"),(r"Statuswert","Attribut")]:out=re.sub(p,r,out)
 if re.search(r"\btraits?\b",en,re.I) and not re.search(r"\bpropert(?:y|ies)\b",en,re.I):out=re.sub(r"Eigenschaften","Merkmale",out);out=re.sub(r"Eigenschaft","Merkmal",out)
 # Game-creature terminology, but preserve ordinary narrative creature wording.
 if re.search(r"\bcreatures?\b",en,re.I) and not re.search(r"mermaid-like creature",en,re.I):
  out=re.sub(r"\bWesen\b","Kreatur",out);out=re.sub(r"\bWesens\b","Kreatur",out)
 # Spell potency means Zaubermacht.
 if re.search(r"spell(?:'s|s')?.{0,50}potency|potency.{0,50}spell",en,re.I):out=re.sub(r"Wirksamkeit","Zaubermacht",out)
 # Reviewed item fixes.
 if en=="Death Creature Core":out="Todeskreatur-Kern"
 elif en=="Nature Creature Core":out="Naturkreatur-Kern"
 elif en=="Sorcery Creature Core":out="Zauberkreatur-Kern"
 elif en=="Orphaned Minion":out="Verwaister Diener"
 # Reviewed spell semantic/token fixes.
 if en.startswith("Your creatures' Spell Gems are unsealed. This Spell Gem cannot be Sealed."):out="Die Zaubersteine deiner Kreaturen werden entsiegelt. Dieser Zauberstein kann nicht versiegelt werden."
 if en.startswith("Your creatures' Spell Gems are unsealed and their {CONDNAME_DEBUFF_SILENCE}"):out="Die Zaubersteine deiner Kreaturen werden entsiegelt und ihre {CONDNAME_DEBUFF_SILENCE}-Debuffs werden entfernt. Dieser Zauber ist ein {SPELL_equipment}."
 if en.startswith("One of the caster's [temporary] Ethereal Spell Gems is Sealed."):out=out.replace("[temporären]","[temporary]")
 if en=="Balance In All Things":out="Gleichgewicht in allen Dingen"
 if en.startswith("Enemies' minions are removed. Enemies are afflicted with a random debuff"):out="Die Diener der Feinde werden entfernt. Feinde werden für jeden entfernten Diener mit einem zufälligen Debuff belegt."
 # False token mismatches: source begins with formatting newlines that German may omit.
 return out

def exception(en,term=None):
 if "mermaid-like creature" in en and term=="Creature":return True
 return False
def false_token(en):return (en.startswith("\\n\\nYou need 5 of these materials")or en.startswith("\\n\\nYou need 3 of these materials")or en=="Balance In All Things"or en.startswith("AT THE END OF YOUR CREATURES' TURNS, THEY'LL SAY")or en.startswith("Your creatures' {CONDNAME_BUFF_SAVAGE} buff now causes")or en.startswith("Your creatures have a 1% chance (up to 35%) to avoid debuffs"))
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
   if term in("Trait","Traits") and re.search(r"\bpropert(?:y|ies)\b",en,re.I):continue
   if exception(en,term):continue
   if re.search(r"\b"+re.escape(term)+r"\b",en,re.I) and want.lower() not in de.lower():issues.append(f"TERM:{term}->{want}")
  if issues:found.append((i,en,de,"; ".join(issues)))
 h=["line","english","german","issues","reviewed","replacement"]
 for n,s in enumerate(range(0,len(found),a.chunk_size),1):
  with(o/f"review_{n:03d}.csv").open("w",encoding="utf-8",newline="")as f:w=csv.writer(f);w.writerow(h);[w.writerow([ln,en,de,iss,"",""])for ln,en,de,iss in found[s:s+a.chunk_size]]
 (o/"SUMMARY.md").write_text(f"# Translation QA summary\n\n- Source: `{a.csv_file}`\n- Rows: {len(rows)}\n- Flagged: {len(found)}\n- Chunk size: {a.chunk_size}\n- Review files: {(len(found)+a.chunk_size-1)//a.chunk_size}\n",encoding="utf-8");print(f"Checked {len(rows)} rows; flagged {len(found)}")
if __name__=="__main__":main()
