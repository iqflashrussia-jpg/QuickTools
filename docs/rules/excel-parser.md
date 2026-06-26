# Excel Parser Rules

These rules protect FlowDesk Excel import, parser diagnostics, and Excel review behavior from accidental changes.

## Scope

The Excel parser domain includes:

- Excel import and review flow;
- `.xlsx` parsing;
- sheet detection;
- header detection;
- row filtering;
- hidden rows;
- merged cells;
- HTML5 format detection;
- platform, size, and format extraction from Excel;
- adaptive size detection from Excel;
- diagnostics for recognized and unrecognized rows;
- UI display of Excel review results.

## Protected behavior

- Do not silently change Excel parsing behavior.
- Do not change recognized or unrecognized row rules without explicit approval.
- Do not change sheet or header detection logic without sample-based checks.
- Do not change hidden-row handling without explicit approval.
- Do not change merged-cell inheritance behavior without explicit approval.
- Do not change HTML5 filtering rules without explicit approval.
- Do not combine Excel parser changes with aliases, publish/archive, optimizer, or UI redesign changes.
- Do not delete or overwrite source Excel files.

## Sheet and header detection

- Preserve current sheet detection behavior.
- Preserve current header scan depth unless explicitly requested.
- Header synonyms must be changed carefully and with examples.
- If headers are missing or ambiguous, prefer diagnostics over guessing.
- Do not assume every Excel uses the same sheet name.

## Row filtering

- Preserve current filtering of HTML5 rows.
- Preserve exclusion of raster-only, instruction-footer, or non-banner rows if current code supports it.
- Preserve hidden-row behavior.
- Preserve treatment of URL and instruction lines unless explicitly requested.
- If filtering changes, report before and after recognized and unrecognized counts.

## Size, platform, and format extraction

- Preserve current extraction of size, platform, subchannel, and format values.
- Do not change canonical size notation unless explicitly requested.
- Be careful with adaptive sizes and `%`-style sizes.
- Be careful with Cyrillic text, mixed separators, and noisy cells.
- If a cell contains multiple possible values, prefer diagnostics over unsafe guessing.

## Diagnostics

- Parser changes must preserve or improve diagnostics.
- Diagnostics should help explain:
  - recognized rows;
  - unrecognized rows;
  - excluded rows;
  - missing headers;
  - ambiguous sizes, platforms, or formats;
  - raw hits not included.
- Do not hide parser errors silently in new code.

## UI boundary

- Excel parsing and business logic belongs in `modules/`.
- PySide6 display, tables, progress, buttons, and dialogs belong in `ui_pyside6/`.
- Do not import PySide6 into parser or business logic modules.
- UI may display parser results, diagnostics, warnings, and progress.
- If parser behavior and UI presentation both need changes, prefer separate scoped commits.

## Safe change process

- Read this file before Excel parser changes.
- Also read `docs/rules/regression-checks.md`.
- Make small scoped commits.
- Use copied sample Excel files only.
- Document before and after counts when parser behavior changes.
- Do not mix parser changes with aliases normalization changes unless explicitly requested.

## Required checks

For Excel parser changes, run:

```powershell
.\.venv\Scripts\python.exe -m compileall modules ui_pyside6 main_pyside6.py
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\ruff.exe check .
```

For real Excel parser changes, also perform manual or smoke checks:

- test on copied sample `.xlsx` files only;
- verify source Excel files are not modified;
- verify recognized and unrecognized counts;
- verify hidden rows are handled as expected;
- verify HTML5 rows are detected as expected;
- verify raster-only and instruction rows are excluded if expected;
- verify adaptive sizes are detected as expected;
- verify diagnostics are understandable;
- verify Excel review UI still displays results correctly.
