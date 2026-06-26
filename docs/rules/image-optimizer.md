# Image Optimizer Rules

These rules protect FlowDesk image optimization behavior from accidental changes.

## Scope

The image optimizer domain includes:

- `modules/image_optimizer.py`;
- `modules/image_optimizer_main.py`;
- optimizer-related calls from `ui_pyside6/optimizer_block.py`;
- external optimization tools such as `oxipng.exe`;
- ZIP and KB target behavior only when directly related to the optimizer flow.

## Protected behavior

- Do not change optimization algorithms unless explicitly requested.
- Do not change return contracts silently.
- Preserve existing fallback behavior.
- Preserve `return False, 0` and `return 0` style contracts unless a task explicitly requires a behavior change.
- Do not remove `oxipng.exe` or assume it is globally installed.
- Do not replace local bundled tools with new external dependencies without explicit approval.
- Do not change target KB interpretation without an explicit request.
- Do not silently change lossy/lossless strategy.
- Do not overwrite or delete source images unless the existing code already does so intentionally.

## Error handling

- Use explicit `except Exception:` instead of bare `except:`.
- Do not hide errors in new optimizer code without logging or returning a documented failure result.
- Preserve user-facing failure behavior unless the task asks to change it.
- Do not convert safe fallback returns into hard crashes without explicit approval.

## UI boundary

- Business logic stays in `modules/`.
- PySide6 widgets, signals, progress UI, and button state belong in `ui_pyside6/`.
- Do not import PySide6 into optimizer business logic.
- Do not mutate widgets from optimizer functions.
- Long-running optimization must not block the UI if the existing architecture uses a worker or thread flow.

## Files and generated artifacts

- Do not commit generated optimized files, reports, caches, or temporary ZIPs.
- Keep generated artifacts under ignored or export folders.
- Be careful with paths containing Cyrillic text, spaces, and Windows separators.
- Do not delete user project folders as part of optimizer cleanup unless explicitly requested.

## Safe change process

- Read this file before optimizer changes.
- Make small scoped commits.
- Do not combine optimizer algorithm changes with UI redesign or archive changes.
- For any behavior change, document before and after behavior in the final report.

## Required checks

For optimizer-related changes, run:

```powershell
.\.venv\Scripts\python.exe -m compileall modules ui_pyside6 main_pyside6.py
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\ruff.exe check .
```

For real optimizer logic changes, also perform manual or smoke checks:

- run optimizer on a small copied sample project only;
- verify original source files are not unexpectedly deleted;
- verify output size and ZIP behavior if the task touches target KB logic;
- verify logs and progress still make sense in the UI.
