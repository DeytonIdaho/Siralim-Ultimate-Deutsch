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
 for p,r in [(r"\bZauber-Edelsteine\b","Zaubersteine"),(r"\bZauber-Edelstein\b","Zauberstein"),(r"\bZauberedelsteine\b","Zaubersteine"),(r"\bZauberedelstein\b","Zauberstein"),(r"\bZaubergems\b","Zaubersteine"),(r"\bZaubergem\b","Zauberstein"),(r"\bZauber-Juwel\b","Zauberstein"),(r"\bRunenzauber-Edelsteine\b","Runenzaubersteine"),(r"\bStatuswerte\b","Attribute"),(r"\bStatuswert\b","Attribut"),(r"\bSchwächungszaubers\b","Debuffs"),(r"\bSchwächungszauber\b","Debuff"),(r"\bSchergen\b","Diener"),(r"\bLakaien\b","Diener"),(r"\bLakai\b","Diener"),(r"\bDieser Effekt stapelt sich mehrmals hintereinander\b","Dieser Effekt ist mehrfach hintereinander kumulativ")]:out=re.sub(p,r,out)
 if re.search(r"\btraits?\b",en,re.I) and not re.search(r"\bpropert(?:y|ies)\b",en,re.I):out=re.sub(r"\bEigenschaften\b","Merkmale",out);out=re.sub(r"\bEigenschaft\b","Merkmal",out)
 # Potency classification: spells/gems => Zaubermacht; debuffs/effects => Effektstärke.
 if re.search(r"\b(?:potency|potent)\b",en,re.I):
  spell=bool(re.search(r"(?:spells?|Gems?|Rune spells?|Relics' spells|\{SPELL_equipment\}s).{0,60}(?:potency|potent)|(?:potency|potent).{0,60}(?:spells?|Gems?|Rune spells?|Relics' spells|\{SPELL_equipment\}s)",en,re.I))
  effect=bool(re.search(r"(?:debuff|effects?|CONDNAME_DEBUFF).{0,80}(?:potency|potent)|(?:potency|potent).{0,80}(?:debuff|effects?|CONDNAME_DEBUFF)",en,re.I))
  if spell and not effect:out=re.sub(r"\bWirksamkeit\b","Zaubermacht",out)
  elif effect and not spell:out=re.sub(r"\bWirksamkeit\b","Effektstärke",out)
 # Explicit ambiguous cases reviewed from perk consistency scan.
 if en.startswith("Increases the potency of your creatures' effects that increase their stats"):out=re.sub(r"\bWirksamkeit\b","Effektstärke",out)
 if en.startswith("Increases the potency of your creatures' effects that decrease enemies' stats"):out=re.sub(r"\bWirksamkeit\b","Effektstärke",out)
 if en.startswith("Decreases the potency of enemies' effects that increase their stats"):out=re.sub(r"\bWirksamkeit\b","Effektstärke",out)
 if en.startswith("50% of the potency of your creatures' {SPELL_equipment}s"):out=re.sub(r"\bWirksamkeit\b","Zaubermacht",out)
 if en.startswith("Your creatures' Relics' spells have"):out=re.sub(r"\bWirksamkeit\b","Zaubermacht",out)
 # Previously reviewed semantic fixes.
 if en.startswith("Your creatures with {CONDNAME_BUFF_ARCANE} cannot have their Spell Gems sealed"):out="Die Zaubersteine deiner Kreaturen mit {CONDNAME_BUFF_ARCANE} können nicht versiegelt werden. Zusätzlich erhalten deine Kreaturen mit {CONDNAME_BUFF_SHELL}, nachdem sie Ziel eines gegnerischen Zaubers wurden, eine Kopie dieses Zaubersteins."
 if en.strip()=="You can have <1>  additional {RACE_Avatar} creature(s) in your party.":out="Du kannst <1> zusätzliche {RACE_Avatar}-Kreatur(en) in deiner Gruppe haben."
 return out

def exception(en,term=None):return ((en.startswith("When this creature {ACTION_attacks}, it has a 100% chance")and term=="Trait")or(en.startswith("After this creature gains a stat, it gains 200%")and term=="Trait")or(en.startswith("At the start of this creature's turn, it Seals one of each creature's Spell Gems")and term=="Spell Gems")or(en.startswith("If this creature's Relic's corresponding {RACE_Avatar}")and term=="Creature"))
def false_token(en):return (en.startswith("AT THE END OF YOUR CREATURES' TURNS, THEY'LL SAY")or en.startswith("While this creature is at 100% {STAT_health}")or en.startswith("Your creatures' {CONDNAME_BUFF_SAVAGE} buff now causes")or en.startswith("Your creatures have a 1% chance (up to 35%) to avoid debuffs")or en.strip()=="Enemies always have {CONDNAME_DEBUFF_SCORN}. This debuff switches back and forth with {CONDNAME_DEBUFF_SILENCE} at the start of this creature's turn."or(en.startswith("Enemies always have {CONDNAME_DEBUFF_SCORN}")and"Enemies can only"in en))
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
   if term=="Creatures"and en.startswith("This creatures starts battles"):continue
   if exception(en,term):continue
   if re.search(r"\b"+re.escape(term)+r"\b",en,re.I)and want.lower()not in de.lower():issues.append(f"TERM:{term}->{want}")
  if issues:found.append((i,en,de,"; ".join(issues)))
 h=["line","english","german","issues","reviewed","replacement"]
 for n,s in enumerate(range(0,len(found),a.chunk_size),1):
  with(o/f"review_{n:03d}.csv").open("w",encoding="utf-8",newline="")as f:w=csv.writer(f);w.writerow(h);[w.writerow([ln,en,de,iss,"",""])for ln,en,de,iss in found[s:s+a.chunk_size]]
 (o/"SUMMARY.md").write_text(f"# Translation QA summary\n\n- Source: `{a.csv_file}`\n- Rows: {len(rows)}\n- Flagged: {len(found)}\n- Chunk size: {a.chunk_size}\n- Review files: {(len(found)+a.chunk_size-1)//a.chunk_size}\n",encoding="utf-8");print(f"Checked {len(rows)} rows; flagged {len(found)}")
if __name__=="__main__":main()
