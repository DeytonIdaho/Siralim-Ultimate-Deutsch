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
 for p,r in [(r"Ätheredelsteine","Ätherische Zaubersteine"),(r"Zauber-Edelsteine","Zaubersteine"),(r"Zauber-Edelstein","Zauberstein"),(r"Zauberedelsteine","Zaubersteine"),(r"Zauberedelstein","Zauberstein"),(r"Zaubergems","Zaubersteine"),(r"Zaubergem","Zauberstein"),(r"Zauber-Juwel","Zauberstein"),(r"Schergen-Schaden","Dienerschaden"),(r"Schergen","Diener"),(r"Statuswerte","Attribute"),(r"Statuswert","Attribut")]:out=re.sub(p,r,out)
 # Trait is Merkmal; property remains Eigenschaft.
 if re.search(r"\btraits?\b",en,re.I):
  out=re.sub(r"Eigenschaftsplätze","Merkmalsplätze",out);out=re.sub(r"Eigenschaftsmaterialien","Merkmalsmaterialien",out);out=re.sub(r"Eigenschaften","Merkmale",out);out=re.sub(r"Eigenschaft","Merkmal",out)
 if en=="Trait Slots":out="Merkmalsplätze"
 if en=="Traits":out="Merkmale"
 if en.startswith("Artifact Materials can be socketed"):out=out.replace("Statusmaterialien","Attributsmaterialien").replace("Statusslots","Attributsplätze")
 if en.startswith("Your creatures' Spell Gems that belong to other classes have 5% more potency."):out=re.sub(r"Wirksamkeit","Zaubermacht",out)
 if en=="A Nemesis Creature appeared nearby!":out="Eine Nemesis-Kreatur ist in der Nähe aufgetaucht!"
 if en.startswith("Your creatures gained +0.1% Minion Damage!"):out="Deine Kreaturen haben +0,1% Dienerschaden erhalten!"
 # Repair damaged Codex macro tutorial in full.
 if en.startswith("Now that you've created a macro, you must assign it to a creature to use it in battle."):
  out='Nachdem du ein Makro erstellt hast, musst du es einer Kreatur zuweisen, um es im Kampf zu verwenden. Öffne das Hauptmenü, wähle "Kreaturen" und anschließend die Kreatur, der du ein Makro zuweisen möchtest. Wähle dann "Makro zuweisen" und das gewünschte Makro.\\n\\nWenn diese Kreatur im Kampf den Befehl "Makro" auswählt, wertet sie alle Zeilen des Makros aus und versucht zu bestimmen, was sie tun soll.\\n\\nStell dir vor, das auf der vorherigen Seite erwähnte Makro wurde einer deiner Kreaturen zugewiesen. Wenn die Gesundheit eines ihrer Verbündeten unter 20% fällt und du anschließend den Befehl "Makro" verwendest, wirkt sie den Zauber "Heilung" auf diesen Verbündeten, sofern sie den Zauber ausgerüstet hat.'
 # Cards grammar cleanup.
 if en.startswith("Your creatures' [temporary] Ethereal Spell Gems grant 10% more healing."):out="Die [temporary] Ätherischen Zaubersteine deiner Kreaturen gewähren 10% mehr Heilung."
 if en.startswith("Your creatures' [temporary] Ethereal Spell Gems grant 10% more stats."):out="Die [temporary] Ätherischen Zaubersteine deiner Kreaturen gewähren 10% mehr Attribute."
 # Existing reviewed fixes.
 if re.search(r"(?:debuff|CONDNAME_DEBUFF).{0,100}(?:potency|potent)|(?:potency|potent).{0,100}(?:debuff|CONDNAME_DEBUFF)",en,re.I):out=re.sub(r"Wirksamkeit","Effektstärke",out)
 if "The potency is based on the caster's {STAT_defense} instead of {STAT_intelligence}" in en:out=re.sub(r"Wirksamkeit","Zaubermacht",out)
 if en=="Diabolic Henchman":out="Teuflischer Diener"
 if en.startswith("Target's next attack deals 100% more damage. This effect does not stack."):out="Der nächste Angriff des Ziels verursacht 100% mehr Schaden. Dieser Effekt ist nicht kumulativ."
 if en=="Death Creature Core":out="Todeskreatur-Kern"
 elif en=="Nature Creature Core":out="Naturkreatur-Kern"
 elif en=="Sorcery Creature Core":out="Zauberkreatur-Kern"
 elif en=="Orphaned Minion":out="Verwaister Diener"
 if en=="Balance In All Things":out="Gleichgewicht in allen Dingen"
 return out
def exception(en,term=None):
 if "mermaid-like creature" in en and term=="Creature":return True
 if en.startswith("Each of the caster's other, permanent Spell Gems") and term=="Spell Gems":return True
 return False
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
   if exception(en,term):continue
   if re.search(r"\b"+re.escape(term)+r"\b",en,re.I)and want.lower()not in de.lower():issues.append(f"TERM:{term}->{want}")
  if issues:found.append((i,en,de,"; ".join(issues)))
 h=["line","english","german","issues","reviewed","replacement"]
 for n,s in enumerate(range(0,len(found),a.chunk_size),1):
  with(o/f"review_{n:03d}.csv").open("w",encoding="utf-8",newline="")as f:w=csv.writer(f);w.writerow(h);[w.writerow([ln,en,de,iss,"",""])for ln,en,de,iss in found[s:s+a.chunk_size]]
 (o/"SUMMARY.md").write_text(f"# Translation QA summary\n\n- Source: `{a.csv_file}`\n- Rows: {len(rows)}\n- Flagged: {len(found)}\n- Chunk size: {a.chunk_size}\n- Review files: {(len(found)+a.chunk_size-1)//a.chunk_size}\n",encoding="utf-8")
if __name__=="__main__":main()
