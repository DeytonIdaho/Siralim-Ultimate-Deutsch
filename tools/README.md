# Translation QA Pipeline

This helper avoids GitHub/API size limits by processing the large Siralim CSV files locally and producing small review chunks.

## Steam Deck / Linux

```bash
cd ~/Siralim-Ultimate-Deutsch
git checkout translation-work
git pull
python3 tools/translation_pipeline.py PATH/TO/perks.csv --out review/perks --glossary glossary.csv
python3 tools/translation_pipeline.py PATH/TO/traits.csv --out review/traits --glossary glossary.csv --chunk-size 100
git add review
git commit -m "Generate translation QA review chunks"
git push origin translation-work
```

If your glossary has another path/name, replace `glossary.csv`. The script also contains a small built-in terminology fallback.

## What is checked

- missing German translation
- mismatch of placeholders/tags such as `{...}`, `[...]`, `<...>`, `%s`, `\\n`
- glossary terminology that appears in English but not in the German translation

## Output

Each `review_XXX.csv` contains:

- original CSV line number
- English source
- current German text
- detected issues
- `reviewed` field
- `replacement` field for a corrected German translation

`SUMMARY.md` gives totals. The generated review files are intentionally small enough to inspect and revise through GitHub/ChatGPT.

## Important

The script does not overwrite game translation files. It creates a QA work queue first. Corrections should be reviewed before being applied to the actual CSVs.
