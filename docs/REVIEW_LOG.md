# Prüfprotokoll

Hier werden geprüfte Bereiche und konkrete Übersetzungsentscheidungen dokumentiert.

## Status

- [x] CSV-Struktur geprüft
- [x] Platzhalter-/Tag-Erhalt als Pflicht festgelegt
- [x] Grundglossar erstellt
- [ ] Traits vollständig geprüft
- [ ] Perks vollständig geprüft
- [ ] Spells vollständig geprüft
- [ ] Battle/UI-Terminologie geprüft
- [ ] Installierbare Override-Dateien erzeugt
- [ ] In-Game-Test auf Steam Deck

## Erste Trait-Prüfung

Die ersten Einträge in `traits.csv` wurden Englisch ↔ Deutsch verglichen.

### Bereits mechanisch korrekt

- Circle of Life / Kreis des Lebens
- Righteous Winds / Rechtschaffene Winde
- Divine Mending / Göttliche Heilung
- Spur of the Heavens / Sporn der Himmel
- Chrysaor's Ambition / Chrysaors Ambition

Diese Einträge erhalten ihre Mechanik korrekt. Stilistische Änderungen werden nur vorgenommen, wenn sie die Lesbarkeit deutlich verbessern, ohne Trigger oder Tags anzutasten.

## Erste Perk-Prüfung

### Celerity / Schnelligkeit

Original:
`After your creatures dodge, they {ACTION_attack} the enemy.`

Aktuelles Deutsch:
`Nachdem deine Kreaturen ausweichen, {ACTION_attack} sie den Feind.`

Bewertung: Mechanisch korrekt, sprachlich holprig. Kandidat für stilistische Korrektur unter Erhalt von `{ACTION_attack}`.

### Serenity / Gelassenheit

Die Einschränkung bezüglich `independent chances to dodge attacks` ist im Deutschen vorhanden. Mechanisch korrekt. `independent` darf bei späterer Überarbeitung nicht entfallen.

### Spiritual Attunement / Geistige Abstimmung

Mechanisch korrekt. Der Trigger `When ... take indirect damage` sowie die Chance, genau diesen Schaden zu verhindern, sind erhalten.

### Protective Winds / Schützende Winde

Mechanisch korrekt. Wichtig: `independent chance` ist korrekt als `unabhängige ... Chance` enthalten und muss erhalten bleiben.

### Dampen Harm / Schaden dämpfen

Mechanisch korrekt. Die Bedingung `would receive fatal damage` und die Kopplung an die Ausweichchance sind erhalten.

## Kritische Prüfwörter

Bei allen folgenden Einträgen wird besonders geprüft, ob diese englischen Regelwörter im Deutschen vollständig erhalten bleiben:

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

Folgende Bestandteile dürfen niemals übersetzt, entfernt oder umsortiert werden:

- `{ACTION_*}`
- `{STAT_*}`
- `{CONDNAME_*}`
- `{TIMELINE}` und vergleichbare `{...}`-Tokens
- `<1>`, `<2>`, `<3>` usw.
- `[creature_or_internal_reference]`
- sonstige interne Spiel-Tags
