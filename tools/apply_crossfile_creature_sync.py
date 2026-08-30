#!/usr/bin/env python3
from pathlib import Path
import base64,csv,io,json,re,zlib

# Load the 232 reviewed old->new creature-name decisions.
parts=[Path(f'tools/creature_name_fixes_20260830_{i}.dat').read_text(encoding='ascii').strip() for i in (1,2,3)]
FIX={t:(o,n) for t,o,n in json.loads(zlib.decompress(base64.b64decode(''.join(parts))))}
if len(FIX)!=232: raise SystemExit(f'Unexpected creature patch size: {len(FIX)}')

# Current creatures.csv supplies the English source names and the already-reviewed new German names.
with open('creatures.csv',encoding='utf-8-sig',newline='') as f:
    creatures={r['Tag']:r for r in csv.DictReader(f)}
if len(creatures)!=1612: raise SystemExit(f'Unexpected creatures row count: {len(creatures)}')
for tag,(old,new) in FIX.items():
    if tag not in creatures: raise SystemExit('Missing creature tag '+tag)
    if creatures[tag]['German']!=new: raise SystemExit(f'creatures.csv not at reviewed state for {tag}')

# Small, independently confirmed terminology fixes found during the same pass.
TERM_RULES=[
    ('Spell Gem','Edelsteine','Zaubersteine'),
    ('Spell Gem','Edelstein','Zauberstein'),
    ('Stat Slot','Statusplatz','Attributslot'),
]

# Grammar/case overrides required after a literal creature-name synchronization.
OVERRIDES={
 ('bosses.csv','L_D_BOSS_COCKATRICE_2'):[('der Kokatrice','die Kokatrice'),('Seinem Charakter treu','Ihrem Charakter treu'),('sobald er dich sieht','sobald sie dich sieht')],
 ('bosses.csv','L_D_BOSS_COCKATRICE_3'):[('der Kokatrice','die Kokatrice')],
 ('bosses.csv','L_D_BOSS_NIX_3'):[('Der Nixe','Die Nixe'),('der es geworfen hat','die es geworfen hat')],
 ('items.csv','L_MAT_SIGILOFTHENIX'):[('des Nixe','der Nixe')],
 ('items.csv','L_MAT_SIGILOFTHECOCKATRICE'):[('der Kokatrice','der Kokatrice')],
 ('ui.csv','L_BLESS_MUSE_3'):[('Erwecktsstatuen','Statuen der Erweckten')],
 ('personality.csv','L_D_PERS_SPEED_ANIMATION'):[('Erweckts','Erweckten')],
 ('decorations.csv','L_DEC_ASTRALGALLERYANIMATIONSTATUE'):[('Erwecktsstatue','Statue der Erweckten')],
}

# Work only on root localization CSVs. creatures.csv is already authoritative; battle.csv was patched in the prior workflow.
files=sorted(p for p in Path('.').glob('*.csv') if p.name not in {'creatures.csv','battle.csv','TERMINOLOGIE.csv'})
plans=[]
for p in files:
    raw=p.read_bytes(); bom=raw.startswith(b'\xef\xbb\xbf'); body=raw[3:] if bom else raw
    text=body.decode('utf-8'); lines=text.splitlines(keepends=True)
    # This patch intentionally refuses multiline physical CSV records so only one physical record is ever rewritten.
    try: rows=list(csv.DictReader(io.StringIO(text)))
    except Exception as e: raise SystemExit(f'{p}: CSV parse failed: {e}')
    if not rows or 'German' not in rows[0] or 'English' not in rows[0] or 'Tag' not in rows[0]: continue
    if len(lines)!=len(rows)+1: raise SystemExit(f'{p}: multiline CSV records detected; refusing automatic patch')
    header=next(csv.reader([lines[0].rstrip('\r\n')]))
    ti,ei,gi=header.index('Tag'),header.index('English'),header.index('German')
    seen=set()
    for i,line in enumerate(lines[1:],1):
        ending='\r\n' if line.endswith('\r\n') else ('\n' if line.endswith('\n') else '')
        core=line[:-len(ending)] if ending else line
        fields=next(csv.reader([core])); tag=fields[ti]; eng=fields[ei]; old_de=fields[gi]; new_de=old_de; reasons=[]
        if tag in seen: raise SystemExit(f'{p}: duplicate tag {tag}')
        seen.add(tag)
        # Synchronize only when the exact English creature name appears as a complete term in the English source row.
        for ctag,(old_name,new_name) in FIX.items():
            en_name=creatures[ctag]['English']
            if not en_name or not old_name or old_name==new_name: continue
            if re.search(r'(?<!\\w)'+re.escape(en_name)+r'(?!\\w)',eng,re.I) and old_name in new_de:
                new_de=new_de.replace(old_name,new_name); reasons.append(ctag)
        # Confirmed terminology leftovers.
        for eng_term,old_term,new_term in TERM_RULES:
            if eng_term.lower() in eng.lower() and old_term in new_de:
                new_de=new_de.replace(old_term,new_term); reasons.append(eng_term)
        # Apply only explicit grammar overrides for known generated forms.
        for a,b in OVERRIDES.get((p.name,tag),[]):
            if a in new_de: new_de=new_de.replace(a,b)
        if new_de!=old_de:
            plans.append((p,i,tag,old_de,new_de,reasons,fields,ending,gi))

EXPECTED=148
if len(plans)!=EXPECTED:
    raise SystemExit(f'Expected exactly {EXPECTED} validated rows, found {len(plans)}')
allowed={'overworld.csv','bosses.csv','achievements.csv','ui.csv','dialog_story.csv','items.csv','personality.csv','decorations.csv','lore.csv','quests.csv','traits.csv','codex.csv','spells.csv'}
actual={x[0].name for x in plans}
if actual!=allowed: raise SystemExit(f'Unexpected file scope: {sorted(actual)}')

# PREVALIDATION COMPLETE. Nothing has been written above this line.
byfile={}
for plan in plans: byfile.setdefault(plan[0],[]).append(plan)
for p,pp in byfile.items():
    raw=p.read_bytes(); bom=b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''; body=raw[len(bom):].decode('utf-8'); lines=body.splitlines(keepends=True)
    for _,i,tag,old_de,new_de,reasons,fields,ending,gi in pp:
        fields[gi]=new_de
        out=io.StringIO(newline=''); csv.writer(out,lineterminator='').writerow(fields)
        lines[i]=out.getvalue()+ending
    p.write_bytes(bom+''.join(lines).encode('utf-8'))
    with p.open(encoding='utf-8-sig',newline='') as f: list(csv.DictReader(f))

print(f'Applied {len(plans)} validated cross-file rows across {len(byfile)} files.')
for p in sorted(byfile,key=lambda x:x.name): print(f'  {p.name}: {len(byfile[p])}')
