#!/usr/bin/env python3
import csv,re,sys
from pathlib import Path
files=sys.argv[1:] or ['spells.csv','battle.csv','creatures.csv','items.csv','accessories.csv','masters.csv','projects.csv']
out=Path('review/gameplay_consistency.csv')
patterns=[('OLD_SPELLGEM',r'(?:Zauberedelstein\w*|Zauber-Edelstein\w*|Zaubergem\w*|Zauber-Juwel\w*)'),('OLD_MINION',r'\b(?:Schergen\w*|Lakai\w*|Lakaien\w*|Handlanger\w*)\b'),('OLD_STAT',r'\bStatuswert\w*\b'),('OLD_DEBUFF',r'\b(?:Schwächungseffekt\w*|Schwächungszauber\w*)\b'),('STACKING',r'\b(?:stapelbar|stapelt sich)\b'),('BAD_POSSESSIVE',r"\bKreaturen'\b"),('AI_ARTIFACT',r'(?i)\b(?:ChatGPT|assistant:)\b')]
rows=[]
for fn in files:
 p=Path(fn)
 with p.open(encoding='utf-8-sig',newline='')as f:
  rd=csv.DictReader(f);fs=rd.fieldnames or[];low={x.lower():x for x in fs};de=next((low[x] for x in('german','de','deutsch','translation','text_de','description_de')if x in low),None);en=next((low[x] for x in('english','en','source','original','text_en','description_en')if x in low),None)
  if not de:continue
  for line,r in enumerate(rd,2):
   text=r.get(de,'')or'';english=r.get(en,'')if en else''
   for name,pat in patterns:
    if re.search(pat,text,re.I):rows.append([fn,line,name,english,text])
   if re.search(r'\btraits?\b',english,re.I) and re.search(r'\bEigenschaft(?:en)?\b',text,re.I):rows.append([fn,line,'OLD_TRAIT',english,text])
   if re.search(r'\bminions?\b|on-minion',english,re.I) and re.search(r'\b(?:Begleiter|Begleitern)\b',text,re.I):rows.append([fn,line,'OLD_MINION',english,text])
   if re.search(r'\b(?:potency|potent)\b',english,re.I) and re.search(r'\b(?:Wirksamkeit|Potenz)\b',text,re.I):rows.append([fn,line,'POTENCY',english,text])
out.parent.mkdir(parents=True,exist_ok=True)
with out.open('w',encoding='utf-8',newline='')as f:w=csv.writer(f);w.writerow(['file','line','check','english','german']);w.writerows(rows)
print(f'Gameplay consistency scan: {len(rows)} candidates across {len(files)} files')
