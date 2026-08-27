#!/usr/bin/env python3
import csv,re,sys
from pathlib import Path
files=sys.argv[1:] or ['quests.csv','overworld.csv','codex.csv','cards.csv']
patterns=[('OLD_SPELLGEM',r'(?:Zauberedelstein\w*|Zauber-Edelstein\w*|Zaubergem\w*|Zauber-Juwel\w*|Zauberjuwel\w*)'),('OLD_MINION',r'\b(?:Schergen\w*|Handlanger\w*|Lakai\w*|Lakaien\w*)\b'),('OLD_STAT',r'\bStatuswert\w*\b'),('AI_ARTIFACT',r'(?i)\b(?:ChatGPT|assistant:)\b')]
rows=[]
for fn in files:
 with open(fn,encoding='utf-8-sig',newline='')as f:
  rd=csv.DictReader(f);low={x.lower():x for x in(rd.fieldnames or[])};en=next((low[x] for x in('english','en','source','original','text_en','description_en')if x in low),None);de=next((low[x] for x in('german','de','deutsch','translation','text_de','description_de')if x in low),None)
  if not de:continue
  for line,r in enumerate(rd,2):
   e=r.get(en,'')if en else'';d=r.get(de,'')or''
   for name,pat in patterns:
    if re.search(pat,d,re.I):rows.append([fn,line,name,e,d])
   if re.search(r'\btraits?\b',e,re.I) and re.search(r'\bEigenschaft(?:en|splätze|smaterialien)?\b',d,re.I):rows.append([fn,line,'OLD_TRAIT',e,d])
   if re.search(r'\b(?:potency|potent)\b',e,re.I) and re.search(r'\b(?:Wirksamkeit|Potenz)\b',d,re.I):rows.append([fn,line,'POTENCY',e,d])
   if re.search(r'\bcreatures?\b',e,re.I) and re.search(r'\bWesen\b',d,re.I):rows.append([fn,line,'CREATURE_AS_WESEN',e,d])
out=Path('review/content_consistency.csv');out.parent.mkdir(parents=True,exist_ok=True)
with out.open('w',encoding='utf-8',newline='')as f:w=csv.writer(f);w.writerow(['file','line','check','english','german']);w.writerows(rows)
print(f'Content consistency scan: {len(rows)} candidates')
