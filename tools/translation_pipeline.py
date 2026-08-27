#!/usr/bin/env python3
"""Siralim Ultimate German translation QA helper.

Reads large CSV files locally (no GitHub API size limitation), compares source and
German text, checks placeholders/tags and terminology, then writes small review
chunks that can be committed and reviewed independently.

Examples:
  python tools/translation_pipeline.py data/perks.csv --out review/perks
  python tools/translation_pipeline.py data/traits.csv --out review/traits --chunk-size 150
"""
from __future__ import annotations
import argparse, csv, re
from collections import Counter
from pathlib import Path

TOKEN_RE = re.compile(r"(?:\{[^{}]+\}|\[[^\[\]]+\]|<[^<>]+>|%\w|\\n)")
DEFAULT_TERMS = {
    "Attack": "Angriff", "Defense": "Verteidigung", "Speed": "Geschwindigkeit",
    "Intelligence": "Intelligenz", "Health": "Gesundheit", "Damage": "Schaden",
    "Spell": "Zauber", "Spells": "Zauber", "Creature": "Kreatur", "Creatures": "Kreaturen",
    "Buff": "Stärkung", "Debuff": "Schwächung", "Trait": "Eigenschaft", "Traits": "Eigenschaften",
}

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
    if not src or not de:
        raise SystemExit(f"Could not detect EN/DE columns. Columns: {fields}")
    return src, de

def load_glossary(path):
    terms = dict(DEFAULT_TERMS)
    if path and Path(path).exists():
        with open(path, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                en = norm(r.get("English") or r.get("EN") or r.get("Source"))
                de = norm(r.get("German") or r.get("DE") or r.get("Deutsch"))
                if en and de: terms[en] = de
    return terms

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("csv_file")
    ap.add_argument("--out", required=True)
    ap.add_argument("--glossary")
    ap.add_argument("--chunk-size", type=int, default=100)
    args=ap.parse_args()
    out=Path(args.out); out.mkdir(parents=True, exist_ok=True)
    terms=load_glossary(args.glossary)
    with open(args.csv_file, encoding="utf-8-sig", newline="") as f:
        rd=csv.DictReader(f); src_col,de_col=detect_columns(rd.fieldnames or [])
        rows=list(rd)
    findings=[]
    for i,r in enumerate(rows, start=2):
        en,de=norm(r.get(src_col)),norm(r.get(de_col)); issues=[]
        if en and not de: issues.append("MISSING_TRANSLATION")
        if tokens(en)!=tokens(de): issues.append("TOKEN_MISMATCH")
        for term,want in terms.items():
            if re.search(r"\b"+re.escape(term)+r"\b", en, re.I) and want.lower() not in de.lower():
                issues.append(f"TERM:{term}->{want}")
        if issues: findings.append((i,en,de,"; ".join(issues)))
    headers=["line","english","german","issues","reviewed","replacement"]
    for n,start in enumerate(range(0,len(findings),args.chunk_size),1):
        p=out/f"review_{n:03d}.csv"
        with p.open("w",encoding="utf-8",newline="") as f:
            w=csv.writer(f); w.writerow(headers)
            for line,en,de,issues in findings[start:start+args.chunk_size]: w.writerow([line,en,de,issues,"",""])
    summary=out/"SUMMARY.md"
    summary.write_text(f"# Translation QA summary\n\n- Source: `{args.csv_file}`\n- Rows: {len(rows)}\n- Flagged: {len(findings)}\n- Chunk size: {args.chunk_size}\n- Review files: {(len(findings)+args.chunk_size-1)//args.chunk_size}\n\nChecks: missing translations, placeholder/tag parity, glossary terminology.\n",encoding="utf-8")
    print(f"Checked {len(rows)} rows; flagged {len(findings)}. Output: {out}")
if __name__=="__main__": main()
