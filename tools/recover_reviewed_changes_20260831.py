import base64,csv,json,zlib
from pathlib import Path
parts=['tools/recovery_payload_20260831.part1','tools/recovery_payload_20260831.part2','tools/recovery_payload_20260831.rem1','tools/recovery_payload_20260831.rem2','tools/recovery_payload_20260831.rem3','tools/recovery_payload_20260831.rem4','tools/recovery_payload_20260831.rem5']
payload=''.join(Path(p).read_text(encoding='utf-8').strip() for p in parts)
DATA=json.loads(zlib.decompress(base64.b64decode(payload)).decode('utf-8'))

def read(fn):
    with open(fn,encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f); return r.fieldnames,list(r)

def write(fn,fields,rows):
    with open(fn,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\r\n'); w.writeheader(); w.writerows(rows)

for fn,edits in DATA.items():
    fields,rows=read(fn); tags=[r['Tag'] for r in rows]
    bytag={}
    for i,r in enumerate(rows): bytag.setdefault(r['Tag'],[]).append(i)
    changed=0
    for tag,old,new in edits:
        hits=[i for i in bytag.get(tag,[]) if rows[i]['German']==old]
        if len(hits)!=1:
            done=[i for i in bytag.get(tag,[]) if rows[i]['German']==new]
            if len(done)==1: continue
            raise SystemExit(f'{fn}/{tag}: expected exactly one old German value, got {len(hits)}')
        rows[hits[0]]['German']=new; changed+=1
    if [r['Tag'] for r in rows]!=tags: raise SystemExit(f'{fn}: tag/order changed')
    write(fn,fields,rows)
    f2,r2=read(fn)
    if f2!=fields or len(r2)!=len(rows) or [r['Tag'] for r in r2]!=tags: raise SystemExit(f'{fn}: round-trip validation failed')
    print(f'{fn}: {changed} newly applied; {len(edits)-changed} already present')
