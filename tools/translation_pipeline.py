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
 if "Trait Material" in en:out=out.replace("Eigenschaftsmaterial","Merkmalsmaterial")
 if en.startswith("Everett:\\nWhen you Fuse two creatures together"):out=out.replace("Eigenschaften beider","Merkmale beider").replace("seine Werte","seine Attribute").replace("Durchschnitt der Werte","Durchschnitt der Attribute")
 if en.startswith("This creature has already used 15 scrolls."):out=out.replace("Dieses Wesen","Diese Kreatur")
 if en.startswith("You can now Transmogrify your character"):out=out.replace("jedes Wesen der","jede Kreatur der")
 if en.startswith("You should bring along at least one creature before using the Teleportation Shrine."):out="Du solltest mindestens eine Kreatur mitnehmen, bevor du den Teleportationsschrein benutzt."
 if en.startswith("Nortah:\\nYou can return to the Menagerie"):out=out.replace("ein Wesen aus deiner Gruppe","eine Kreatur aus deiner Gruppe")
 if en=="Spell Gems":out="Zaubersteine"
 if en=="Abnormal Spell Gems":out="Abnormale Zaubersteine"
 if en=="Customizable Creature":out="Anpassbare Kreatur"
 if en in("Scylla","Charybdis") and not out:out=en
 # Personality: here 'trait' is ordinary prose, not the game mechanic.
 if en=="(It seems to be excessively confident in itself. Always a good trait to have in a creature.)":out="(Es scheint übermäßig selbstsicher zu sein. Immer eine gute Eigenschaft für ein Wesen.)"
 if en=="NEW HOBBY. WANT TO EAT YOUR SPELL GEMS NOW.":out="NEUES HOBBY. WILL JETZT DEINE ZAUBERSTEINE FRESSEN."
 return out

def narrative_file(path):return Path(path).stem in {"personality","dialog","dialog_story"}
def exception(path,en,term):
 if narrative_file(path) and term in("Creature","Creatures"):
  mechanical=(en.startswith("This creature has already used 15 scrolls.") or en.startswith("You can now Transmogrify your character") or en.startswith("You should bring along at least one creature before using the Teleportation Shrine.") or en.startswith("Nortah:\\nYou can return to the Menagerie"))
  return not mechanical
 # Narrative English 'trait' can mean ordinary characteristic rather than Trait mechanic.
 if Path(path).stem=="personality" and term in("Trait","Traits") and en=="(It seems to be excessively confident in itself. Always a good trait to have in a creature.)":return True
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
   if exception(a.csv_file,en,term):continue
   if re.search(r"\b"+re.escape(term)+r"\b",en,re.I)and want.lower()not in de.lower():issues.append(f"TERM:{term}->{want}")
  if issues:found.append((i,en,de,"; ".join(issues)))
 h=["line","english","german","issues","reviewed","replacement"]
 for n,s in enumerate(range(0,len(found),a.chunk_size),1):
  with(o/f"review_{n:03d}.csv").open("w",encoding="utf-8",newline="")as f:w=csv.writer(f);w.writerow(h);[w.writerow([ln,en,de,iss,"",""])for ln,en,de,iss in found[s:s+a.chunk_size]]
 (o/"SUMMARY.md").write_text(f"# Translation QA summary\n\n- Source: `{a.csv_file}`\n- Rows: {len(rows)}\n- Flagged: {len(found)}\n- Chunk size: {a.chunk_size}\n- Review files: {(len(found)+a.chunk_size-1)//a.chunk_size}\n",encoding="utf-8")
if __name__=="__main__":main()
