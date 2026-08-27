#!/usr/bin/env python3
"""Siralim Ultimate German translation QA and reviewed trait fixes."""
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
 for p,r in [(r"\bDeine Wesen\b","Deine Kreaturen"),(r"\bdeine Wesen\b","deine Kreaturen"),(r"\btote Wesen\b","tote Kreatur"),(r"\blebende Wesen\b","lebende Kreatur"),(r"\bandere Wesen\b","andere Kreatur"),(r"\bjedes Wesen\b","jede Kreatur"),(r"\bfür jedes Wesen\b","für jede Kreatur"),(r"\bSchwächungseffekte\b","Debuffs"),(r"\bSchwächungseffekt\b","Debuff"),(r"\bdieser Merkmal\b","dieses Merkmal"),(r"\bDieser Merkmal\b","Dieses Merkmal"),(r"\bnicht stapelbar\b","nicht kumulativ"),(r"\bStatuswert\b","Attribut")]:out=re.sub(p,r,out)
 if re.search(r"\btraits?\b",en,re.I) and not re.search(r"\bpropert(?:y|ies)\b",en,re.I):out=re.sub(r"\bEigenschaften\b","Merkmale",out);out=re.sub(r"\bEigenschaft\b","Merkmal",out)
 # Explicit final potency decisions.
 spell_potency_prefixes=("If this creature has {ACTION_provoked}","Your {RACE_Djinn}s' spells","When this creature {ACTION_casts} a spell, the spell has","While this creature is at the bottom of the {TIMELINE}","[icons,1976]Toxic Frogmania","If your creatures have collectively {ACTION_cast}")
 if en=="Potency":out="Zaubermacht"
 elif en.startswith(spell_potency_prefixes):out=re.sub(r"\bWirksamkeit\b","Zaubermacht",out)
 elif en.startswith("The potency of your creatures' non-damaging spells"):out=re.sub(r"\bWirksamkeit\b","Zaubermacht",out)
 elif en.startswith("Your creatures deal additional damage with attacks and spells equal to 50% of the potency of their {CONDNAME_BUFF_BARRIER}"):out=re.sub(r"\bWirksamkeit\b","Effektstärke",out)
 elif en.startswith("After this creature {ACTION_casts} a spell, it increases the potency of enemies'"):out=re.sub(r"\bWirksamkeit\b","Effektstärke",out)
 # Previously reviewed semantic fixes.
 if en.strip()=="Enemies always have {CONDNAME_DEBUFF_SCORN}. This debuff switches back and forth with {CONDNAME_DEBUFF_SILENCE} at the start of this creature's turn.":out="Feinde haben immer {CONDNAME_DEBUFF_SCORN}. Dieser Debuff wechselt zu Beginn des Zuges dieser Kreatur zwischen {CONDNAME_DEBUFF_SCORN} und {CONDNAME_DEBUFF_SILENCE}."
 elif en.startswith("Enemies always have {CONDNAME_DEBUFF_SCORN}.") and "Enemies can only" in en:out="Feinde haben immer {CONDNAME_DEBUFF_SCORN}. Dieser Debuff wechselt zu Beginn des Zuges dieser Kreatur zwischen {CONDNAME_DEBUFF_SCORN} und {CONDNAME_DEBUFF_SILENCE}. Feinde können pro Zug nur 1 Mal {ACTION_attack} und nur 1 Mal einen Zauber {ACTION_cast}."
 if en.startswith("Your creatures' Ultimate Spell Gems cannot be Sealed"):out="Die ultimativen Zaubersteine deiner Kreaturen können nicht versiegelt werden und verbrauchen keine {STAT_charges}. Deine Kreaturen sind immun gegen {CONDNAME_DEBUFF_SILENCE}."
 if en.startswith("At the start of this creature's turn, it kills the creature with the highest {STAT_speed}"):out="Zu Beginn des Zuges dieser Kreatur tötet sie in normalen Kämpfen die Kreatur mit dem höchsten {STAT_speed}. In Bosskämpfen {ACTION_attacks} diese Kreatur sie stattdessen. Dieses Merkmal kann nur einmal pro Kampf aktiviert werden."
 return out

def exception(en,term=None):
 return ((en.startswith("When this creature {ACTION_attacks}, it has a 100% chance") and term=="Trait") or(en.startswith("After this creature gains a stat, it gains 200%") and term=="Trait")or(en.startswith("At the start of this creature's turn, it Seals one of each creature's Spell Gems") and term=="Spell Gems")or(en.startswith("If this creature's Relic's corresponding {RACE_Avatar}") and term=="Creature"))
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
  false_token=(en.startswith("AT THE END OF YOUR CREATURES' TURNS, THEY'LL SAY") or en.startswith("While this creature is at 100% {STAT_health}") or en.strip()=="Enemies always have {CONDNAME_DEBUFF_SCORN}. This debuff switches back and forth with {CONDNAME_DEBUFF_SILENCE} at the start of this creature's turn." or(en.startswith("Enemies always have {CONDNAME_DEBUFF_SCORN}") and "Enemies can only" in en))
  if toks(en)!=toks(de) and not false_token:issues.append("TOKEN_MISMATCH")
  for term,want in TERMS.items():
   if term in("Trait","Traits") and re.search(r"\bpropert(?:y|ies)\b",en,re.I):continue
   if term=="Creatures" and en.startswith("This creatures starts battles"):continue
   if exception(en,term):continue
   if re.search(r"\b"+re.escape(term)+r"\b",en,re.I) and want.lower() not in de.lower():issues.append(f"TERM:{term}->{want}")
  if issues:found.append((i,en,de,"; ".join(issues)))
 h=["line","english","german","issues","reviewed","replacement"]
 for n,s in enumerate(range(0,len(found),a.chunk_size),1):
  with(o/f"review_{n:03d}.csv").open("w",encoding="utf-8",newline="")as f:w=csv.writer(f);w.writerow(h);[w.writerow([ln,en,de,iss,"",""])for ln,en,de,iss in found[s:s+a.chunk_size]]
 (o/"SUMMARY.md").write_text(f"# Translation QA summary\n\n- Source: `{a.csv_file}`\n- Rows: {len(rows)}\n- Flagged: {len(found)}\n- Chunk size: {a.chunk_size}\n- Review files: {(len(found)+a.chunk_size-1)//a.chunk_size}\n",encoding="utf-8");print(f"Checked {len(rows)} rows; flagged {len(found)}")
if __name__=="__main__":main()
