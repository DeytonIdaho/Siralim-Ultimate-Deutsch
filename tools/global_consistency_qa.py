#!/usr/bin/env python3
"""Cross-file consistency QA. Read-only; writes reports to consistency_review/."""
import csv,re
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path('.');OUT=Path('consistency_review');EN_COLS=('english','en','source','original','text_en','description_en');DE_COLS=('german','de','deutsch','translation','text_de','description_de')
TOKEN=re.compile(r'\{[^{}]+\}|<\d+>|\[[^\[\]]+\]');NUM=re.compile(r'(?<![\w])\d+(?:\.\d+)?%?')
RULES={'creature':('Kreatur','Kreaturen','Wesen','Monster','Gegnerwesen'),'trait':('Merkmal','Eigenschaft'),'stat':('Attribut','Attribute','Wert','Werte','Status','Eigenschaft'),'spell gem':('Zauberstein','Zaubersteine'),'artifact':('Artefakt','Artefakte'),'relic':('Relikt','Relikte'),'buff':('Buff','Buffs','buffen','Buffe','bufft','gebufft'),'debuff':('Debuff','Debuffs','debuffen','Debuffe','debufft','gedebufft'),'minion':('Diener','Dienern','Dienermeister','Dienerschaden'),'charge':('Ladung','Ladungen'),'maximum':('maximal','Maximum'),'current':('aktuell','derzeitig','gegenwärtig'),'additional':('zusätzlich','weiter'),'independent':('unabhängig',),'manually':('manuell',),'instead':('statt','anstatt'),'once per turn':('einmal pro Zug',),'for each':('für jede','für jeden','für jedes','pro '),'cannot':('kann nicht','können nicht'),'always':('immer',),'before':('bevor','vor '),'after':('nachdem','nach '),'start of':('zu Beginn','am Anfang'),'end of':('am Ende','zum Ende')}
SUS={'Plünderer':'Reaver specialization','Behändigkeit':'Celerity/Schnelligkeit reference','Vorteilspunkte':'old perk terminology','Vorteilsrang':'old perk terminology','Stat Slots':'Attribut-Slots','Spell Gems':'untranslated gameplay term'}
FOCUSED={
 'trait':(re.compile(r'\btraits?\b',re.I),(re.compile(r'\bmerkmale?n?\b',re.I),)),
 'buff':(re.compile(r'\bbuffs?\b',re.I),(re.compile(r'\bbuff(?:s|e|en|t|te|ten)?\b|\bgebufft\b',re.I),)),
 'debuff':(re.compile(r'\bdebuffs?\b',re.I),(re.compile(r'\bdebuff(?:s|e|en|t|te|ten)?\b|\bgedebufft\b',re.I),)),
 'minion':(re.compile(r'\bminions?\b',re.I),(re.compile(r'\bdiener(?:n|s)?(?:meister(?:s)?|schaden(?:s)?)?\b',re.I),)),
 'perk':(re.compile(r'\bperks?\b|\bperk[ -](?:points?|ranks?|menu|screen|list|tree)\b',re.I),(re.compile(r'\b(?:spezialisierungs)?talent(?:e|en|s|punkt(?:e|en|s)?|rang(?:e|es|en)?|menü|liste|baum)?\b',re.I),))}
def cols(fs):
 lo={x.lower():x for x in fs};return next((lo[x] for x in EN_COLS if x in lo),None),next((lo[x] for x in DE_COLS if x in lo),None)
def norm(s):return re.sub(r'\s+',' ',(s or '').strip())
def dump(name,header,data):
 with (OUT/name).open('w',encoding='utf-8',newline='') as f:w=csv.writer(f);w.writerow(header);w.writerows(data)
def main():
 OUT.mkdir(exist_ok=True);rows=[]
 for p in sorted(ROOT.glob('*.csv')):
  with p.open(encoding='utf-8-sig',newline='') as f:
   r=csv.DictReader(f);e,d=cols(r.fieldnames or [])
   if not e or not d:continue
   for line,row in enumerate(r,2):rows.append((p.name,line,row.get(e,'') or '',row.get(d,'') or ''))
 exact=defaultdict(Counter);examples=defaultdict(lambda:defaultdict(list));rc={k:Counter() for k in RULES};sus=[];tm=[];nm=[];focused={k:[] for k in FOCUSED}
 for fn,line,en,de in rows:
  ne,nd=norm(en),norm(de)
  if ne:
   exact[ne][nd]+=1
   if len(examples[ne][nd])<3:examples[ne][nd].append(f'{fn}:{line}')
  et,dt=Counter(TOKEN.findall(en)),Counter(TOKEN.findall(de))
  if et!=dt:tm.append((fn,line,en,de,str(dict(et)),str(dict(dt))))
  ev=Counter(NUM.findall(TOKEN.sub('',en)));dv=Counter(NUM.findall(TOKEN.sub('',de)))
  if ev!=dv:nm.append((fn,line,en,de,str(dict(ev)),str(dict(dv))))
  low,dl=en.lower(),de.lower()
  for key,variants in RULES.items():
   if key in low:rc[key][next((v for v in variants if v.lower() in dl),'<none>')]+=1
  for key,(enpat,depats) in FOCUSED.items():
   if enpat.search(en) and not any(p.search(de) for p in depats):focused[key].append((fn,line,en,de))
  for bad,note in SUS.items():
   if bad.lower() in dl:sus.append((fn,line,bad,note,en,de))
 with (OUT/'same_english_multiple_german.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.writer(f);w.writerow(['english','variants','german','count','examples'])
  for en,c in sorted(exact.items(),key=lambda x:(-len(x[1]),x[0])):
   vals=[(de,n) for de,n in c.items() if de]
   if len(vals)>1:
    for de,n in vals:w.writerow([en,len(vals),de,n,'; '.join(examples[en][de])])
 dump('token_mismatches.csv',['file','line','english','german','english_tokens','german_tokens'],tm);dump('number_mismatches.csv',['file','line','english','german','english_numbers','german_numbers'],nm);dump('suspect_terms.csv',['file','line','term','reason','english','german'],sus)
 for key,data in focused.items():dump(f'{key}_outliers.csv',['file','line','english','german'],data)
 with (OUT/'rule_term_matrix.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.writer(f);w.writerow(['english_rule_term','german_variant','count'])
  for k,c in rc.items():
   for v,n in c.most_common():w.writerow([k,v,n])
 multi=sum(1 for c in exact.values() if len([x for x in c if x])>1);fs='\n'.join(f'- {k} focused outliers: {len(v)}' for k,v in focused.items())
 summary=f'# Global consistency QA\n\n- Localization rows scanned: {len(rows)}\n- Exact English strings with multiple German variants: {multi}\n- Token mismatch candidates: {len(tm)}\n- Number/percentage mismatch candidates: {len(nm)}\n- Explicit suspect-term occurrences: {len(sus)}\n{fs}\n\nThese are review candidates, not automatic errors.\n';(OUT/'SUMMARY.md').write_text(summary,encoding='utf-8');print(summary)
if __name__=='__main__':main()
