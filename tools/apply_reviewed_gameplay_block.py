import csv,json,zlib,base64
payload=''.join(open(f'tools/review_block_97_{i}.dat',encoding='utf-8').read().strip() for i in range(1,5))
CHANGES=json.loads(zlib.decompress(base64.b64decode(payload)))
count=0
for fn,edits in CHANGES.items():
    with open(fn,encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f)); fields=list(rows[0])
    for idx,tag,english,old,new in edits:
        r=rows[idx]
        if (r['Tag'],r['English'])!=(tag,english):
            raise SystemExit(f'{fn}:{idx+2} identity mismatch')
        if r['German'] not in (old,new):
            raise SystemExit(f"{fn}:{idx+2} unexpected German: {r['German']!r}")
        if r['German']!=new:
            r['German']=new; count+=1
    with open(fn,'w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(rows)
print(f'Applied {count} pending changes; verified {sum(map(len,CHANGES.values()))} reviewed row targets.')
