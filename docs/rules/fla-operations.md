# FLA Operations Rules

These rules protect FlowDesk FLA discovery and opening behavior from accidental changes.

## Scope

The FLA operations domain includes:

- `modules/fla_operations.py`;
- FLA-related UI in `ui_pyside6/fla_block.py`;
- `.fla` discovery;
- opening `.fla` files from the app;
- Windows-only launch behavior such as `os.startfile`;
- project folders containing Animate or FLA sources.

## Protected behavior

- Do not change how `.fla` files are discovered unless explicitly requested.
- Do not change "open by size" or "open all" semantics without explicit approval.
- Do not rename, move, delete, or modify `.fla` source files.
- Do not include `.fla` in ZIP or archive flows unless explicitly requested in archive rules.
- Do not assume `.fla` files are safe to overwrite.
- Do not combine FLA logic changes with archive, optimizer, folder scanner, or UI redesign changes.

## Windows behavior

- FLA opening is Windows-aware and may depend on `os.startfile`.
- Do not replace `os.startfile` with cross-platform code unless explicitly requested.
- If adding cross-platform behavior, preserve Windows behavior first.
- Handle missing file associations gracefully.
- Do not hardcode Adobe Animate executable paths unless explicitly requested.

## Path safety

- Be careful with Cyrillic paths, spaces, long Windows paths, and mixed separators.
- Never delete or rewrite project folders during FLA discovery.
- Never create generated files next to `.fla` sources unless the task explicitly asks.
- Preserve safe fallback behavior when files or folders are missing.

## UI boundary

- Business logic stays in `modules/`.
- PySide6 widgets, dialogs, progress, logs, and buttons stay in `ui_pyside6/`.
- Do not import PySide6 into `modules/fla_operations.py`.
- FLA functions should return results or log through existing callback and data flow; UI decides how to display it.
- UI should remain responsive during batch open and find operations if worker or thread flow exists.

## Error handling

- Use explicit `except Exception:` instead of bare `except:`.
- Opening failures should be logged when existing log flow is available.
- Do not hide destructive or path-related errors silently in new code.
- Do not convert safe fallback behavior into hard crashes without explicit approval.

## Safe change process

- Read this file before FLA-related changes.
- Make small scoped commits.
- Do not mix FLA changes with archive, optimizer, Excel parser, aliases, or UI redesign.
- For behavior changes, describe before and after behavior in the final report.
- For risky path or opening changes, add or update smoke checks where possible.

## Required checks

For FLA-related changes, run:

```powershell
.\.venv\Scripts\python.exe -m compileall modules ui_pyside6 main_pyside6.py
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\ruff.exe check .
```

For real FLA changes, also perform manual or smoke checks:

- run on a copied sample project only;
- verify `.fla` files are not renamed, moved, deleted, or modified;
- verify "open by size" still opens intended files;
- verify "open all" still targets only intended `.fla` files;
- verify missing files or folders produce safe logs or fallback behavior;
- verify Cyrillic paths and paths with spaces.
