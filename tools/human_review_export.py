#!/usr/bin/env python3
import csv,sys,re
from pathlib import Path

def cols(fs):
 low={x.lower():x for x in fs}
 def pick(names):
  for n in names:
   if n in low:return low[n]
 return pick(['english','en','source','original','text_en','description_en']),pick(['german','de','deutsch','translation','text_de','description_de'])

def esc(s):
 return (s or '').replace('\r','').replace('\n','\\n').replace('|','\\|')

def main():
 fn=sys.argv[1];size=int(sys.argv[2]) if len(sys.argv)>2 else 100
 out=Path('human_review')/Path(fn).stem;out.mkdir(parents=True,exist_ok=True)
 with open(fn,encoding='utf-8-sig',newline='') as f:
  rd=csv.DictReader(f);ec,dc=cols(rd.fieldnames or []);rows=list(rd)
 if not ec or not dc:raise SystemExit(f'No EN/DE columns in {fn}')
 for start in range(0,len(rows),size):
  p=out/f'block_{start//size+1:03d}.md'
  lines=[f'# Human review: {fn} — {start+1}-{min(start+size,len(rows))}','', '| Row | English | German |','|---:|---|---|']
  for i,r in enumerate(rows[start:start+size],start+2):lines.append(f'| {i} | {esc(r.get(ec))} | {esc(r.get(dc))} |')
  p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
 (out/'SUMMARY.md').write_text(f'# Human review export\n\n- Source: `{fn}`\n- Rows: {len(rows)}\n- Block size: {size}\n- Blocks: {(len(rows)+size-1)//size}\n',encoding='utf-8')
if __name__=='__main__':main()
