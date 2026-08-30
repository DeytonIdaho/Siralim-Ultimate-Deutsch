import csv
from pathlib import Path

PATH = Path('vocabulary.csv')
FIXES = {
'L_ARSENALSPELL':'Arsenalzauber','L_BOOZESPELL':'Saufzauber','L_ULTIMATESPELL':'Ultimativzauber','L_REPELLING':'Zauberabwehr','L_MENDING':'Regeneration','L_LEECHING':'Lebensentzug','L_WARDED':'Unbeugsam','L_SPLASHING':'Streuschaden','L_STONE':'Versteinert','L_SLEEPING':'Schlafend','L_SCORNED':'Entmutigt','L_WRITHELINGS':'Writhelinge','L_BRIMFIENDS':'Brim-Unholde','L_GUILD_NATURE':'Naturgilde','L_STATSLOT':'Attribut-Slot','L_TRICKSLOT':'Effekt-Slot','L_TRAITSLOT':'Merkmals-Slot','L_SPELLSLOT':'Zauber-Slot','L_RELIC_SURATHLI_EXT':'Schlichter, Heiliger Schild von Surathli','L_RELIC_AZURAL_EXT':'Wintermaul, Großer Hammer von Azural','L_RELIC_VENEDON':'Dämmerung & Morgenröte','L_RELIC_CALIBAN_EXT':'Essenz der Leere, Dunkles Herz von Caliban','L_RELIC_ARIAMAKI_EXT':'Rippenspalter, Jenseitiger Stab von Ariamaki','L_RELIC_ANNELTHA_EXT':'Gläsern, Kristallauge von Anneltha','L_PERS_BASHFUL':'Gehemmt','L_PERS_TIMID':'Zaghaft','L_ARTMOD_DEATHSTRENGTH':'Todes-Stärke','L_ARTMOD_LIFESTRENGTH':'Lebens-Stärke','L_ARTMOD_NATURESTRENGTH':'Natur-Stärke','L_ARTMOD_SORCERYSTRENGTH':'Zauberei-Stärke','L_ARTMOD_SAVAGEONDAMAGE':'Brutal bei Schaden','L_ARTMOD_WARDEDONDAMAGE':'Unbeugsam bei Schaden','L_ARTMOD_SHELLEDONDAMAGE':'Gepanzert bei Schaden','L_ARTMOD_MENDINGONDAMAGE':'Regeneration bei Schaden','L_ARTMOD_SPLASHINGONDAMAGE':'Streuschaden bei Schaden','L_ARTMOD_REPELLINGONDAMAGE':'Zauberabwehr bei Schaden','L_ARTMOD_PROFICIENTONDAMAGE':'Versiert bei Schaden','L_ARTMOD_SCORNEDONDAMAGE':'Entmutigt bei Schaden','L_ARTMOD_SLEEPONDAMAGE':'Schlafend bei Schaden','L_ARTMOD_STONEONDAMAGE':'Versteinert bei Schaden'}
with PATH.open(encoding='utf-8-sig', newline='') as f:
    reader=csv.DictReader(f); fields=reader.fieldnames; rows=list(reader)
by_tag={r['Tag']:r for r in rows}
missing=[t for t in FIXES if t not in by_tag]
if missing: raise SystemExit(f'Missing tags: {missing}')
for tag,value in FIXES.items(): by_tag[tag]['German']=value
with PATH.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(rows)
# exact post-write verification
with PATH.open(encoding='utf-8',newline='') as f: check={r['Tag']:r['German'] for r in csv.DictReader(f)}
bad={t:(check.get(t),v) for t,v in FIXES.items() if check.get(t)!=v}
if bad: raise SystemExit(f'Verification failed: {bad}')
print(f'Verified {len(FIXES)}/{len(FIXES)} approved vocabulary terms.')
