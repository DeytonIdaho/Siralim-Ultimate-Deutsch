#!/usr/bin/env python3
from pathlib import Path
import csv, io, re

SPELL_UI = {
'L_MENU_BTEXT_GEMS','L_MENU_EQUIP_GEM','L_MENU_ITEM_ARTIFACT_NOSPELL','L_GEMCRAFT_TITLE','L_GEMCRAFT_CURRENT','L_GEMCRAFT_NO_RESOURCES','L_GEMMOD_TITLE','L_GEMMOD_DISENCHANT_GEM','L_GEMMOD_UPGRADE_COST','L_GEMMOD_NO_RESOURCES','L_GEMMOD_MAXED','L_GEMMOD_INCOMPATIBLE','L_GEMMOD_NO_MATS','L_GEMMOD_NO_PROPERTIES','L_GEMUPGRADE_NO_RESOURCES','L_GEMMOD_UPGRADE_ENCHANTER','L_GEMMOD_TIER_MAXED','L_REALM_NOGEMGAIN','L_REALM_SEALAFTERCAST','L_MACRO_PROCESS_GEM_NOT_FOUND','L_MACRO_PROCESS_CANT_CAST_TRAIT','L_MACRO_PROCESS_CANT_CAST_GEM','L_MACRO_PROCESS_CANT_CAST_BOOZE','L_MACRO_PROCESS_NO_GEMS_FOUND'}
DIRECT = {
('dialog_story.csv','L_D_BLACKSMITH_D7'): ('Statusplätze','Attributslots'),
('traits.csv','L_TRAIT_DESC_IMBUE'): ('Die Statusplätze [slot_stat] deiner Kreaturen bieten 15% mehr Nutzen.','Die [slot_stat]-Attributslots deiner Kreaturen gewähren 15% mehr Nutzen.'),
('traits.csv','L_TRAIT_DESC_WARCRAFT'): ("Dieser Kreatur's [slot_stat] Statusplätze gewähren 40% mehr Nutzen.",'Die [slot_stat]-Attributslots dieser Kreatur gewähren 40% mehr Nutzen.'),
('traits.csv','L_TRAIT_DESC_LOSTINFOREVER'): ("Dieser Kreatur's Effekte",'Die Effekte dieser Kreatur'),
('traits.csv','L_TRAIT_DESC_TRUENORTH'): ("Dieser Kreatur's Effekte",'Die Effekte dieser Kreatur'),
('codex.csv','L_CODD_ARTIFACTS_INTRODUCTION'): ('Statusboni','Attributboni'),
('codex.csv','L_CODD_RELICS_RELIQUARY_UPGRADES'): ('Statusboni','Attributboni'),
('ui.csv','L_RELIQUARY_COST'): ('Kosten für aufwertung','Kosten für Aufwertung'),
('ui.csv','L_RELIQUARY_BONUS_DESC7'): ('Statusboni','Attributboni'),
('ui.csv','L_PERK_TITLE'): ('Wähle einen Talent zum aufwerten.','Wähle ein Talent zum Aufwerten.'),
('spells.csv','L_SD_ANGER'): ("Zielkreatur's {STAT_attack} wird gleich ihrem {STAT_intelligence} gesetzt.",'Das {STAT_attack}-Attribut der Zielkreatur wird auf ihr {STAT_intelligence}-Attribut gesetzt.'),
('spells.csv','L_SD_HALFWAYTHROUGH'): ("Ziel's {STAT_health} wird auf 50% gesetzt.",'Die {STAT_health} des Ziels wird auf 50% gesetzt.'),
('spells.csv','L_SD_GEMGAMBLE'): ("Ziel's {STAT_charges} werden entweder auf 0% oder 100% gesetzt.",'Die {STAT_charges} des Ziels werden entweder auf 0% oder 100% gesetzt.'),
('overworld.csv','L_OW_ANOINTMENTORB28'): ('Zauberstatistik-Modifikation','Zauberattribut-Modifikation'),
('battle.csv','L_X_CHARGES_CLASS'): ('Edelsteine','Zaubersteine'),
('items.csv','L_ID_GEM_CRAFT_DESC'): ('Edelsteine','Zaubersteine'),
('bosses.csv','L_D_BOSS_ANIMATION_2'): ('körperlosen Wesensteils','körperlosen Kreaturenteils'),
}
SEXT={'L_ACH_DESC_127','L_ACH_DESC_137','L_ACH_DESC_147','L_ACH_DESC_157'}
NUMWORDS={'billion':'Milliarde','trillion':'Billion','quadrillion':'Billiarde','quintillion':'Trillion','sextillion':'Trilliarde','septillion':'Quadrillion','octillion':'Quadrilliarde'}

def records(text):
    lines=text.splitlines(keepends=True); rd=csv.reader(io.StringIO(text,newline='')); out=[]; prev=0
    for row in rd:
        end=rd.line_num; out.append((row,''.join(lines[prev:end]))); prev=end
    if prev!=len(lines): raise SystemExit('physical-line accounting mismatch')
    return out

def achievement_text(eng):
    m=re.fullmatch(r'(Increase|Decrease) the (\{STAT_[^}]+\}) stat by a total of (.+) points in battle\.',eng)
    if not m: raise SystemExit(f'Unexpected achievement source: {eng}')
    verb='Erhöhe' if m.group(1)=='Increase' else 'Verringere'; amount=m.group(3)
    if amount.startswith('1 '):
        word=amount[2:]
        if word in NUMWORDS: amount='1 '+NUMWORDS[word]
    amount=re.sub(r'(?<=\d),(?=\d{3}\b)', '.', amount)
    return f'{verb} {m.group(2)} im Kampf um insgesamt {amount} Punkte.'

def transform(fn,tag,eng,de):
    new=de
    key=(fn,tag)
    if key in DIRECT:
        a,b=DIRECT[key]
        if a not in new: raise SystemExit(f'{fn}/{tag}: expected old fragment missing: {a!r}')
        new=new.replace(a,b)
    if fn=='ui.csv' and tag in SPELL_UI:
        if 'Edelstein' not in new: raise SystemExit(f'{fn}/{tag}: expected Edelstein missing')
        new=new.replace('Edelsteine','Zaubersteine').replace('Edelstein','Zauberstein')
        if tag=='L_GEMMOD_UPGRADE_COST': new=new.replace('zum aufwerten','zum Aufwerten')
    if fn=='achievements.csv':
        n=int(tag.rsplit('_',1)[1]) if tag.startswith('L_ACH_DESC_') and tag.rsplit('_',1)[1].isdigit() else -1
        if 160<=n<=259: new=achievement_text(eng)
        elif tag in SEXT:
            if 'sextillion' not in eng.lower(): raise SystemExit(f'{tag}: expected sextillion source')
            new=re.sub(r'1\s+(?:Sextillion|Trillion)', '1 Trilliarde', new)
        new=re.sub(r'(?<=\d),(?=\d{3}\b)', '.', new)
    return new

files=['achievements.csv','battle.csv','bosses.csv','codex.csv','dialog_story.csv','items.csv','overworld.csv','spells.csv','traits.csv','ui.csv']
changed=[]
for fn in files:
    p=Path(fn); raw=p.read_bytes(); bom=raw.startswith(b'\xef\xbb\xbf'); text=(raw[3:] if bom else raw).decode('utf-8'); recs=records(text)
    hdr=recs[0][0]; ti,ei,gi=[hdr.index(x) for x in ('Tag','English','German')]; chunks=[]
    for idx,(row,rawrec) in enumerate(recs):
        if idx==0: chunks.append(rawrec); continue
        if len(row)!=len(hdr): raise SystemExit(f'{fn}: malformed record {idx}')
        tag,eng,de=row[ti],row[ei],row[gi]; new=transform(fn,tag,eng,de)
        if new==de: chunks.append(rawrec); continue
        ending='\r\n' if rawrec.endswith('\r\n') else ('\n' if rawrec.endswith('\n') else '')
        row=list(row); row[gi]=new; s=io.StringIO(newline=''); csv.writer(s,lineterminator='').writerow(row); chunks.append(s.getvalue()+ending)
        changed.append((fn,tag,de,new))
    p.write_bytes((b'\xef\xbb\xbf' if bom else b'')+''.join(chunks).encode('utf-8'))

expected=179
if len(changed)!=expected:
    raise SystemExit(f'Expected {expected} changed records, found {len(changed)}')
by={}
for fn,*_ in changed: by[fn]=by.get(fn,0)+1
print(f'Applied {len(changed)} reviewed QA records across {len(by)} files.')
for fn in sorted(by): print(f'  {fn}: {by[fn]}')
