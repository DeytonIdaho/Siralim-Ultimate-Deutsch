#!/usr/bin/env python3
import csv,re,sys
from pathlib import Path
src=Path(sys.argv[1] if len(sys.argv)>1 else 'perks.csv');out=Path(sys.argv[2] if len(sys.argv)>2 else 'review/perks_consistency.csv')
checks=[('OLD_CREATURE',r'\b(?:Wesen|Wesens)\b'),('OLD_SPELLGEM',r'\b(?:Zauberedelstein\w*|Zauber-Edelstein\w*|Zaubergem\w*|Zauber-Juwel\w*)\b'),('OLD_MINION',r'\b(?:Lakai\w*|Begleiter\w*|Schergen\w*|Handlanger\w*)\b'),('OLD_TRAIT',r'\bEigenschaft(?:en)?\b'),('OLD_STAT',r'\bStatuswert\w*\b'),('STACKING',r'\b(?:stapelbar|stapelt sich)\b'),('CRIT_HIT',r'\bkritische(?:r|n|m|s)? Treffer\b'),('BAD_POSSESSIVE',r"\bKreaturen'\b")]
with src.open(encoding='utf-8-sig',newline='')as f:
 rd=csv.DictReader(f);fields=rd.fieldnames or[];low={x.lower():x for x in fields};de=next((low[x] for x in('german','de','deutsch','translation','text_de','description_de')if x in low),None);en=next((low[x] for x in('english','en','source','original','text_en','description_en')if x in low),None)
 if not de:raise SystemExit('German column not found')
 rows=[]
 for line,r in enumerate(rd,2):
  text=r.get(de,'')or'';english=r.get(en,'')if en else''
  for name,pat in checks:
   if name=='OLD_TRAIT' and not re.search(r'\btraits?\b',english,re.I):continue
   if name=='OLD_MINION' and not re.search(r'\bminions?\b|on-minion',english,re.I):continue
   if re.search(pat,text,re.I):rows.append([line,name,english,text])
  if re.search(r'\b(?:potency|potent)\b',english,re.I) and re.search(r'\b(?:Wirksamkeit|Potenz)\b',text,re.I):rows.append([line,'POTENCY',english,text])
out.parent.mkdir(parents=True,exist_ok=True)
with out.open('w',encoding='utf-8',newline='')as f:w=csv.writer(f);w.writerow(['line','check','english','german']);w.writerows(rows)
print(f'Perk consistency scan: {len(rows)} candidates')
