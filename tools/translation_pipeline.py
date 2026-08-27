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
 out=de or""
 for p,r in [(r"Zauberjuwel","Zauberstein"),(r"Zauber-Edelsteine","Zaubersteine"),(r"Zauber-Edelstein","Zauberstein"),(r"Zauberedelsteine","Zaubersteine"),(r"Zauberedelstein","Zauberstein"),(r"Zaubergems","Zaubersteine"),(r"Zaubergem","Zauberstein"),(r"Zauber-Juwel","Zauberstein")]:out=re.sub(p,r,out)
 if "Trait Material" in en:out=out.replace("Eigenschaftsmaterialien","Merkmalsmaterialien").replace("Eigenschaftsmaterial","Merkmalsmaterial")
 if en.startswith("The most ambitious project was directed by Zonte's master"):out=out.replace("Der ehrgeizigste Projekt","Das ehrgeizigste Projekt")
 # Reviewed perk-language fixes. Keep debatable perk names for the later naming pass.
 perk_exact={
 "After your creatures dodge, they gain <1>% {STAT_defense} for each time they've {ACTION_attacked} with [nature_monk_kaze] Celerity in the current battle.":"Nachdem deine Kreaturen ausweichen, erhalten sie <1>% {STAT_defense} für jedes Mal, das sie im aktuellen Kampf mit [nature_monk_kaze] Schnelligkeit {ACTION_attacked} haben.",
 "Your creatures' attacks cannot be dodged.":"Den Angriffen deiner Kreaturen kann nicht ausgewichen werden.",
 "Your creatures' stat changes persist through death.":"Attributsänderungen deiner Kreaturen bleiben auch nach dem Tod bestehen.",
 "Your creatures' stats are no longer reset after they're killed.":"Die Attribute deiner Kreaturen werden nach ihrem Tod nicht mehr zurückgesetzt.",
 "At the start of battle, your Animatus gains a copy of your fifth creature's innate trait.":"Zu Beginn des Kampfes erhält dein Animatus eine Kopie des angeborenen Merkmals deiner fünften Kreatur.",
 "At the start of battle, your {RACE_Godspawn} creatures gain their respective {RACE_Avatar}'s trait.":"Zu Beginn des Kampfes erhalten deine {RACE_Godspawn}-Kreaturen das Merkmal ihres jeweiligen {RACE_Avatar}s.",
 "The first 3 times your creatures are resurrected, they gain a random trait that belongs to their race.":"Die ersten 3 Male, wenn deine Kreaturen wiederbelebt werden, erhalten sie ein zufälliges Merkmal ihrer Rasse.",
 "You have a 100% increased chance to find Skins. This perk is always active, even if your specialization is not {SPEC_DEPRIVED}.":"Du hast eine um 100% erhöhte Chance, Skins zu finden. Dieser Vorteil ist immer aktiv, auch wenn deine Spezialisierung nicht {SPEC_DEPRIVED} ist.",
 "Your creatures' [slot_trick] Trick Slots that apply buffs and debuffs affect 1 additional creature.":"Die [slot_trick]-Trick-Slots deiner Kreaturen, die Buffs und Debuffs anwenden, betreffen 1 zusätzliche Kreatur.",
 "After your creatures manually {ACTION_cast} an {SPELL_equipment}, they {ACTION_cast} a Living Lance spell. The type of Living Lance spell is based on the caster's class.":"Nachdem deine Kreaturen manuell ein {SPELL_equipment} {ACTION_cast}, {ACTION_cast} sie einen Zauber der Lebenden Lanze. Die Art des Zaubers der Lebenden Lanze richtet sich nach der Klasse des Zauberwirkers.",
 "After start-of-battle effects are determined, your creatures' [temporary] Ethereal {SPELL_alcohol}s gain the 'Chance to Attack', 'Chance to Defend', and 'Chance to Provoke' properties.":"Nachdem die Effekte zu Kampfbeginn bestimmt wurden, erhalten die [temporary] Ätherischen {SPELL_alcohol}s deiner Kreaturen die Eigenschaften 'Chance auf Angriff', 'Chance auf Verteidigung' und 'Chance auf Provokation'.",
 "After your creatures are killed, one of your other creatures casts the top-most [icons,1980]Dark Crystal Spell Gem they have equipped.":"Nachdem eine deiner Kreaturen getötet wurde, wirkt eine deiner anderen Kreaturen den obersten ausgerüsteten [icons,1980]Dunkler-Kristall-Zauberstein.",
 }
 if en in perk_exact:out=perk_exact[en]
 # Safe systematic language cleanup in mechanical perk text.
 if Path(getattr(fix,'current_file','')).stem=='perks':
  out=out.replace("Eure Kreaturen","Deine Kreaturen").replace("eure Kreaturen","deine Kreaturen")
  out=out.replace("Kräutling","Herbling")
  out=out.replace("Statusänderungen","Attributsänderungen")
  out=out.replace("statussteigernden","attributssteigernden")
  out=out.replace("Kreaturen'","Kreaturen")
  out=out.replace("Trickkarten","Trick-Slots")
  # Ultimate gems are still Spell Gems in game terminology.
  if "{SPELL_ultimate}" in en:out=out.replace("Edelsteine","Zaubersteine").replace("Edelstein(e)","Zauberstein(e)").replace("Edelstein","Zauberstein")
  # English Gem references in perk mechanics are spell gems, not generic jewels.
  if re.search(r'\b(?:Spell )?Gems?\b',en):out=out.replace("Edelsteine","Zaubersteine").replace("Edelstein(e)","Zauberstein(e)").replace("Edelstein","Zauberstein")
  out=out.replace("Zauberflickerei","Zauberheilung")
 # Lore repairs retained.
 if en.startswith("At the dawn of civilization, the Amaranths fell from the sky."):
  out='Zu Beginn der Zivilisation fielen die Amaranthe vom Himmel. Yseros eilte zum Ende der Ewigkeit und traf dort Vertraag. "Warst du das?", fragte sie. "Nein", antwortete der Gott der Zeit. Ein Lächeln erschien auf seinem Gesicht. "Es war niemand. Sie waren bereits hier."\\n\\nWenn ein Zauber den Enklaven-Amaranth trifft, prallt ein Teil der Magie von seinem Körper ab und bewegt sich auf den Zaubernden zu. Nach einer Naturkatastrophe findet man häufig Gruppen dieser Wesen, die schweigend die Schäden betrachten.'
 if en.startswith("The Goddess of Earth has multiple 'granddaughters' shaped from the stone and dirt and given life"):
  out="Die Erdgöttin hat mehrere 'Enkelinnen', die aus Stein und Erde geformt und zum Leben erweckt wurden und ihr dabei helfen, das Gleichgewicht in den Verbotenen Tiefen zu bewahren. Obwohl es nur neun von ihnen gibt, ist Thana unter ihnen eine lebende Legende, da sie einen Weg gefunden hat, das Siegel der Verbotenen Tiefen zu umgehen. Von Zeit zu Zeit taucht sie sogar in Vulcanars Reich auf und richtet im Herrschaftsgebiet des Feuergottes Chaos an.\\n\\nAus ferner Vergangenheit gibt es Aufzeichnungen darüber, dass Thana die Oberfläche sogar einmal für kurze Zeit besuchte. Da sie jedoch keine der Sprachen Rodias sprechen kann, hielten die Menschen Thana für ein schreckliches Monster und griffen sie an. Schwer verletzt zog sich Thana in die Verbotenen Tiefen zurück und hegt seither einen tiefen, gewaltsamen Hass auf die Menschheit, dem sie bislang jedoch nicht nachgegeben hat. Das bereitet Anneltha große Sorge, weshalb sie Thana nur jenen anvertraut, von denen sie glaubt, dass sie ihr hoffnungsvollere Sichtweisen vermitteln können."
 if en.startswith("These dragons can emit a flashing light once a day through their horns"):
  out="Diese Drachen können einmal am Tag über ihre Hörner ein blitzendes Licht aussenden, das ihre Feinde für mehrere Sekunden blendet. Sie nutzen diese Fähigkeit häufig, wenn sie umzingelt sind, wodurch ihnen die Flucht gelingt ... meistens jedenfalls. Einige Wesen, etwa Imps, haben gelernt, ihre Augen genau in dem Moment zu schließen, in dem ein Kirin aufblitzt, und verschiedene Strategien perfektioniert, um sie zu fangen. Jeder, selbst ein Imp, weiß, dass das Horn eines Kirins nicht blitzen kann, wenn es vom Körper getrennt wurde. Der Besitz eines solchen Horns verleiht dem Imp-Clan, der es besitzt, jedoch Ansehen. Kirins finden das verständlicherweise nicht amüsant: Selbst wenn sie dabei nie getötet werden und ihre Hörner nachwachsen, leiden sie beim Fang und bei der Entfernung der Hörner. Deshalb haben sie begonnen, nachts Häuser der Imps zu zerstören und die gestohlenen Hörner mit ihren Hufen zu zertrümmern – als Rache und Warnung."
 return out

def narrative_file(path):return Path(path).stem in {"personality","dialog","dialog_story","lore"}
def exception(path,en,term):
 stem=Path(path).stem
 if narrative_file(path) and term in("Creature","Creatures"):
  mechanical=(en.startswith("This creature has already used 15 scrolls.") or en.startswith("You can now Transmogrify your character") or en.startswith("You should bring along at least one creature before using the Teleportation Shrine.") or en.startswith("Nortah:\\nYou can return to the Menagerie"))
  return not mechanical
 if stem=="personality" and term in("Trait","Traits") and en=="(It seems to be excessively confident in itself. Always a good trait to have in a creature.)":return True
 if stem=="lore" and term in("Trait","Traits") and "Trait Material" not in en:return True
 return False
def false_token(en):return en.startswith("A random enemy recovers a large amount of {STAT_health}")
def main():
 ap=argparse.ArgumentParser();ap.add_argument("csv_file");ap.add_argument("--out",required=True);ap.add_argument("--chunk-size",type=int,default=100);ap.add_argument("--apply-safe-fixes",action="store_true");ap.add_argument("--fixed-file");a=ap.parse_args();o=Path(a.out);o.mkdir(parents=True,exist_ok=True);fix.current_file=a.csv_file
 with open(a.csv_file,encoding="utf-8-sig",newline="")as f:rd=csv.DictReader(f);fs=rd.fieldnames or[];ec,dc=cols(fs);rows=list(rd)
 if a.apply_safe_fixes:
  for r in rows:r[dc]=fix(r.get(ec,""),r.get(dc,""))
  with Path(a.fixed_file or a.csv_file).open("w",encoding="utf-8",newline="")as f:w=csv.DictWriter(f,fieldnames=fs);w.writeheader();w.writerows(rows)
 found=[]
 for i,r in enumerate(rows,2):
  en,de=norm(r.get(ec)),norm(r.get(dc));issues=[]
  if en and not de:issues.append("MISSING_TRANSLATION")
  if toks(en)!=toks(de) and not false_token(en):issues.append("TOKEN_MISMATCH")
  for term,want in TERMS.items():
   if term in("Trait","Traits")and re.search(r"\bpropert(?:y|ies)\b",en,re.I):continue
   if exception(a.csv_file,en,term):continue
   if re.search(r"\b"+re.escape(term)+r"\b",en,re.I)and want.lower()not in de.lower():issues.append(f"TERM:{term}->{want}")
  if issues:found.append((i,en,de,"; ".join(issues)))
 h=["line","english","german","issues","reviewed","replacement"]
 for n,s in enumerate(range(0,len(found),a.chunk_size),1):
  with(o/f"review_{n:03d}.csv").open("w",encoding="utf-8",newline="")as f:w=csv.writer(f);w.writerow(h);[w.writerow([ln,en,de,iss,"",""])for ln,en,de,iss in found[s:s+a.chunk_size]]
 (o/"SUMMARY.md").write_text(f"# Translation QA summary\n\n- Source: `{a.csv_file}`\n- Rows: {len(rows)}\n- Flagged: {len(found)}\n- Chunk size: {a.chunk_size}\n- Review files: {(len(found)+a.chunk_size-1)//a.chunk_size}\n",encoding="utf-8")
if __name__=="__main__":main()
