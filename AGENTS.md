# QuickTools / FlowDesk — Codex Rules

These rules are the source of truth for AI-assisted changes in this repository.

## Project identity

QuickTools / FlowDesk is a Windows desktop Python application for HTML5 banner workflow.

Core responsibilities:
- create and prepare project folders;
- scan banner folders;
- find and validate settings;
- optimize images and ZIP packages;
- create archives;
- help with FLA-related operations;
- provide a PySide6 desktop UI for the workflow.

## Repository structure

Expected structure:

- `main_pyside6.py` — PySide6 application entry point.
- `ui_pyside6/` — PySide6 UI blocks, widgets, styles, icons, tabs.
- `modules/` — business logic, file operations, parsing, optimization, archive logic.
- `requirements.txt` — runtime dependencies.
- `oxipng.exe` — external optimizer binary that is intentionally kept in the repo.
- `last_project.txt` — local user state; must not be committed.
- `project_structure.txt` — generated repository snapshot; must not be committed.

## Non-negotiable rules

Codex must not:
- rewrite the architecture without explicit permission;
- mix unrelated tasks in one change;
- touch unrelated files;
- silently rename public functions/classes;
- delete existing business rules without a clear reason and user approval;
- convert a targeted bug fix into a broad refactor;
- commit generated reports, local state, caches, build artifacts, or temporary files;
- claim checks passed if they were not actually run.

## Architecture boundaries

- UI code belongs in `ui_pyside6/`.
- Business logic belongs in `modules/`.
- UI may call business logic.
- Business logic must not depend on PySide6 widgets.
- Business logic should remain testable without launching the UI.
- File-system operations should be explicit and easy to trace.

## Protected behavior

Preserve existing user-approved behavior unless the task explicitly asks to change it.

Important areas:
- project creation;
- folder scanning;
- settings detection;
- image optimization;
- archive creation;
- FLA operations;
- PySide6 UI layout and styling;
- local project path persistence.

## Rule routing

Before changing code, identify the task domain and read the relevant rule files.

Always read:
- `docs/rules/project-hygiene.md` for local/generated files and repository hygiene.
- `docs/rules/git-workflow.md` for branch, commit, and push safety.
- `docs/rules/codex-safe-commit.md` before staging or committing changes.
- `docs/rules/regression-checks.md` before deciding which checks to run.

For domain-specific tasks, also read:

- Image optimizer / target KB / image compression:
  - `docs/rules/image-optimizer.md`

- Publish, archive, ZIP creation, generated archives, `.fla` ZIP exclusions:
  - `docs/rules/publish-and-archive.md`

- Folder scanning, banner sizes, platform/subchannel/campaign naming, path parsing:
  - `docs/rules/folder-scanning-and-sizes.md`

- Excel parser, Excel import, Excel review, `.xlsx` parsing, sheet/header detection, row filtering, hidden rows, merged cells, HTML5 row detection:
  - `docs/rules/excel-parser.md`

- Aliases, normalization, canonical values, platform aliases, size aliases, adaptive size aliases, format aliases, matched/unmatched diagnostics:
  - `docs/rules/aliases-normalization.md`

- FLA discovery/opening, `os.startfile`, open by size, open all:
  - `docs/rules/fla-operations.md`

- PySide6 visual/UI tasks:
  - `docs/rules/ui-pyside6.md`

- PySide6 threading, workers, signals, progress/logs, button states:
  - `docs/rules/ui-pyside6.md`
  - `docs/rules/pyside6-threading-and-ui.md`

When a task touches multiple domains, read every matching rule file and keep changes separated into small scoped commits.

## Dependency rules

- Keep `requirements.txt` synchronized with actual imports.
- If a new external package is used, add it to `requirements.txt`.
- Do not remove dependencies without checking all imports.
- Prefer standard library modules unless an external dependency is clearly justified.

## UI rules

- Keep the UI dark, restrained, and consistent.
- Primary CTA buttons should remain visually prominent.
- Do not redesign screens unless the task explicitly asks for UI redesign.
- Do not mix large visual redesign with logic changes.
- Reuse existing widgets/styles when possible.
- Prefer consistent spacing, cards, table separators, and button states.

## Change process

Before editing, Codex must:
1. read the relevant files;
2. summarize the task;
3. list target files;
4. identify risks;
5. avoid broad refactoring unless explicitly requested.

During editing, Codex must:
1. keep the diff small;
2. preserve existing behavior;
3. make reversible changes;
4. add comments only where they explain why, not what every line does.

After editing, Codex must report:
1. changed files;
2. what changed and why;
3. checks run;
4. checks not run;
5. remaining risks or assumptions.

## Required checks

When possible, run:

```bash
python -m compileall .
```

If configured in the repository, also run:

```bash
ruff check .
pytest
```

If a command is unavailable or tests do not exist, say so clearly. Do not invent successful results.

## Git rules

- One task = one logical diff.
- Do not commit unless the user explicitly asks for a commit.
- Before commit, show `git status` and a short diff summary.
- Never include local state, generated reports, caches, `.venv/`, or temporary files in commits.

## Response format for Codex

Use this final format after each task:

```text
Summary:
- ...

Changed files:
- path/to/file.py — what changed and why

Checks:
- python -m compileall . — passed/failed/not run
- ruff check . — passed/failed/not run
- pytest — passed/failed/not run

Not changed:
- ...

Risks / notes:
- ...
```
