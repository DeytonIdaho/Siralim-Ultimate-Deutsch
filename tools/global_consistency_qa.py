#!/usr/bin/env python3
"""Final cross-file consistency QA. Reports only unreviewed candidates."""
import csv,re
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path('.');OUT=Path('consistency_review');EN_COLS=('english','en','source','original','text_en','description_en');DE_COLS=('german','de','deutsch','translation','text_de','description_de')
TOKEN=re.compile(r'\{[^{}]+\}|<\d+>|\[[^\[\]]+\]');RAWNUM=re.compile(r'(?<![\w])\d+(?:[.,]\d+)*(?:%)?')
RULES={'buff':('Buff','Buffs','buffen','Buffe','bufft','gebufft'),'debuff':('Debuff','Debuffs','debuffen','Debuffe','debufft','gedebufft'),'minion':('Diener','Dienern','Dienermeister','Dienerschaden'),'perk':('Talent','Talente','Talenten','Talentpunkt','Talentpunkte','Talentrang')}
FOCUSED={'buff':(re.compile(r'\bbuffs?\b',re.I),re.compile(r'\bbuff(?:s|e|en|t|te|ten)?\b|\bgebufft\b',re.I)),'debuff':(re.compile(r'\bdebuffs?\b',re.I),re.compile(r'\bdebuff(?:s|e|en|t|te|ten)?\b|\bgedebufft\b',re.I)),'minion':(re.compile(r'\bminions?\b',re.I),re.compile(r'\bdiener',re.I)),'perk':(re.compile(r'\bperks?\b|\bperk[ -](?:points?|ranks?|menu|screen|list|tree)\b',re.I),re.compile(r'\b(?:spezialisierungs)?talent',re.I))}
ALLOWED_MULTI={'Attack','Casting','Provoking','Dice'}
def cols(fs):
 lo={x.lower():x for x in fs};return next((lo[x] for x in EN_COLS if x in lo),None),next((lo[x] for x in DE_COLS if x in lo),None)
def norm(s):return re.sub(r'\s+',' ',(s or '').strip())
def numcanon(s):
 pct=s.endswith('%');x=s[:-1] if pct else s
 if re.fullmatch(r'\d{1,3}(?:[,\.]\d{3})+',x):x=x.replace(',','').replace('.','')
 else:x=x.replace(',','.')
 return x+('%' if pct else '')
def nums(text):return Counter(numcanon(x) for x in RAWNUM.findall(TOKEN.sub('',text)))
def reviewed_token(en,de):
 # Relic achievement titles deliberately replace English relic names with localization tokens.
 if re.match(r'^(Earning|Empowering) ',en) and '{RELIC_' in de:return True
 # German repeats SCORN to make the switch pair explicit; semantics reviewed.
 if en.startswith('Enemies always have {CONDNAME_DEBUFF_SCORN}.') and de.count('{CONDNAME_DEBUFF_SCORN}')==2:return True
 # Literal bracket syntax, not a localization token.
 if en=='[[Macro Editor]':return True
 return False
def reviewed_number(en,de):
 if '5740-NG' in en and '{RELIC_ROBO}' in de:return True
 # German written-out number words preserve these exact source values.
 if en=='Random enemies take a moderate amount of damage 3 times, plus 2 more times for each dead creature on the battlefield.' and 'dreimal' in de and 'zweimal' in de:return True
 if en in ('Enemies take a moderate amount of damage 4 times.','Enemies take a moderate amount of damage 2 times.') and ('viermal' in de or 'zweimal' in de):return True
 if en.startswith("This creature's on-attack, on-cast, on-defend, and on-provoke effects have a 50% chance to activate 1 additional time.") and 'ein zusätzliches Mal' in de:return True
 if en.startswith('Enemies always have {CONDNAME_DEBUFF_SCORN}.') and de.count('1 Mal')==2:return True
 return False
def dump(name,header,data):
 with (OUT/name).open('w',encoding='utf-8',newline='') as f:w=csv.writer(f);w.writerow(header);w.writerows(data)
def main():
 OUT.mkdir(exist_ok=True);rows=[]
 for p in sorted(ROOT.glob('*.csv')):
  with p.open(encoding='utf-8-sig',newline='') as f:
   r=csv.DictReader(f);e,d=cols(r.fieldnames or [])
   if not e or not d:continue
   for line,row in enumerate(r,2):rows.append((p.name,line,row.get(e,'') or '',row.get(d,'') or ''))
 exact=defaultdict(Counter);examples=defaultdict(lambda:defaultdict(list));tm=[];nm=[];focused={k:[] for k in FOCUSED}
 for fn,line,en,de in rows:
  ne,nd=norm(en),norm(de)
  if ne:exact[ne][nd]+=1;examples[ne][nd].append(f'{fn}:{line}')
  et,dt=Counter(TOKEN.findall(en)),Counter(TOKEN.findall(de))
  if et!=dt and not reviewed_token(en,de):tm.append((fn,line,en,de,str(dict(et)),str(dict(dt))))
  ev,dv=nums(en),nums(de)
  if ev!=dv and not reviewed_number(en,de):nm.append((fn,line,en,de,str(dict(ev)),str(dict(dv))))
  for key,(ep,dp) in FOCUSED.items():
   if ep.search(en) and not dp.search(de):focused[key].append((fn,line,en,de))
 multirows=[]
 for en,c in sorted(exact.items()):
  if en in ALLOWED_MULTI:continue
  vals=[(de,n) for de,n in c.items() if de]
  if len(vals)>1:
   for de,n in vals:multirows.append((en,len(vals),de,n,'; '.join(examples[en][de][:3])))
 dump('same_english_multiple_german.csv',['english','variants','german','count','examples'],multirows);dump('token_mismatches.csv',['file','line','english','german','english_tokens','german_tokens'],tm);dump('number_mismatches.csv',['file','line','english','german','english_numbers','german_numbers'],nm)
 for k,v in focused.items():dump(f'{k}_outliers.csv',['file','line','english','german'],v)
 summary=f'# Final Global Consistency QA\n\n- Localization rows scanned: {len(rows)}\n- Unreviewed duplicate groups: {len(set(x[0] for x in multirows))}\n- Unreviewed token mismatches: {len(tm)}\n- Unreviewed number/percentage mismatches: {len(nm)}\n'+''.join(f'- {k} terminology outliers: {len(v)}\n' for k,v in focused.items())+'\nReviewed known exceptions are filtered from this final report.\n'
 (OUT/'SUMMARY.md').write_text(summary,encoding='utf-8');print(summary)
if __name__=='__main__':main()
