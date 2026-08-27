#!/usr/bin/env python3
import csv,re,sys
from pathlib import Path
files=sys.argv[1:] or ['misc.csv','dialog.csv','decorations.csv','personality.csv','dialog_story.csv']
checks=[('OLD_SPELLGEM',r'(?:Zauberedelstein\w*|Zauber-Edelstein\w*|Zaubergem\w*|Zauber-Juwel\w*|Zauberjuwel\w*)'),('OLD_MINION',r'\b(?:Schergen\w*|Lakai\w*|Lakaien\w*)\b'),('OLD_STAT',r'\bStatuswert\w*\b'),('AI_ARTIFACT',r'(?i)\b(?:ChatGPT|assistant:)\b')]
rows=[]
for fn in files:
 with open(fn,encoding='utf-8-sig',newline='')as f:
  rd=csv.DictReader(f);low={x.lower():x for x in(rd.fieldnames or[])};en=next((low[x] for x in('english','en','source','original','text_en','description_en')if x in low),None);de=next((low[x] for x in('german','de','deutsch','translation','text_de','description_de')if x in low),None)
  if not de:continue
  for line,r in enumerate(rd,2):
   e=r.get(en,'')if en else'';d=r.get(de,'')or''
   for name,pat in checks:
    if re.search(pat,d,re.I):rows.append([fn,line,name,e,d])
   # Strict only for unmistakable game terminology, not ordinary narrative words.
   if re.search(r'\bTrait Materials?\b',e,re.I) and re.search(r'Eigenschaftsmaterial',d,re.I):rows.append([fn,line,'TRAIT_MATERIAL',e,d])
   if re.search(r'\bSpell Gems?\b',e,re.I) and not re.search(r'Zauberstein',d,re.I):rows.append([fn,line,'SPELL_GEM_TERM',e,d])
   # Catch untranslated source fragments and common machine artifacts without policing style.
   if re.search(r'(?i)\b(?:the creature|spell gems?|trait material)\b',d):rows.append([fn,line,'ENGLISH_FRAGMENT',e,d])
out=Path('review/narrative_consistency.csv');out.parent.mkdir(parents=True,exist_ok=True)
with out.open('w',encoding='utf-8',newline='')as f:w=csv.writer(f);w.writerow(['file','line','check','english','german']);w.writerows(rows)
print(f'Narrative consistency scan: {len(rows)} candidates')
