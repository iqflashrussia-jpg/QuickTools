# Folder Scanning and Size Rules

These rules protect FlowDesk folder scanning, banner size detection, naming, and path behavior from accidental changes.

## Scope

The folder scanning and size domain includes:

- `modules/folder_scanner.py`;
- `modules/settings_finder.py`;
- project and folder creation code that depends on folder names or banner sizes;
- publish and create-project UI calls that display or use scanned folders;
- banner size detection;
- platform, subchannel, and campaign folder conventions;
- Windows paths, Cyrillic names, spaces, and nested project folders.

## Protected behavior

- Do not silently change how banner folders are detected.
- Do not silently change size parsing or size normalization.
- Do not silently change platform, subchannel, or campaign naming rules.
- Do not change folder traversal depth or ignored folders without an explicit request.
- Do not include ZIP, export, or cache folders in source folder scans unless explicitly requested.
- Do not treat generated archives as source banner folders.
- Do not change behavior for Cyrillic paths, spaces, or Windows separators without targeted checks.
- Do not combine folder scanning changes with optimizer, archive, Excel parser, or UI redesign changes.

## Size conventions

- Preserve existing size formats and naming conventions.
- Be careful with `300x250`, `240x400`, adaptive `%`-style names, and any project-specific canonical size names.
- Do not convert size notation or rename size folders unless the task explicitly asks for it.
- If size parsing changes, document before and after examples.
- If a size cannot be confidently parsed, prefer reporting or logging over guessing.

## Folder and path safety

- Never delete source folders during scanning.
- Never rename user project folders during scanning unless explicitly requested.
- Do not scan ignored or generated locations as source truth.
- Be careful with Cyrillic folder names, spaces in paths, long Windows paths, mixed slash/backslash separators, and nested campaign/platform/size folders.
- Preserve existing safe fallback behavior for missing or invalid paths.

## UI boundary

- Business logic stays in `modules/`.
- PySide6 widgets, dialogs, progress, logs, and button states stay in `ui_pyside6/`.
- Do not import PySide6 into folder scanning business logic.
- Folder scanning functions should return data or diagnostics; UI decides how to display it.
- Long scans should not freeze the UI if worker or thread flow exists.

## Diagnostics and logging

- Preserve existing diagnostics and log messages unless a task asks to change them.
- If scanner behavior changes, expose enough information to understand skipped folders, detected banner folders, detected sizes, and ambiguous or invalid names.
- Do not hide path or scanning errors silently in new code.

## Safe change process

- Read this file before folder scanning or size parsing changes.
- Make small scoped commits.
- Do not mix scanning changes with archive, optimizer, Excel parser, aliases, or UI redesign.
- For behavior changes, include before and after examples in the final report.
- For risky parsing changes, add or update regression tests where possible.

## Required checks

For folder scanning or size-related changes, run:

```powershell
.\.venv\Scripts\python.exe -m compileall modules ui_pyside6 main_pyside6.py
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\ruff.exe check .
```

For real folder scanning or size changes, also perform manual or smoke checks:

- run scan on a copied sample project only;
- verify source folders are not renamed or deleted;
- verify ZIP, export, and cache folders are ignored if expected;
- verify detected platform, subchannel, and size values;
- verify Cyrillic paths and paths with spaces;
- verify UI display and logs still make sense.
