#!/usr/bin/env python3
import base64,csv,io,json,zlib
from pathlib import Path
parts=[Path(f'tools/creature_name_fixes_20260830_{i}.dat').read_text(encoding='ascii').strip() for i in (1,2,3)]
FIX={t:(o,n) for t,o,n in json.loads(zlib.decompress(base64.b64decode(''.join(parts))))}
if len(FIX)!=232: raise SystemExit(f'Unexpected patch size: {len(FIX)}')
p=Path('creatures.csv'); raw=p.read_bytes(); bom=b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''; body=raw[len(bom):].decode('utf-8'); lines=body.splitlines(keepends=True)
rows=list(csv.DictReader(io.StringIO(body)))
if len(rows)!=1612: raise SystemExit(f'Unexpected row count: {len(rows)}')
if len(lines)!=len(rows)+1: raise SystemExit('Unexpected multiline CSV records')
h=next(csv.reader([lines[0].rstrip('\r\n')])); ti,gi=h.index('Tag'),h.index('German'); seen=set(); out=[lines[0]]; changed=0
for line in lines[1:]:
 e='\r\n' if line.endswith('\r\n') else ('\n' if line.endswith('\n') else ''); text=line[:-len(e)] if e else line; f=next(csv.reader([text])); tag=f[ti]
 if tag in FIX:
  if tag in seen: raise SystemExit('Duplicate tag '+tag)
  seen.add(tag); old,new=FIX[tag]
  if f[gi]!=old: raise SystemExit(f'Unexpected old value {tag}: {f[gi]!r} != {old!r}')
  f[gi]=new; b=io.StringIO(newline=''); csv.writer(b,lineterminator='').writerow(f); out.append(b.getvalue()+e); changed+=1
 else: out.append(line)
missing=set(FIX)-seen
if missing: raise SystemExit('Missing tags: '+', '.join(sorted(missing)))
if changed!=len(FIX): raise SystemExit(f'Expected {len(FIX)} changes, got {changed}')
p.write_bytes(bom+''.join(out).encode('utf-8'))
with p.open(encoding='utf-8-sig',newline='') as fh: result={r['Tag']:r for r in csv.DictReader(fh)}
for tag,(_,new) in FIX.items():
 if result[tag]['German']!=new: raise SystemExit('Post-check failed '+tag)
print(f'Applied and verified {changed} reviewed creature-name changes')
