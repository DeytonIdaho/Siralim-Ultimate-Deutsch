#!/usr/bin/env python3
"""Siralim Ultimate German translation QA and reviewed trait fix helper."""
from __future__ import annotations
import argparse,csv,re
from collections import Counter
from pathlib import Path
TOKEN_RE=re.compile(r"(?:\{[^{}]+\}|\[[^\[\]]+\]|<[^<>]+>|%\w|\\n)")
DEFAULT_TERMS={"Creature":"Kreatur","Creatures":"Kreaturen","Trait":"Merkmal","Traits":"Merkmale","Minion":"Diener","Spell Gem":"Zauberstein","Spell Gems":"Zaubersteine"}
SAFE=[
(r"\bDieses Wesen\b","Diese Kreatur"),(r"\bdieses Wesen\b","diese Kreatur"),(r"\bDieses Wesens\b","Dieser Kreatur"),(r"\bdas Wesen\b","die Kreatur"),(r"\bdem Wesen\b","der Kreatur"),(r"\bvom Wesen\b","von der Kreatur"),(r"\balle Wesen\b","alle Kreaturen"),(r"\bvon allen Wesen\b","von allen Kreaturen"),(r"\banderen Wesen\b","anderen Kreaturen"),(r"\bdeinen Wesen\b","deinen Kreaturen"),(r"\bdeiner Wesen\b","deiner Kreaturen"),(r"\bdeine Wesen\b","deine Kreaturen"),
(r"\bDiese Merkmal\b","Dieses Merkmal"),(r"\bEigenschaft ist nicht stapelbar\b","Merkmal ist nicht kumulativ"),(r"\bDieser Effekt ist nicht stapelbar\b","Dieses Merkmal ist nicht kumulativ"),
(r"\bangeborenen Eigenschaften\b","angeborenen Merkmale"),(r"\bangeborene Eigenschaften\b","angeborene Merkmale"),(r"\bangeborene Eigenschaft\b","angeborenes Merkmal"),(r"\bExtraeigenschaften\b","zusätzlichen Merkmale"),
(r"\bZauber-Edelsteine\b","Zaubersteine"),(r"\bZauber-Edelstein\b","Zauberstein"),(r"\bZauberedelsteine\b","Zaubersteine"),(r"\bZauberedelstein\b","Zauberstein"),(r"\bHeilungszauber-Edelsteine\b","Heilungszaubersteine"),(r"\bSchwächungszauber-Edelsteine\b","Debuff-Zaubersteine"),
(r"\bin der aktuellen Kampf\b","im aktuellen Kampf")]

def norm(s):return(s or"").strip()
def tokens(s):return Counter(TOKEN_RE.findall(s or""))
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
 for p,r in SAFE:out=re.sub(p,r,out)
 # Apply Eigenschaft -> Merkmal only when the English row is actually about traits.
 # Preserve German Eigenschaft for English 'property/properties'.
 if re.search(r"\btraits?\b",en,re.I) and not re.search(r"\bpropert(?:y|ies)\b",en,re.I):
  out=re.sub(r"\bEigenschaften\b","Merkmale",out);out=re.sub(r"\bEigenschaft\b","Merkmal",out)
 # Explicit mixed rows: properties remain Eigenschaften, only the non-stack sentence is a trait.
 if re.search(r"\bpropert(?:y|ies)\b",en,re.I) and re.search(r"This trait does not stack",en,re.I):
  out=re.sub(r"Dieser Effekt ist nicht stapelbar\.","Dieses Merkmal ist nicht kumulativ.",out)
 # Known token repair.
 if "[icons,1976] Metamorphose" in out and "{ACTION_casts}" not in out:
  out=out.replace("wirkt sie [icons,1976] Metamorphose","{ACTION_casts} sie [icons,1976] Metamorphose")
 # ALL-CAPS joke line: keep tone, normalize only terminology/non-stack wording.
 out=out.replace("DIESE EIGENSCHAFT STAPELT SICH NICHT","DIESES MERKMAL IST NICHT KUMULATIV")
 return out

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
  if tokens(en)!=tokens(de):issues.append("TOKEN_MISMATCH")
  for term,want in DEFAULT_TERMS.items():
   # Properties are deliberately allowed to use Eigenschaft(en).
   if term in ("Trait","Traits") and re.search(r"\bpropert(?:y|ies)\b",en,re.I):continue
   if re.search(r"\b"+re.escape(term)+r"\b",en,re.I) and want.lower() not in de.lower():issues.append(f"TERM:{term}->{want}")
  if issues:found.append((i,en,de,"; ".join(issues)))
 h=["line","english","german","issues","reviewed","replacement"]
 for n,s in enumerate(range(0,len(found),a.chunk_size),1):
  with(o/f"review_{n:03d}.csv").open("w",encoding="utf-8",newline="")as f:w=csv.writer(f);w.writerow(h);[w.writerow([ln,en,de,iss,"",""])for ln,en,de,iss in found[s:s+a.chunk_size]]
 (o/"SUMMARY.md").write_text(f"# Translation QA summary\n\n- Source: `{a.csv_file}`\n- Rows: {len(rows)}\n- Flagged: {len(found)}\n- Chunk size: {a.chunk_size}\n- Review files: {(len(found)+a.chunk_size-1)//a.chunk_size}\n",encoding="utf-8");print(f"Checked {len(rows)} rows; flagged {len(found)}")
if __name__=="__main__":main()
