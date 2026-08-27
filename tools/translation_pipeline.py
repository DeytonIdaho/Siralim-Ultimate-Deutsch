#!/usr/bin/env python3
"""Siralim Ultimate German translation QA and safe-fix helper."""
from __future__ import annotations
import argparse, csv, re
from collections import Counter
from pathlib import Path

TOKEN_RE = re.compile(r"(?:\{[^{}]+\}|\[[^\[\]]+\]|<[^<>]+>|%\w|\\n)")
DEFAULT_TERMS = {
    "Attack": "Angriff", "Defense": "Verteidigung", "Speed": "Geschwindigkeit",
    "Intelligence": "Intelligenz", "Damage": "Schaden", "Spell": "Zauber", "Spells": "Zauber",
    "Creature": "Kreatur", "Creatures": "Kreaturen", "Trait": "Merkmal", "Traits": "Merkmale",
    "Minion": "Diener", "Spell Gem": "Zauberstein", "Spell Gems": "Zaubersteine",
}

# Only replacements confirmed as unambiguous during trait review.
SAFE_REPLACEMENTS = [
    (r"\bDieses Wesen\b", "Diese Kreatur"),
    (r"\bdieses Wesen\b", "diese Kreatur"),
    (r"\bEigenschaft ist nicht stapelbar\b", "Merkmal ist nicht kumulativ"),
    (r"\bDiese Eigenschaft\b", "Dieses Merkmal"),
    (r"\bdiese Eigenschaft\b", "dieses Merkmal"),
    (r"\bStatuswerte\b", "Attribute"),
    (r"\bStatuswert\b", "Attribut"),
    (r"\bZauber-Edelsteine\b", "Zaubersteine"),
    (r"\bZauber-Edelstein\b", "Zauberstein"),
    (r"\bZauberedelsteine\b", "Zaubersteine"),
    (r"\bZauberedelstein\b", "Zauberstein"),
    (r"\bZauber-Juwel\b", "Zauberstein"),
    (r"\bHandlanger\b", "Diener"),
    (r"\bSchergen\b", "Diener"),
    (r"\bSchwächungseffekt\b", "Debuff"),
    (r"\bStärkungseffekt\b", "Buff"),
    (r"\baktuellen Schlacht\b", "aktuellen Kampf"),
]

def norm(s): return (s or "").strip()
def tokens(s): return Counter(TOKEN_RE.findall(s or ""))

def detect_columns(fields):
    low = {f.lower(): f for f in fields}
    def pick(names):
        for n in names:
            if n in low: return low[n]
        return None
    src = pick(["english","en","source","original","text_en","description_en"])
    de = pick(["german","de","deutsch","translation","text_de","description_de"])
    if not src or not de: raise SystemExit(f"Could not detect EN/DE columns. Columns: {fields}")
    return src,de

def apply_safe_fixes(text):
    out=text or ""
    for pat,repl in SAFE_REPLACEMENTS: out=re.sub(pat,repl,out)
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("csv_file")
    ap.add_argument("--out", required=True)
    ap.add_argument("--chunk-size", type=int, default=100)
    ap.add_argument("--apply-safe-fixes", action="store_true")
    ap.add_argument("--fixed-file")
    args=ap.parse_args()
    out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    with open(args.csv_file,encoding="utf-8-sig",newline="") as f:
        rd=csv.DictReader(f); fields=rd.fieldnames or []; src_col,de_col=detect_columns(fields); rows=list(rd)
    if args.apply_safe_fixes:
        for r in rows: r[de_col]=apply_safe_fixes(r.get(de_col,""))
        fixed=Path(args.fixed_file or args.csv_file)
        with fixed.open("w",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    findings=[]
    for i,r in enumerate(rows,start=2):
        en,de=norm(r.get(src_col)),norm(r.get(de_col)); issues=[]
        if en and not de: issues.append("MISSING_TRANSLATION")
        if tokens(en)!=tokens(de): issues.append("TOKEN_MISMATCH")
        for term,want in DEFAULT_TERMS.items():
            if re.search(r"\b"+re.escape(term)+r"\b",en,re.I) and want.lower() not in de.lower():
                issues.append(f"TERM:{term}->{want}")
        if issues: findings.append((i,en,de,"; ".join(issues)))
    headers=["line","english","german","issues","reviewed","replacement"]
    for n,start in enumerate(range(0,len(findings),args.chunk_size),1):
        with (out/f"review_{n:03d}.csv").open("w",encoding="utf-8",newline="") as f:
            w=csv.writer(f); w.writerow(headers)
            for line,en,de,issues in findings[start:start+args.chunk_size]: w.writerow([line,en,de,issues,"",""])
    (out/"SUMMARY.md").write_text(f"# Translation QA summary\n\n- Source: `{args.csv_file}`\n- Rows: {len(rows)}\n- Flagged: {len(findings)}\n- Chunk size: {args.chunk_size}\n- Review files: {(len(findings)+args.chunk_size-1)//args.chunk_size}\n",encoding="utf-8")
    print(f"Checked {len(rows)} rows; flagged {len(findings)}")
if __name__=="__main__": main()
