# Übersetzungsglossar

Dieses Glossar definiert die verbindliche Terminologie für die deutsche Community-Übersetzung von Siralim Ultimate.

## Grundregeln

- Mechanische Genauigkeit hat Vorrang vor wörtlicher Übersetzung.
- Gleiche englische Mechanik wird immer gleich übersetzt.
- Platzhalter wie `{1}`, `{2}` sowie Formatierungs-Tags bleiben unverändert.
- `after`, `before`, `when`, `at the start`, `at the end` werden nicht miteinander vermischt.
- `additional` muss als zusätzlicher Effekt erkennbar bleiben.
- Namen von Buffs, Debuffs, Stats, Klassen und Kernmechaniken werden konsistent verwendet.

## Kampfbegriffe

| Englisch | Deutsch | Hinweis |
|---|---|---|
| Attack | Angriff | Stat/Aktion kontextabhängig, Begriff bleibt konsistent |
| Intelligence | Intelligenz | Stat |
| Defense | Verteidigung | Stat |
| Speed | Geschwindigkeit | Stat |
| Health | Gesundheit | aktuelle/grundsätzliche Gesundheit; Kontext beachten |
| Maximum Health / Max Health | Maximale Gesundheit | niemals mit aktueller Gesundheit verwechseln |
| missing Health | fehlende Gesundheit | Differenz zwischen Maximum und aktuell |
| current Health | aktuelle Gesundheit | explizit, wenn das Original `current` sagt |
| Spell | Zauber | |
| Spell Gem | Zauberstein | vorläufig; wird anhand bestehender UI-Terminologie gegengeprüft |
| cast | zaubern / wirkt einen Zauber | niemals `Besetzung` |
| manually cast | manuell zaubern / wirkt manuell | Trigger-relevant; `manuell` darf nicht entfallen |
| additional | zusätzlich | mechanisch relevant |
| Spell Potency | Zauberstärke | vorläufig; Konsistenz mit Spiel-UI wird geprüft |
| Charges | Ladungen | Anzahl verfügbarer Zauberanwendungen |
| Trait | Eigenschaft | bestehender deutscher Spielbegriff wird noch global geprüft |
| Perk | Perk | Klassen-Perks |
| Buff | Buff | |
| Debuff | Debuff | |
| Minion | Diener | vorläufig; bestehende Spielterminologie wird geprüft |
| resurrect | wiederbeleben | |
| resurrection | Wiederbelebung | |
| Defend | Verteidigen | Aktion |
| Provoke | Provozieren | Aktion |
| Dodge | Ausweichen | |
| Critical Hit | Kritischer Treffer | |

## Trigger und Zeitpunkte

| Englisch | Deutsch |
|---|---|
| after | nachdem / nach |
| before | bevor / vor |
| when | wenn |
| at the start of battle | zu Beginn des Kampfes |
| at the end of battle | am Ende des Kampfes |
| at the start of its turn | zu Beginn seines Zuges |
| at the end of its turn | am Ende seines Zuges |
| for the rest of battle | für den Rest des Kampfes |
| once per turn | einmal pro Zug |

## Noch zu prüfen

Die Begriffe `Spell Gem`, `Spell Potency`, `Trait` und `Minion` werden gegen `ui.csv`, `battle.csv`, `spells.csv` und `vocabulary.csv` geprüft, bevor wir sie massenhaft verwenden.
