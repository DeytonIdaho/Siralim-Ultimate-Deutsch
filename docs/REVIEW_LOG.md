# Prüfprotokoll

Hier werden geprüfte Bereiche und konkrete Übersetzungsentscheidungen dokumentiert.

## Status

- [x] CSV-Struktur geprüft
- [x] Platzhalter-/Tag-Erhalt als Pflicht festgelegt
- [x] Grundglossar erstellt
- [x] Traits vollständig geprüft
- [x] Perks vollständig geprüft
- [x] Spells vollständig geprüft
- [x] Battle/UI-Terminologie geprüft
- [x] Review-Korrekturpakete in den globalen QA-Workflow integriert
- [x] Globaler QA-Endlauf über alle Localization-CSV-Dateien durchgeführt
- [x] Alle verbleibenden automatischen QA-Treffer menschlich klassifiziert: keine bestätigten echten Restfehler
- [ ] Installierbare Override-Dateien erzeugt
- [ ] In-Game-Test auf Steam Deck

## Globaler QA-Endtest

Der Workflow `.github/workflows/translation-qa.yml` wendet die geprüften Korrekturpakete an und erzeugt anschließend für sämtliche Localization-CSV-Dateien neue QA-Queues und Human-Review-Blöcke.

Nach dem finalen Lauf wurden alle verbleibenden automatischen Treffer geprüft. Die Restmeldungen waren Scanner-Fehlalarme, insbesondere:

- dynamische Relikt-Tokens in Achievements (`{RELIC_*}`), die absichtlich sichtbare englische Reliktnamen ersetzen;
- Singular/Plural-Flexionen wie `Spell Gems` → `Zauberstein` nach `Each`;
- kontextgerechte Übersetzungen von `creature(s)` als `Kreatur`, `Kreaturen`, `Wesen` oder `Gegnerwesen`;
- unterschiedliche, aber korrekte Zeilenumbruch-Formatierung;
- wiederholte Condition-Tokens und Prozentangaben, die vom Token-Scanner fälschlich als Mismatch erkannt werden.

Ergebnis: Im globalen End-QA wurde kein bestätigter echter Übersetzungs-, Mechanik-, Zahlen- oder Tagfehler mehr gefunden. Der aktuelle Stand ist damit ein Release-Kandidat; offen bleiben nur Verpackung/Installation und der praktische In-Game-Test.

## Wichtige Übersetzungsentscheidungen

### Reaver

Die Spezialisierung bleibt als `Reaver` erhalten und wird nicht zu `Plünderer` o. Ä. umbenannt. Vorkommen wie `Soul Reaver`, die eigenständige Namen/Traits sind, werden davon getrennt behandelt.

### Celerity / Schnelligkeit

`Celerity` wird konsistent als `Schnelligkeit` geführt. Abweichende Verweise wie `Behändigkeit` wurden in der Endredaktion als Terminologieproblem behandelt.

## Kritische Prüfwörter

Bei der Regelprüfung wurde besonders auf den vollständigen Erhalt folgender Bedeutungen geachtet:

- manually
- additional
- independent
- instead / instead of
- current
- maximum
- missing
- lowest / highest
- before / after
- start / end
- once per turn
- first time
- for each
- based on
- equal to
- prevent
- cannot
- always

## Technische Regeln

Folgende Bestandteile dürfen niemals übersetzt, entfernt oder unkontrolliert verändert werden:

- `{ACTION_*}`
- `{STAT_*}`
- `{CONDNAME_*}`
- `{TIMELINE}` und vergleichbare `{...}`-Tokens
- `<1>`, `<2>`, `<3>` usw.
- `[creature_or_internal_reference]`
- sonstige interne Spiel-Tags
