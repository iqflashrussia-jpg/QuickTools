# Aliases and Normalization Rules

These rules protect FlowDesk alias handling, value normalization, canonical values, and review diagnostics from accidental changes.

## Scope

The aliases and normalization domain includes:

- alias dictionaries and alias config files;
- canonical values for platforms, sizes, adaptive sizes, and formats;
- normalization of noisy Excel values;
- normalization used before publish or folder creation;
- manual alias review flows, if present in the project;
- diagnostics for matched and unmatched values;
- confidence and match method metadata, if present in the project.

## Current source of truth

- The source of truth is the current repository state.
- Do not assume old file names exist.
- Do not recreate missing historical files such as `modules/value_normalizer.py` unless explicitly requested.
- Before changing aliases or normalization, locate the actual current config or code path.
- If alias data is stored in JSON or config files, treat those files as user-facing project data and change them carefully.

## Protected behavior

- Do not silently rename canonical values.
- Do not silently merge or delete aliases.
- Do not change platform, size, adaptive size, or format normalization behavior without explicit approval.
- Do not change match priority or confidence behavior without explicit approval.
- Do not convert unknown values into guessed canonical values.
- Do not combine alias changes with Excel parser, publish/archive, optimizer, or UI redesign changes.
- Do not overwrite user alias data without backup or explicit approval.

## Canonical values

- Canonical values must remain stable because other flows may depend on them.
- Be careful with platform names, size notation, adaptive sizes, and HTML5 format labels.
- Do not change canonical notation unless the task explicitly asks for it.
- If a canonical value changes, document before and after and affected aliases.
- Prefer adding explicit aliases over changing existing canonical values when possible.

## Matching and diagnostics

- Preserve existing diagnostics for matched and unmatched values.
- If match method or confidence metadata exists, do not remove it without approval.
- Ambiguous values should be reported for review instead of guessed.
- Matching changes must include before and after examples.
- Do not hide normalization errors silently in new code.

## Data safety

- Alias and config edits should be small and reviewable.
- Back up user-maintained alias data before risky edits if the project already has a backup pattern.
- Do not delete generated reports or alias candidate files unless explicitly requested.
- Do not use broad automated rewrites for alias JSON or config files.
- Do not reorder large alias files unless the task explicitly asks for sorting or reformatting.

## UI boundary

- Normalization and business logic belongs in `modules/` or config/data files.
- PySide6 alias review tables, dialogs, buttons, and display logic belong in `ui_pyside6/`.
- Do not import PySide6 into normalization or business logic modules.
- If alias behavior and alias UI both need changes, prefer separate scoped commits.

## Safe change process

- Read this file before aliases or normalization changes.
- Also read `docs/rules/excel-parser.md` if the task touches Excel values.
- Also read `docs/rules/folder-scanning-and-sizes.md` if the task touches size, platform, or folder naming.
- Also read `docs/rules/regression-checks.md`.
- Make small scoped commits.
- For behavior changes, include before and after examples and matched/unmatched counts where possible.
- Do not mix alias normalization changes with parser changes unless explicitly requested.

## Required checks

For aliases or normalization changes, run:

```powershell
.\.venv\Scripts\python.exe -m compileall modules ui_pyside6 main_pyside6.py
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\ruff.exe check .
```

For real aliases or normalization changes, also perform manual or smoke checks:

- test on copied sample Excel or project data only;
- verify source Excel files are not modified;
- verify known platform aliases still normalize correctly;
- verify known size aliases still normalize correctly;
- verify adaptive sizes still normalize correctly if touched;
- verify unmatched values remain visible for review;
- verify publish and folder creation still receives expected canonical values;
- verify alias UI or review flow still displays understandable results if present.
