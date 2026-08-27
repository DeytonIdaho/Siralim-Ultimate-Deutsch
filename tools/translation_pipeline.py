#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,re
from collections import Counter
from pathlib import Path
TOKEN_RE=re.compile(r"(?:\{[^{}]+\}|\[[^\[\]]+\]|<[^<>]+>|%\w|\\n)")
TERMS={"Creature":"Kreatur","Creatures":"Kreaturen","Trait":"Merkmal","Traits":"Merkmale","Minion":"Diener","Spell Gem":"Zauberstein","Spell Gems":"Zaubersteine"}
def norm(s):return(s or"").strip()
def toks(s):return Counter(TOKEN_RE.findall(s or""))
def cols(fs):
 low={f.lower():f for f in fs}
 def p(ns):
  for n in ns:
   if n in low:return low[n]
 a=p(["english","en","source","original","text_en","description_en"]);b=p(["german","de","deutsch","translation","text_de","description_de"])
 if not a or not b:raise SystemExit("EN/DE columns not found")
 return a,b
def fix(en,de):
 out=de or"";stem=Path(getattr(fix,'current_file','')).stem
 for p,r in [(r"Zauberjuwel","Zauberstein"),(r"Zauber-Edelsteine","Zaubersteine"),(r"Zauber-Edelstein","Zauberstein"),(r"Zauberedelsteine","Zaubersteine"),(r"Zauberedelstein","Zauberstein"),(r"Zaubergems","Zaubersteine"),(r"Zaubergem","Zauberstein"),(r"Zauber-Juwel","Zauberstein")]:out=re.sub(p,r,out)
 if "Trait Material" in en:out=out.replace("Eigenschaftsmaterialien","Merkmalsmaterialien").replace("Eigenschaftsmaterial","Merkmalsmaterial").replace("Eigenschaftsmaterie","Merkmalsmaterial").replace("Merkmalsmaterie","Merkmalsmaterial")
 if stem in {'ui','vocabulary'}:
  if re.search(r'\bTraits?\b',en):out=out.replace('Eigenschaft(en)','Merkmal(e)').replace('Eigenschaftsgewinne','Merkmalsgewinne').replace('Eigenschaftsdetails','Merkmalsdetails').replace('Eigenschaftsplatz','Merkmalsplatz').replace('Eigenschaften','Merkmale').replace('Eigenschaft','Merkmal')
  if re.search(r'\bSpell Gems?\b',en):out=out.replace('Zauberstein-Platz/Plätze','Zaubersteinplatz/-plätze').replace('Zauberstein-Plätze','Zaubersteinplätze').replace('Edelsteine','Zaubersteine').replace('Edelstein','Zauberstein')
  # Resource and currency standard. Only replace when the English source explicitly names the currency/resource.
  resource_terms={'Brimstone':'Schwefel','Crystal':'Kristall','Essence':'Essenz','Granite':'Granit','Power':'Kraft','Favor':'Gunst','Glory':'Ruhm','Notoriety':'Berüchtigtheit','Piety':'Frömmigkeit','Stardust':'Sternenstaub','Glamour':'Glamour','Emblem':'Emblem','Mana':'Mana'}
  for src,want in resource_terms.items():
   if re.search(r'\b'+re.escape(src)+r'\b',en,re.I):
    # Repair known machine-translated resource names without touching unrelated uses of words such as power.
    bad={'Brimstone':['Brimstone'],'Crystal':['Crystal'],'Essence':['Essence'],'Granite':['Granite'],'Power':['Power'],'Favor':['Favor'],'Glory':['Glory'],'Notoriety':['Notoriety'],'Piety':['Piety'],'Stardust':['Stardust'],'Glamour':['Glamour']}.get(src,[])
    for b in bad:out=re.sub(r'\b'+re.escape(b)+r'\b',want,out,flags=re.I)
  # Reviewed specialization section.
  if en.startswith('Perseverance, an iron will, and a touch of insanity are the perfect recipe for victory.'):
   out='Ausdauer, ein eiserner Wille und ein Hauch von Wahnsinn sind das perfekte Rezept für den Sieg. Reaver leben nach diesem Mantra und erfüllen ihre Kreaturen mit kaltem, berechnendem Zorn. Dadurch werden sie im Verlauf des Kampfes immer mächtiger, während ihre Feinde zunehmend ermüden.'
  if en.startswith("Many people foolishly mistake a Druid's introversion for weakness."):
   out='Viele halten die Zurückgezogenheit eines Druiden törichterweise für Schwäche. Diese Magier sind überzeugt, dass auf dem Schlachtfeld Qualität stets über Quantität siegt. Entgegen der Tradition sieht man sie häufig mit weniger als sechs Kreaturen. Doch wenn druidische Magie ihre kleine Truppe verstärkt, ist die Verwüstung, die sie anrichtet, beeindruckend.'
  if en.startswith("The Engineer's sole purpose in life is to build a bigger and better explosive than last time."):
   out='Der einzige Lebenszweck des Ingenieurs besteht darin, eine noch größere und bessere Sprengladung als die letzte zu bauen. Dieser bombastische Bombardier befestigt Bomben an seinen Gegnern und sprengt sie mit gewaltiger Wucht davon.'
  if en.startswith('The Deprived was born with nothing and will die with nothing.'):
   out='Der Entbehrte wurde mit nichts geboren und wird mit nichts sterben. Verflucht mit der Intelligenz eines Schwamms und dem Körperbau eines kränklichen Kindes muss der Entbehrte mit dem Wenigen auskommen, das ihm das Schicksal gelassen hat.'
  if en.startswith("As a Deprived, you'll lose access to your most significant sources of power"):
   out='Als Entbehrter verlierst du den Zugang zu deinen wichtigsten Machtquellen, darunter Merkmale aus Fusionen, Avatar-Kreaturen und Relikteffekte. Dies ist eine Herausforderungsspezialisierung und erscheint nach dem Freischalten nicht im Kelch der Prüfungen.'
  if en.startswith("As a Monk, you'll boost your creatures' chance to Dodge attacks and spells."):
   out='Als Mönch erhöhst du die Chance deiner Kreaturen, Angriffen und Zaubern auszuweichen. Wenn deine Kreaturen ausweichen, führen sie einen verheerenden Gegenangriff gegen den Feind aus.'
  if en=='Innate Trait:':out='Angeborenes Merkmal:'
  if en=='Fused Trait:':out='Fusionsmerkmal:'
  if 'Reaver' in en:out=re.sub(r'\bPlünderer\b','Reaver',out)
  # Reviewed relic section.
  relic_effect=('relic' in en.lower() or 'bearer' in en.lower()) and not en.startswith('You can now take on ')
  if relic_effect:
   out=out.replace('Reliquien','Relikte').replace('Reliquie','Relikt')
   out=out.replace('Statuswert-steigernde','attributssteigernde').replace('Statuswerte steigernde','attributssteigernde').replace('Statuswert-steigernden','attributssteigernden').replace('Statuswerte','Attribute').replace('Statuswert','Attribut')
   out=out.replace('Attribut-steigernde','attributssteigernde').replace('Attribut-steigernden','attributssteigernden').replace('für jedes Mal, das ','für jedes Mal, wenn ')
  # Realm bonus / late UI cleanup discovered by full human review.
  if re.search(r'\bStat (?:Boost|Reduction|Boosts)\b|Enemies\' Stats|Random Stat Boost|All Stats Boost',en):
   out=out.replace('Statuswertreduzierung','Attributssenkung').replace('Statusreduktion','Attributssenkung').replace('Statuswerte-Verstärkungen','Attributsboni').replace('Statusboosts','Attributsboni').replace('Statusboost','Attributsbonus').replace('Werte der Gegner','Attribute der Gegner').replace('Gegner-Werte','Attribute der Gegner')
  out=out.replace('Portalsbossen','Portalbossen').replace('Portal-Bosse','Portalbosse').replace('Portalbosse','Portalbosse')
  out=out.replace('Schatztrolle','Schatzgolems').replace('Knochenhaufen Gewähren','Schädelhaufen gewähren').replace('Kloß','Knödel').replace('Teigtaschen','Knödel')
  # Normalize obvious English title-case leakage in short realm bonus strings.
  for a,b in [(' Gewähren ',' gewähren '),(' Gewährt ',' gewährt '),(' Verringern ',' verringern '),(' Reduzieren ',' reduzieren '),(' Töten ',' töten '),(' Tötet ',' tötet '),(' Lassen ',' lassen '),(' Fallen',' fallen'),(' Füllen ',' füllen '),(' Manchmal ',' manchmal '),(' Nach',' nach'),(' Schaden ',' schaden '),(' Beschwören ',' beschwören '),(' Fliehen ',' fliehen '),(' Niemals',' niemals'),(' Nie',' nie')]:out=out.replace(a,b)
  exact={
   "You don't have Rank S knowledge with any creatures.":'Du hast für keine Kreatur Wissen auf Rang S.',
   'Relics Grant Crystal':'Relikte gewähren Kristall',
   'Pineapples Grant Brimstone':'Ananas gewähren Schwefel',
   'Fruit of Life Grants Power':'Frucht des Lebens gewährt Kraft',
   'Traps Grant Essence':'Fallen gewähren Essenz',
   'Tithes Grant Granite':'Zehnten gewähren Granit',
   'Arbiter Robes Drop Treasure':'Richterroben lassen Schätze fallen',
   'Fae Drop Treasure':'Fae lassen Schätze fallen',
   'Creature has additional Spell Gem slots.':'Kreatur hat zusätzliche Zaubersteinplätze.',
   'Source:':'Quelle:',
   'Move Gem to Another Slot':'Zauberstein in einen anderen Platz verschieben',
   'Casting Sound Effect':'Zauber-Soundeffekt',
   'History (Battle)':'Kampfchronik',
   'Menagerie Duel Settings':'Menagerie-Duell-Einstellungen',
   'This option randomizes the creatures found in realms.':'Diese Option bestimmt die Kreaturen, die du in den Reichen findest, zufällig.',
   'This option allows you to adjust the game\'s difficulty.\n\n"Ruthless" significantly increases the difficulty of enemies and makes it more difficult to acquire resources, experience points, items, and more.\n\n"Relaxed" is the exact opposite.':'Mit dieser Option kannst du den Schwierigkeitsgrad des Spiels anpassen.\n\n„Unbarmherzig“ erhöht die Stärke der Gegner deutlich und erschwert es, Ressourcen, Erfahrungspunkte, Gegenstände und mehr zu erhalten.\n\n„Entspannt“ bewirkt das genaue Gegenteil.',
   'This option makes it so you can only visit each Realm Depth once. In addition, if your party is wiped out, you will never be able to use the Teleportation Shrine again (in other words, it\'s game over).\n\nEnabling this mode automatically enables Skip Story Mode, so make sure you read about that mode before proceeding.':'Mit dieser Option kannst du jede Reichtiefe nur einmal besuchen. Wird deine Gruppe vollständig besiegt, kannst du den Teleportationsschrein danach nicht mehr benutzen – das Spiel ist damit beendet.\n\nDieser Modus aktiviert automatisch „Story-Modus überspringen“. Lies dir die Beschreibung dieses Modus durch, bevor du fortfährst.',
   'This option allows you to start the game with almost everything unlocked, as well as some cheats enabled. This mode is ideal for testing purposes.\n\nEnabling this mode automatically enables Skip Story Mode, so make sure you read about that mode before proceeding.':'Mit dieser Option startest du das Spiel mit fast allen freigeschalteten Inhalten und einigen aktivierten Cheats. Dieser Modus eignet sich besonders für Testzwecke.\n\nDieser Modus aktiviert automatisch „Story-Modus überspringen“. Lies dir die Beschreibung dieses Modus durch, bevor du fortfährst.',
   'You can forcefully forfeit the battle at any time by holding {KEYQ}, {KEYE}, and {KEYF} for a few seconds.':'Du kannst einen Kampf jederzeit sofort aufgeben, indem du {KEYQ}, {KEYE} und {KEYF} einige Sekunden lang gedrückt hältst.',
  }
  if en in exact:out=exact[en]
 return out

def narrative_file(path):return Path(path).stem in {'personality','dialog','dialog_story','lore','bosses'}
def exception(path,en,term):
 stem=Path(path).stem
 if narrative_file(path) and term in('Creature','Creatures'):return True
 if stem=='ui' and en=="You don't have Rank S knowledge with any creatures." and term=='Creatures':return True
 if stem=='personality' and term in('Trait','Traits'):return True
 if stem=='lore' and term in('Trait','Traits') and 'Trait Material' not in en:return True
 return False
def false_token(en):return en.startswith('A random enemy recovers a large amount of {STAT_health}') or en.startswith('{CONDNAME_DEBUFF_CONFUSED} creatures have a 50% chance') or en.startswith('Creatures that are resistant to {CONDNAME_DEBUFF_FROZEN}') or en=='[[Macro Editor]' or en.startswith('The bearer has a 100% chance to avoid damage')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('csv_file');ap.add_argument('--out',required=True);ap.add_argument('--chunk-size',type=int,default=100);ap.add_argument('--apply-safe-fixes',action='store_true');ap.add_argument('--fixed-file');a=ap.parse_args();o=Path(a.out);o.mkdir(parents=True,exist_ok=True);fix.current_file=a.csv_file
 with open(a.csv_file,encoding='utf-8-sig',newline='')as f:rd=csv.DictReader(f);fs=rd.fieldnames or[];ec,dc=cols(fs);rows=list(rd)
 if a.apply_safe_fixes:
  for r in rows:r[dc]=fix(r.get(ec,''),r.get(dc,''))
  with Path(a.fixed_file or a.csv_file).open('w',encoding='utf-8',newline='')as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 found=[]
 for i,r in enumerate(rows,2):
  en,de=norm(r.get(ec)),norm(r.get(dc));issues=[]
  if en and not de:issues.append('MISSING_TRANSLATION')
  if toks(en)!=toks(de) and not false_token(en):issues.append('TOKEN_MISMATCH')
  for term,want in TERMS.items():
   if term in('Trait','Traits')and re.search(r'\bpropert(?:y|ies)\b',en,re.I):continue
   if exception(a.csv_file,en,term):continue
   if re.search(r'\b'+re.escape(term)+r'\b',en,re.I)and want.lower()not in de.lower():issues.append(f'TERM:{term}->{want}')
  if issues:found.append((i,en,de,'; '.join(issues)))
 h=['line','english','german','issues','reviewed','replacement']
 for n,s in enumerate(range(0,len(found),a.chunk_size),1):
  with(o/f'review_{n:03d}.csv').open('w',encoding='utf-8',newline='')as f:w=csv.writer(f);w.writerow(h);[w.writerow([ln,en,de,iss,'',''])for ln,en,de,iss in found[s:s+a.chunk_size]]
 (o/'SUMMARY.md').write_text(f'# Translation QA summary\n\n- Source: `{a.csv_file}`\n- Rows: {len(rows)}\n- Flagged: {len(found)}\n- Chunk size: {a.chunk_size}\n- Review files: {(len(found)+a.chunk_size-1)//a.chunk_size}\n',encoding='utf-8')
if __name__=='__main__':main()
