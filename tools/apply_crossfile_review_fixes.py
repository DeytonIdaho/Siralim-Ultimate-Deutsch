from pathlib import Path
import csv, io

# Reviewed safe corrections discovered during the cross-file creature-name/grammar pass.
# Each tuple is: tag, expected old German text, new German text.
PATCHES = {
    'battle.csv': [
        ('L_B_CAST_ERROR1', 'Kreatur kann diesen Zauber nicht wirken (keine Aufladungen, Verstummt, Edelstein ist versiegelt, usw.)', 'Kreatur kann diesen Zauber nicht wirken (keine Ladungen, Verstummt, Zauberstein ist versiegelt usw.)'),
        ('L_B_ETH_GEMS_SEALED', 'Ätherische Edelsteine\\nVersiegelt', 'Ätherische Zaubersteine\\nVersiegelt'),
        ('L_B_ETH_GEMS_REPLACED', 'Ätherische Edelsteine\\nErsetzt', 'Ätherische Zaubersteine\\nErsetzt'),
        ('L_B_FLOAT_PERKGAINED', 'Talent erhalten:\\n{1}', 'Vorteil erhalten:\\n{1}'),
        ('L_B_GAIN_GEM', '{1} erhielt Edelstein: {2}.', '{1} erhielt Zauberstein: {2}.'),
        ('L_B_GAIN_GEM_FLOAT', 'Erhaltener Edelstein:\\n{1}', 'Zauberstein erhalten:\\n{1}'),
        ('L_B_MSG_NOCAST_REALM', 'Eine Reichseigenschaft verhindert, dass dein {1} manuell verteidigt.', 'Eine Reichseigenschaft verhindert, dass dein {1} manuell Zauber wirkt.'),
    ],
}


def replace_row(path, tag, old, new):
    raw = path.read_bytes()
    bom = raw.startswith(b'\xef\xbb\xbf')
    data = raw[3:] if bom else raw
    newline = b'\r\n' if b'\r\n' in data else b'\n'
    lines = data.splitlines(keepends=True)
    hits = []
    for i, line in enumerate(lines):
        text = line.decode('utf-8').rstrip('\r\n')
        try:
            row = next(csv.reader([text]))
        except Exception:
            continue
        if row and row[0] == tag:
            hits.append((i, row, line))
    if len(hits) != 1:
        raise SystemExit(f'{path}: {tag}: expected exactly one row, found {len(hits)}')
    i, row, original = hits[0]
    header = next(csv.reader([lines[0].decode('utf-8').rstrip('\r\n')]))
    try:
        de = header.index('German')
    except ValueError:
        raise SystemExit(f'{path}: German column missing')
    if row[de] != old:
        raise SystemExit(f'{path}: {tag}: old value mismatch\nEXPECTED: {old!r}\nACTUAL:   {row[de]!r}')
    row[de] = new
    out = io.StringIO(newline='')
    csv.writer(out, lineterminator='').writerow(row)
    ending = b'\r\n' if original.endswith(b'\r\n') else (b'\n' if original.endswith(b'\n') else b'')
    lines[i] = out.getvalue().encode('utf-8') + ending
    path.write_bytes((b'\xef\xbb\xbf' if bom else b'') + b''.join(lines))


def validate(path):
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        rows = list(csv.reader(f))
    if not rows or 'German' not in rows[0]:
        raise SystemExit(f'{path}: invalid CSV/header')
    width = len(rows[0])
    bad = [n for n,r in enumerate(rows,1) if len(r) != width]
    if bad:
        raise SystemExit(f'{path}: malformed row widths at {bad[:10]}')

count = 0
for filename, patches in PATCHES.items():
    p = Path(filename)
    for tag, old, new in patches:
        replace_row(p, tag, old, new)
        count += 1
    validate(p)

print(f'Applied and validated {count} reviewed cross-file corrections.')
