#!/usr/bin/env python3
from pathlib import Path
import base64,csv,io,json,re,zlib
parts=[Path(f'tools/creature_name_fixes_20260830_{i}.dat').read_text(encoding='ascii').strip() for i in (1,2,3)]
FIX={t:(o,n) for t,o,n in json.loads(zlib.decompress(base64.b64decode(''.join(parts))))}
if len(FIX)!=232: raise SystemExit(f'Unexpected creature patch size: {len(FIX)}')
with open('creatures.csv',encoding='utf-8-sig',newline='') as f: creature_rows=list(csv.DictReader(f))
if len(creature_rows)!=1612: raise SystemExit(f'Unexpected creatures record count: {len(creature_rows)}')
creature_groups={}
for r in creature_rows: creature_groups.setdefault(r['Tag'],[]).append(r)
if len(creature_groups)!=1585 or sum(len(v)-1 for v in creature_groups.values())!=27: raise SystemExit('Unexpected creature tag structure')
creatures={}
for tag,group in creature_groups.items():
    if len({r['English'] for r in group})!=1: raise SystemExit(f'Conflicting English values for duplicate creature tag {tag}')
    creatures[tag]=group[0]
for tag,(old,new) in FIX.items():
    if tag not in creature_groups or any(r['German']!=new for r in creature_groups[tag]): raise SystemExit(f'creatures.csv not at reviewed state for {tag}')
TERM_RULES=[('Spell Gem','Edelsteine','Zaubersteine'),('Spell Gem','Edelstein','Zauberstein'),('Stat Slot','Statusplatz','Attributslot')]
OVERRIDES={
 ('bosses.csv','L_D_BOSS_COCKATRICE_2'):[('der Kokatrice','die Kokatrice'),('Seinem Charakter treu','Ihrem Charakter treu'),('sobald er dich sieht','sobald sie dich sieht')],
 ('bosses.csv','L_D_BOSS_COCKATRICE_3'):[('der Kokatrice','die Kokatrice')],
 ('bosses.csv','L_D_BOSS_NIX_3'):[('Der Nixe','Die Nixe'),('der es geworfen hat','die es geworfen hat')],
 ('items.csv','L_MAT_SIGILOFTHENIX'):[('des Nixe','der Nixe')],
 ('ui.csv','L_BLESS_MUSE_3'):[('Erwecktsstatuen','Statuen der Erweckten')],
 ('personality.csv','L_D_PERS_SPEED_ANIMATION'):[('Erweckts','Erweckten')],
 ('decorations.csv','L_DEC_ASTRALGALLERYANIMATIONSTATUE'):[('Erwecktsstatue','Statue der Erweckten')],
}
def records_with_raw(text):
    phys=text.splitlines(keepends=True); reader=csv.reader(io.StringIO(text,newline='')); out=[]; prev=0
    for row in reader:
        end=reader.line_num; out.append((row,''.join(phys[prev:end]))); prev=end
    if prev!=len(phys): raise SystemExit('CSV physical-line accounting mismatch')
    return out
files=sorted(p for p in Path('.').glob('*.csv') if p.name not in {'creatures.csv','battle.csv','TERMINOLOGIE.csv'})
plans=[]; parsed={}
for p in files:
    raw=p.read_bytes(); bom=raw.startswith(b'\xef\xbb\xbf'); text=(raw[3:] if bom else raw).decode('utf-8'); recs=records_with_raw(text)
    if len(recs)<2: continue
    header=recs[0][0]
    if not {'Tag','English','German'}.issubset(header): continue
    ti,ei,gi=header.index('Tag'),header.index('English'),header.index('German'); parsed[p]=(bom,recs,gi)
    for ri,(fields,rawrec) in enumerate(recs[1:],1):
        if len(fields)!=len(header): raise SystemExit(f'{p}: malformed CSV record {ri}')
        tag=fields[ti]; eng=fields[ei]; old_de=fields[gi]; new_de=old_de; reasons=[]
        # Record identity is (file, record index, tag, English, old German); duplicate tags are legitimate.
        for ctag,(old_name,new_name) in FIX.items():
            en_name=creatures[ctag]['English']
            if en_name and old_name and old_name!=new_name and re.search(r'(?<!\w)'+re.escape(en_name)+r'(?!\w)',eng,re.I) and old_name in new_de:
                new_de=new_de.replace(old_name,new_name); reasons.append(ctag)
        for eng_term,old_term,new_term in TERM_RULES:
            if eng_term.lower() in eng.lower() and old_term in new_de:
                new_de=new_de.replace(old_term,new_term); reasons.append(eng_term)
        for a,b in OVERRIDES.get((p.name,tag),[]):
            if a in new_de: new_de=new_de.replace(a,b)
        if new_de!=old_de: plans.append((p,ri,tag,eng,old_de,new_de,reasons))
EXPECTED=148
if len(plans)!=EXPECTED: raise SystemExit(f'Expected exactly {EXPECTED} validated rows, found {len(plans)}')
allowed={'overworld.csv','bosses.csv','achievements.csv','ui.csv','dialog_story.csv','items.csv','personality.csv','decorations.csv','lore.csv','quests.csv','traits.csv','codex.csv','spells.csv'}
actual={x[0].name for x in plans}
if actual!=allowed: raise SystemExit(f'Unexpected file scope: {sorted(actual)}')
# Verify every planned record still has its exact identity before any write.
for p,ri,tag,eng,old,new,reasons in plans:
    rec=parsed[p][1][ri][0]; header=parsed[p][1][0][0]; ti,ei,gi=header.index('Tag'),header.index('English'),header.index('German')
    if (rec[ti],rec[ei],rec[gi])!=(tag,eng,old): raise SystemExit(f'{p}: record identity changed at {ri}')
byfile={}
for plan in plans: byfile.setdefault(plan[0],[]).append(plan)
for p,pp in byfile.items():
    bomflag,recs,gi=parsed[p]; changes={ri:new for _,ri,tag,eng,old,new,reasons in pp}; chunks=[]
    for ri,(fields,rawrec) in enumerate(recs):
        if ri not in changes: chunks.append(rawrec); continue
        ending='\r\n' if rawrec.endswith('\r\n') else ('\n' if rawrec.endswith('\n') else '')
        fields=list(fields); fields[gi]=changes[ri]; out=io.StringIO(newline=''); csv.writer(out,lineterminator='').writerow(fields); chunks.append(out.getvalue()+ending)
    p.write_bytes((b'\xef\xbb\xbf' if bomflag else b'')+''.join(chunks).encode('utf-8'))
    with p.open(encoding='utf-8-sig',newline='') as f: post=list(csv.reader(f))
    if len(post)!=len(recs): raise SystemExit(f'{p}: record count changed')
print(f'Applied {len(plans)} validated cross-file rows across {len(byfile)} files.')
for p in sorted(byfile,key=lambda x:x.name): print(f'  {p.name}: {len(byfile[p])}')
