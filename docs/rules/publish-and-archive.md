# Publish and Archive Rules

These rules protect FlowDesk publish, archive, and ZIP behavior from accidental changes.

## Scope

The publish and archive domain includes:

- `modules/archive_handler.py`;
- publish and archive-related UI in `ui_pyside6/archiver_block.py`;
- publish-related UI in `ui_pyside6/publish_block.py`;
- ZIP creation and deletion flow;
- publish folder creation;
- generated archives and export artifacts.

## Protected behavior

- Do not change ZIP or archive behavior unless explicitly requested.
- Do not silently change output folder locations.
- Do not silently rename generated ZIP files.
- Do not include `.fla` files in generated ZIPs unless explicitly requested.
- Preserve existing file-count and log behavior unless the task asks to change it.
- Do not change publish folder structure without explicit approval.
- Do not change platform or subchannel naming behavior without explicit approval.
- Do not combine archive logic changes with optimizer or UI redesign changes.

## File safety

- Never delete user source folders unless the task explicitly asks for deletion.
- Never delete `.fla`, source assets, or project roots as part of cleanup.
- Deletion actions must be limited, visible, and logged.
- Be careful with paths containing Cyrillic text, spaces, long names, and Windows separators.
- Generated ZIPs, reports, and caches should stay in ignored or export locations.

## ZIP rules

- `.fla` should stay excluded from ZIP by default.
- Preserve existing exclusion lists unless explicitly changed.
- Do not compress or optimize images as part of archive-only changes.
- Do not change target KB or image optimizer behavior from archive code.
- Keep archive creation deterministic where possible.

## UI boundary

- Business logic stays in `modules/`.
- PySide6 widgets, dialogs, progress, logs, and button states stay in `ui_pyside6/`.
- Do not import PySide6 into archive business logic.
- Long-running archive or publish work should not freeze the UI if worker or thread flow exists.
- User-facing logs should remain clear and non-destructive.

## Error handling

- Use explicit `except Exception:` instead of bare `except:`.
- Do not hide destructive-operation errors.
- Do not convert safe fallback behavior into hard crashes without explicit approval.
- Deletion and archive failures should be logged when there is an existing log flow.

## Safe change process

- Read this file before archive or publish changes.
- Make small scoped commits.
- Do not mix archive, optimizer, Excel parser, aliases, and UI redesign in one commit.
- For behavior changes, describe before and after behavior in the final report.
- For destructive operations, explicitly list what can be deleted and what cannot.

## Required checks

For publish or archive-related changes, run:

```powershell
.\.venv\Scripts\python.exe -m compileall modules ui_pyside6 main_pyside6.py
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\ruff.exe check .
```

For real archive or publish changes, also perform manual or smoke checks:

- run archive creation on a copied sample project only;
- verify `.fla` files are excluded from ZIP;
- verify source folders and assets are not unexpectedly deleted;
- verify ZIP output location and naming;
- verify UI logs and progress still make sense;
- verify deletion actions only affect intended generated files.
