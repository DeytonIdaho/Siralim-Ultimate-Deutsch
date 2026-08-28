# Siralim Ultimate – Deutsche Community-Übersetzung

Inoffizielle deutsche Community-Überarbeitung der Lokalisierung von **Siralim Ultimate** mit Schwerpunkt auf verständlichen, konsistenten und spielmechanisch korrekten Texten.

## Status

**Übersetzung und globaler QA-Durchlauf sind abgeschlossen. Der aktuelle Stand ist bereit für den Ingame-Test.**

Der finale Konsistenztest umfasste 37.568 Lokalisierungszeilen. Nach Prüfung und Bereinigung der bekannten Sonderfälle verblieben keine ungeklärten Dubletten, Tokenfehler, Zahlen-/Prozentabweichungen oder Ausreißer bei den zentralen Begriffen Buff, Debuff, Diener und Talent.

Die Übersetzung ist trotzdem ein Community-Projekt. Fehler, unglückliche Formulierungen oder Probleme, die erst im Spielkontext sichtbar werden, können weiterhin vorkommen. Der nächste Schritt ist daher der praktische Ingame-Test.

## Download

Für einen Test kann der aktuelle Stand dieses Repository-Branches als ZIP heruntergeladen werden:

1. Auf GitHub den Branch **`translation-work`** auswählen.
2. **Code → Download ZIP** wählen.
3. Das ZIP entpacken.
4. Für die Installation werden nur die `.csv`-Lokalisierungsdateien aus dem Hauptverzeichnis benötigt.

Die Entwicklungs- und QA-Ordner wie `.github`, `review`, `consistency_review`, `tools` und `docs` gehören **nicht** in den Spielordner.

## Installation in Siralim Ultimate

Seit Siralim Ultimate 2.0 unterstützt die Steam-Version Localization Overrides.

1. In Steam Rechtsklick auf **Siralim Ultimate** → **Eigenschaften** → **Installierte Dateien** → **Durchsuchen**.
2. Im Installationsverzeichnis einen Ordner mit exakt diesem Namen erstellen:

   `localization_override`

3. Die `.csv`-Dateien aus dem Hauptverzeichnis dieses Projekts direkt in `localization_override` kopieren.
4. Siralim Ultimate starten und Deutsch als Sprache verwenden.

Die CSV-Dateien behalten das Format der Originaldateien aus dem Spielordner `localization` bei. Passende Einträge aus `localization_override` überschreiben automatisch die Originaltexte.

**Wichtig:** Der Ordner muss exakt `localization_override` heißen. Laut Thylacine Studios kann ein anders benannter Override-Ordner bei einem Steam-Update gelöscht werden.

Offizielle Anleitung von Thylacine Studios:  
https://www.thylacinestudios.com/blog/siralim-ultimate-2-0-localization-override-instructions

## Was wurde überarbeitet?

Der Schwerpunkt lag auf spielmechanisch relevanten Texten und projektweiter Konsistenz, insbesondere:

- Traits und komplexe Regeltexte
- Talente (engl. Perks) und Spezialisierungen
- Zauber und Zaubersteine
- Buffs und Debuffs
- Diener (engl. Minions)
- Kreaturen- und Rassennamen
- Attribute, Lebenspunkte, Ladungen und Prozentwerte
- Trigger und Timing wie `before`, `after`, `start of turn` und `end of turn`
- Platzhalter, Tokens und dynamische Spielbegriffe
- UI-, Codex-, Achievement-, Item-, Dialog- und weitere Lokalisierungstexte

## Zentrale Terminologie

Einige bewusst festgelegte Begriffe:

- `Perk` → **Talent**
- `Perk Point` → **Talentpunkt**
- `Buff` → **Buff**
- `Debuff` → **Debuff**
- `Minion` → **Diener**
- `Trait` → **Merkmal**
- `Spell Gem` → **Zauberstein**
- `Notoriety` → **Berüchtigung**

Bei Eigennamen, Kreaturenrassen und wiederkehrenden Spielbegriffen wurde projektweit auf eine einheitliche Benennung geachtet.

## Übersetzungsgrundsätze

- Das englische Original ist die Referenz für die Spielmechanik.
- Mechanische Genauigkeit hat Vorrang vor wortwörtlicher Übersetzung.
- Trigger wie `before`, `after`, `when`, `manually casts` und `additional` werden nicht miteinander vermischt.
- `Maximum Health`, `Current Health` und `Missing Health` werden unterschieden.
- Zahlen, Prozentwerte und Einschränkungen werden möglichst exakt erhalten.
- IDs, Platzhalter, Tokens und CSV-Struktur bleiben erhalten.
- Wiederkehrende Begriffe werden möglichst konsistent verwendet.
- Texte werden nicht nur aus Stilgründen geändert, wenn die vorhandene Übersetzung bereits korrekt und verständlich ist.

## QA

Zusätzlich zur Übersetzungsarbeit wurden projektweite Prüfungen durchgeführt, unter anderem auf:

- identische englische Texte mit abweichenden deutschen Übersetzungen
- fehlende oder zusätzliche Localization-Tokens
- Zahlen- und Prozentabweichungen
- uneinheitliche Regelterminologie
- Buff-/Debuff-/Diener-/Talent-Ausreißer
- bekannte problematische Altbegriffe

Die QA-Hilfsdateien befinden sich weiterhin im Repository, sind aber **nicht Teil der Installation**.

## Fehler melden / Ingame-Test

Beim Testen sind besonders hilfreich:

- Screenshot der fehlerhaften Stelle
- englischer Originaltext, falls bekannt
- deutscher Text
- Menü, Kreatur, Trait, Zauber oder Situation, in der der Text erscheint
- kurze Beschreibung, was falsch oder missverständlich ist

Damit lässt sich die entsprechende CSV-Stelle später gezielt korrigieren.

## Hinweis

Dies ist ein inoffizielles Community-Projekt. **Siralim Ultimate**, die Originaltexte und alle zugehörigen Marken und Inhalte gehören ihren jeweiligen Rechteinhabern. Dieses Repository dient der Verbesserung der deutschen Lokalisierung für Spieler des Spiels.
