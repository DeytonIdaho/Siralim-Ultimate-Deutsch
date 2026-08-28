#!/usr/bin/env python3
"""Cross-file consistency QA for the German Siralim Ultimate localization.

Read-only: scans every root CSV and writes reports under consistency_review/.
It deliberately reports candidates rather than modifying translations.
"""
import csv,re
from pathlib import Path
from collections import Counter,defaultdict

ROOT=Path('.')
OUT=Path('consistency_review')
EN_COLS=('english','en','source','original','text_en','description_en')
DE_COLS=('german','de','deutsch','translation','text_de','description_de')
TOKEN=re.compile(r'\{[^{}]+\}|<\d+>|\[[^\[\]]+\]')
NUM=re.compile(r'(?<![\w])\d+(?:\.\d+)?%?')

# High-value rule vocabulary. These are candidate detectors, not automatic errors.
RULES={
 'creature':('Kreatur','Kreaturen','Wesen','Monster','Gegnerwesen'),
 'trait':('Merkmal','Eigenschaft'),
 'stat':('Attribut','Attribute','Wert','Werte','Status','Eigenschaft'),
 'spell gem':('Zauberstein','Zaubersteine','Zauberjuwel','Zauberjuwelen'),
 'artifact':('Artefakt','Artefakte'),
 'relic':('Reliquie','Reliquien','Relikt','Relikte'),
 'buff':('Buff','Buffs','Verbesserung','Verbesserungen'),
 'debuff':('Debuff','Debuffs','Schwächung','Schwächungen'),
 'minion':('Diener','Dienern','Minion','Minions'),
 'charge':('Ladung','Ladungen'),
 'maximum':('maximal','maximale','maximalen','Maximum'),
 'current':('aktuell','aktuelle','derzeitig','gegenwärtig'),
 'additional':('zusätzlich','zusätzliche','weiter','weiteres'),
 'independent':('unabhängig','unabhängige'),
 'manually':('manuell',),
 'instead':('statt','anstatt'),
 'once per turn':('einmal pro Zug','1 Mal pro Zug','ein Mal pro Zug'),
 'for each':('für jede','für jeden','für jedes','pro '),
 'cannot':('kann nicht','können nicht','unfähig'),
 'always':('immer',),
 'before':('bevor','vor '),
 'after':('nachdem','nach '),
 'start of':('zu Beginn','am Anfang'),
 'end of':('am Ende','zum Ende'),
}

# Known project decisions worth detecting explicitly.
FORBIDDEN_OR_SUSPECT={
 'Plünderer':'Use Reaver for the specialization',
 'Behändigkeit':'Check whether this is an inconsistent Celerity/Schnelligkeit reference',
 'Vorteilspunkte':'Prefer Talentpunkte where the English means perk points',
 'Stat Slots':'Prefer Attribut-Slots',
 'Spell Gems':'Untranslated English gameplay term',
}

def cols(fields):
 lo={x.lower():x for x in fields}
 return next((lo[x] for x in EN_COLS if x in lo),None),next((lo[x] for x in DE_COLS if x in lo),None)

def norm(s):return re.sub(r'\s+',' ',(s or '').strip())

def main():
 OUT.mkdir(exist_ok=True)
 rows=[]
 for p in sorted(ROOT.glob('*.csv')):
  with p.open(encoding='utf-8-sig',newline='') as f:
   r=csv.DictReader(f);e,d=cols(r.fieldnames or [])
   if not e or not d:continue
   for line,row in enumerate(r,2):rows.append((p.name,line,row.get(e,'') or '',row.get(d,'') or ''))

 exact=defaultdict(Counter); examples=defaultdict(lambda:defaultdict(list))
 rule_counts={k:Counter() for k in RULES}; suspects=[]; token_mismatch=[]; number_mismatch=[]
 for fn,line,en,de in rows:
  ne,nd=norm(en),norm(de)
  if ne:
   exact[ne][nd]+=1
   if len(examples[ne][nd])<3:examples[ne][nd].append(f'{fn}:{line}')
  et=Counter(TOKEN.findall(en));dt=Counter(TOKEN.findall(de))
  if et!=dt:token_mismatch.append((fn,line,en,de,str(dict(et)),str(dict(dt))))
  # Numbers are compared as multisets; this catches changed percentages/counts while ignoring order.
  ev=Counter(NUM.findall(TOKEN.sub('',en)));dv=Counter(NUM.findall(TOKEN.sub('',de))
  if ev!=dv:number_mismatch.append((fn,line,en,de,str(dict(ev)),str(dict(dv))))
  low=en.lower();dl=de.lower()
  for key,variants in RULES.items():
   if key in low:
    hit=next((v for v in variants if v.lower() in dl),'<none>')
    rule_counts[key][hit]+=1
  for bad,note in FORBIDDEN_OR_SUSPECT.items():
   if bad.lower() in dl:suspects.append((fn,line,bad,note,en,de))

 # Same exact English source translated differently across the project.
 with (OUT/'same_english_multiple_german.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.writer(f);w.writerow(['english','variants','german','count','examples'])
  for en,c in sorted(exact.items(),key=lambda x:(-len(x[1]),x[0])):
   nonempty=[(de,n) for de,n in c.items() if de]
   if len(nonempty)>1:
    for de,n in nonempty:w.writerow([en,len(nonempty),de,n,'; '.join(examples[en][de])])

 def dump(name,header,data):
  with (OUT/name).open('w',encoding='utf-8',newline='') as f:
   w=csv.writer(f);w.writerow(header);w.writerows(data)
 dump('token_mismatches.csv',['file','line','english','german','english_tokens','german_tokens'],token_mismatch)
 dump('number_mismatches.csv',['file','line','english','german','english_numbers','german_numbers'],number_mismatch)
 dump('suspect_terms.csv',['file','line','term','reason','english','german'],suspects)
 with (OUT/'rule_term_matrix.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.writer(f);w.writerow(['english_rule_term','german_variant','count'])
  for k,c in rule_counts.items():
   for v,n in c.most_common():w.writerow([k,v,n])

 multi=sum(1 for c in exact.values() if len([x for x in c if x])>1)
 summary=(
  '# Global consistency QA\n\n'
  f'- Localization rows scanned: {len(rows)}\n'
  f'- Exact English strings with multiple German variants: {multi}\n'
  f'- Token mismatch candidates: {len(token_mismatch)}\n'
  f'- Number/percentage mismatch candidates: {len(number_mismatch)}\n'
  f'- Explicit suspect-term occurrences: {len(suspects)}\n\n'
  'These are review candidates, not automatic errors. Context-sensitive German inflection and deliberate dynamic tokens can produce false positives.\n'
 )
 (OUT/'SUMMARY.md').write_text(summary,encoding='utf-8')
 print(summary)
if __name__=='__main__':main()
