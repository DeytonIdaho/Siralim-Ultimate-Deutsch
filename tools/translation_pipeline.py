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
 for p,r in [(r"Ultimativzauber-Edelsteine","Ultimative Zaubersteine"),(r"Zauberjuwel","Zauberstein"),(r"Zauber-Edelsteine","Zaubersteine"),(r"Zauber-Edelstein","Zauberstein"),(r"Zauberedelsteine","Zaubersteine"),(r"Zauberedelstein","Zauberstein"),(r"Zaubergems","Zaubersteine"),(r"Zaubergem","Zauberstein"),(r"Zauber-Juwel","Zauberstein"),(r"Schergen","Diener"),(r"Handlanger","Diener"),(r"Statuswerte","Attribute"),(r"Statuswert","Attribut")]:out=re.sub(p,r,out)
 if re.search(r"\btraits?\b",en,re.I):out=re.sub(r"Eigenschaftsplätze","Merkmalsplätze",out);out=re.sub(r"Eigenschaftsmaterialien","Merkmalsmaterialien",out);out=re.sub(r"Eigenschaften","Merkmale",out);out=re.sub(r"Eigenschaft","Merkmal",out)
 if en.startswith("Find gem fragments in this Realm to create a new Spell Gem."):out="Finde Edelsteinfragmente in diesem Reich, um einen neuen Zauberstein herzustellen."
 # Fully repair damaged Codex Cards page.
 if en.startswith("Cards are extremely rare items that have a chance to drop from enemy creatures after battle."):
  out='Karten sind extrem seltene Gegenstände, die nach einem Kampf mit einer gewissen Wahrscheinlichkeit von feindlichen Kreaturen fallen gelassen werden. Jede Karte gehört zu einem "Karten-Set". Wenn du genügend Karten eines Karten-Sets sammelst, erhalten deine Kreaturen im Kampf einen passiven Bonus. Für jede einzelne Kreatur in Rodia gibt es eine Karte.\\n\\nDu kannst alle gesammelten Karten sowie die dafür freigeschalteten Boni ansehen, indem du im Hauptmenü die Option [menu_cards] Karten auswählst.\\n\\nDu kannst zwar doppelte Karten sammeln, diese gewähren jedoch nur die zusätzlichen Attributsboni, die sie normalerweise verleihen würden, und tragen nicht zu den Karten-Set-Boni bei.'
 # Mechanical creature terminology in Codex pages.
 if en.startswith("Each creature has a unique, innate trait that changes the way it fights in battle."):
  out='Jede Kreatur besitzt ein einzigartiges, angeborenes Merkmal, das ihre Kampfweise im Kampf verändert.\\n\\nWenn du zwei Kreaturen miteinander verschmilzt, erbt der Nachwuchs die Merkmale beider Eltern.\\n\\nKreaturen können ein zusätzliches Merkmal erhalten, indem sie den Merkmalsplatz ihres Artefakts bestücken.'
 if en.startswith('Each creature belongs to a "race".'):
  out='Jede Kreatur gehört einer "Rasse" an. Eine Rasse umfasst normalerweise etwa 6 Kreaturen, deren Klasse, Merkmale und Attribute meist miteinander harmonieren.\\n\\nWenn du neu in Siralim Ultimate bist und noch nicht weißt, wie du ein starkes Team zusammenstellst, kannst du zunächst ein Team aus Kreaturen derselben Rasse bilden, bis du das Spiel besser kennst.'
 if en.startswith("Each creature belongs to one of five classes:"):
  out='Jede Kreatur gehört einer von fünf Klassen an: {CLASS_Chaos}, {CLASS_Death}, {CLASS_Life}, {CLASS_Nature} oder {CLASS_Sorcery}.\\n\\nWenn eine deiner Kreaturen einem Feind Schaden zufügt, wird der Schaden erhöht, wenn die Klasse deiner Kreatur stark gegen die Klasse des Feindes ist.\\n\\nWenn du einen Feind anvisierst, zeigt ein Indikator an, ob er gegen die Klasse deiner Kreatur stark oder schwach ist. Daher musst du dir nicht merken, welche Klasse gegen welche andere stark oder schwach ist.'
 if en.startswith("Each god has a corresponding Relic for you to unlock."):
  out='Jeder Gott besitzt eine entsprechende Reliquie, die du freischalten kannst. Reliquien können mit Frömmigkeit aufgewertet werden. Mit steigendem Rang gewährt eine Reliquie der auf sie abgestimmten Kreatur einen stärkeren Attributsbonus. Zusätzlich erhält die abgestimmte Kreatur alle 10 Ränge (bis Rang 100) einen zusätzlichen Vorteil. Du kannst eine Reliquie über Rang 100 hinaus aufwerten, danach erhöht sich jedoch nur noch ihr Attributsbonus.'
 if en.startswith("When one of your creatures damages an enemy, some of that damage is reflected back to your creature."):out="Wenn eine deiner Kreaturen einem Feind Schaden zufügt, wird ein Teil dieses Schadens auf deine Kreatur zurückgeworfen."
 if en=="Enemies start battles with the specified minion.":out="Feinde beginnen Kämpfe mit dem angegebenen Diener."
 # Previous key fixes.
 if en.startswith("Your creatures' Spell Gems that belong to other classes have 5% more potency."):out=re.sub(r"Wirksamkeit","Zaubermacht",out)
 if en.startswith("Now that you've created a macro, you must assign it to a creature to use it in battle."):
  out='Nachdem du ein Makro erstellt hast, musst du es einer Kreatur zuweisen, um es im Kampf zu verwenden. Öffne das Hauptmenü, wähle "Kreaturen" und anschließend die Kreatur, der du ein Makro zuweisen möchtest. Wähle dann "Makro zuweisen" und das gewünschte Makro.\\n\\nWenn diese Kreatur im Kampf den Befehl "Makro" auswählt, wertet sie alle Zeilen des Makros aus und versucht zu bestimmen, was sie tun soll.\\n\\nStell dir vor, das auf der vorherigen Seite erwähnte Makro wurde einer deiner Kreaturen zugewiesen. Wenn die Gesundheit eines ihrer Verbündeten unter 20% fällt und du anschließend den Befehl "Makro" verwendest, wirkt sie den Zauber "Heilung" auf diesen Verbündeten, sofern sie den Zauber ausgerüstet hat.'
 return out
def exception(en,term=None):return False
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
