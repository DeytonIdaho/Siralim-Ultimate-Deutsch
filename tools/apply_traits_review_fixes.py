#!/usr/bin/env python3
"""Apply reviewed German fixes to traits.csv safely.

Each fix identifies the exact English source string and the expected current
German string. The script aborts if a source row is missing, duplicated, or
has changed since review. This prevents broad/accidental replacements.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "traits.csv"

# (English source, expected German, reviewed German)
FIXES = [
    (
        'At the start of battle, this creature\'s spells with the "Cascading" property gain 4 additional maximum {STAT_charges} for each unique class among your creatures. Does not work on {SPELL_ultimate}s.',
        'Diese Kreatur\\\'s Zauber mit der Eigenschaft "Kaskadierend" haben 3 zusätzliche maximale {STAT_charges} für jede einzigartige Klasse unter deinen Kreaturen. Funktioniert nicht bei {SPELL_ultimate}.',
        'Zu Beginn des Kampfes erhalten die Zauber dieser Kreatur mit der Eigenschaft "Kaskadierend" 4 zusätzliche maximale {STAT_charges} für jede einzigartige Klasse unter deinen Kreaturen. Funktioniert nicht bei {SPELL_ultimate}s.',
    ),
    (
        'Enemies with {CONDNAME_DEBUFF_FEAR} take 15% more damage for each {CLASS_Death} creature fighting on your side. This trait does not stack.',
        'Feinde mit {CONDNAME_DEBUFF_FEAR} erleiden 20% mehr Schaden für jede {CLASS_Death} Kreatur, die auf deiner Seite kämpft. Dieses Merkmal ist nicht kumulativ.',
        'Feinde mit {CONDNAME_DEBUFF_FEAR} erleiden 15% mehr Schaden für jede {CLASS_Death}-Kreatur, die auf deiner Seite kämpft. Dieses Merkmal ist nicht kumulativ.',
    ),
    (
        'This is an extremely overpowered trait.',
        'Dies ist eine extrem übermächtige Merkmal.',
        'Dies ist ein extrem mächtiges Merkmal.',
    ),
    (
        "At the start of battle, your creatures gain a random enemy's trait. This trait does not stack.",
        'Zu Beginn des Kampfes erhalten deine Kreaturen eine zufällige Merkmal eines Gegners. Dieses Merkmal ist nicht kumulativ.',
        'Zu Beginn des Kampfes erhalten deine Kreaturen ein zufälliges Merkmal eines Gegners. Dieses Merkmal ist nicht kumulativ.',
    ),
    (
        'At the start of this creature\'s turn, it afflicts enemies with a random debuff.',
        'Zu Beginn des Zuges dieser Kreatur belegt sie Feinde mit einem zufälligen Debuffs.',
        'Zu Beginn des Zuges dieser Kreatur belegt sie Feinde mit einem zufälligen Debuff.',
    ),
    (
        'After this creature takes damage from an enemy\'s attack or spell, all other creatures with this trait {ACTION_attack} the enemy who afflicted that damage.',
        'Nachdem diese Kreatur Schaden durch den Angriff oder Zauber eines Feindes erleidet, {ACTION_attack} alle anderen Kreaturen mit dieses Merkmal den Feind, der diesen Schaden verursacht hat.',
        'Nachdem diese Kreatur Schaden durch den Angriff oder Zauber eines Feindes erleidet, {ACTION_attack} alle anderen Kreaturen mit diesem Merkmal den Feind, der diesen Schaden verursacht hat.',
    ),
    (
        'After this creature takes damage from an enemy\'s attack or spell, all other creatures with this trait {ACTION_attack} the enemy who afflicted that damage 3 times. These attacks always deal critical damage and cannot be dodged.',
        'Nachdem diese Kreatur Schaden durch den Angriff oder Zauber eines Feindes erleidet, {ACTION_attack} alle anderen Kreaturen mit dieses Merkmal den Feind, der diesen Schaden verursacht hat, 3 Mal. Diese Angriffe verursachen immer kritischen Schaden und können nicht ausgewichen werden.',
        'Nachdem diese Kreatur Schaden durch den Angriff oder Zauber eines Feindes erleidet, {ACTION_attack} alle anderen Kreaturen mit diesem Merkmal den Feind, der diesen Schaden verursacht hat, 3 Mal. Diese Angriffe verursachen immer kritischen Schaden und ihnen kann nicht ausgewichen werden.',
    ),
    (
        'Your creatures deal 75% more damage when it is not their turn. This trait does not stack.',
        'Deine Kreaturen verursachen 75% mehr Schaden, wenn sie nicht am Zug sind. Dieses Merkmal ist nicht kumulativ.',
        'Deine Kreaturen verursachen 75% mehr Schaden, wenn sie nicht am Zug sind. Dieses Merkmal ist nicht kumulativ.',
    ),
    (
        'After your creatures gain a stat (other than {STAT_health}), they grant 25% of this stat to your other creatures as well. Your creatures gain 50% less stats. This trait does not stack.',
        'Nachdem deine Kreaturen eine Merkmal erhalten (außer {STAT_health}), gewähren sie 25% dieses Merkmal auch deinen anderen Kreaturen. Deine Kreaturen erhalten 50% weniger Merkmale. Dieses Merkmal ist nicht kumulativ.',
        'Nachdem deine Kreaturen ein Attribut erhalten (außer {STAT_health}), gewähren sie deinen anderen Kreaturen ebenfalls 25% dieses Attributs. Deine Kreaturen erhalten 50% weniger Attribute. Dieses Merkmal ist nicht kumulativ.',
    ),
    (
        'This creature has 15% more stats (other than {STAT_health}) for each other creature with this trait fighting on your side.',
        'Diese Kreatur hat 15% mehr Attribute (außer {STAT_health}) für jedes andere Kreatur mit dieses Merkmal, das an deiner Seite kämpft.',
        'Diese Kreatur hat 15% mehr Attribute (außer {STAT_health}) für jede andere Kreatur mit diesem Merkmal, die an deiner Seite kämpft.',
    ),
    (
        'At the start of battle, this creature transforms into a copy of the second creature in your party, gains the innate trait of the third creature in your party, and gains the fused trait of the fourth creature in your party. This creature always starts battles at the bottom of the {TIMELINE}.',
        'Zu Beginn des Kampfes verwandelt sich diese Kreatur in eine Kopie der zweiten Kreatur in deiner Gruppe, erhält die angeborenes Merkmal der dritten Kreatur in deiner Gruppe und erhält die fusionierte Merkmal der vierten Kreatur in deiner Gruppe. Diese Kreatur beginnt Kämpfe immer am unteren Ende der {TIMELINE}.',
        'Zu Beginn des Kampfes verwandelt sich diese Kreatur in eine Kopie der zweiten Kreatur in deiner Gruppe, erhält das angeborene Merkmal der dritten Kreatur und das Fusionsmerkmal der vierten Kreatur. Diese Kreatur beginnt Kämpfe immer am unteren Ende der {TIMELINE}.',
    ),
    (
        'After this creature {ACTION_attacks}, it transforms into a copy of the target.',
        'Nachdem diese Kreatur {ACTION_attacks}, verwandelt sie sich in eine Kopie des Ziels.',
        'Nachdem diese Kreatur {ACTION_attacks}, verwandelt sie sich in eine Kopie des Ziels.',
    ),
]


def main() -> int:
    with PATH.open('r', encoding='utf-8-sig', newline='') as f:
        rows = list(csv.reader(f))

    applied = 0
    for english, expected_de, replacement_de in FIXES:
        matches = []
        for i, row in enumerate(rows):
            if len(row) >= 2 and row[0] == english:
                matches.append(i)
        if len(matches) != 1:
            raise SystemExit(f'ABORT: expected exactly one row for {english!r}, found {len(matches)}')
        i = matches[0]
        if rows[i][1] != expected_de:
            raise SystemExit(
                f'ABORT: reviewed German text changed for row {i+1}:\n'
                f'expected: {expected_de!r}\nactual:   {rows[i][1]!r}'
            )
        if replacement_de != expected_de:
            rows[i][1] = replacement_de
            applied += 1

    tmp = PATH.with_suffix('.csv.tmp')
    with tmp.open('w', encoding='utf-8-sig', newline='') as f:
        csv.writer(f, lineterminator='\n').writerows(rows)
    tmp.replace(PATH)
    print(f'Applied {applied} reviewed traits fixes.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
