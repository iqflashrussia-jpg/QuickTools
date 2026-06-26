# PySide6 Threading and UI Rules

These rules protect FlowDesk PySide6 runtime behavior, worker flow, progress updates, logs, and button state from accidental changes.

## Scope

The PySide6 threading and UI behavior domain includes:

- PySide6 UI files in `ui_pyside6/`;
- `main_pyside6.py`;
- `QThread` and worker patterns;
- signals and slots;
- progress bars, logs, and long-running actions;
- button enabled, disabled, and loading states;
- `QFileDialog` and `QMessageBox` UI flows;
- UI calls into `modules/` business logic.

## Relationship to ui-pyside6.md

- This file complements `docs/rules/ui-pyside6.md`.
- `ui-pyside6.md` covers visual and design consistency.
- This file covers runtime safety, threading, long-running actions, and UI state.
- For UI tasks, read both files when the task touches behavior, workers, progress, logs, or button state.

## Protected behavior

- Do not redesign UI while fixing threading or behavior bugs.
- Do not change visual styling unless explicitly requested.
- Do not change button labels, tabs, workflows, or user-facing text unless the task asks for it.
- Do not move business logic into UI files.
- Do not move PySide6 dependencies into `modules/`.
- Do not combine UI behavior changes with optimizer, archive, or parser algorithm changes.

## Threading and worker safety

- Do not update Qt widgets directly from worker or background threads.
- Use signals, slots, or the existing project pattern for progress and log updates.
- Keep `QThread` and worker object lifetimes safe; avoid local variables that get garbage-collected during work.
- Do not block the main UI thread with long-running optimizer, archive, publish, or scanning work.
- Restore button states after success, failure, or cancellation.
- Handle repeated clicks and re-entry safely.
- Do not create multiple competing workers for the same action unless explicitly designed.

## Progress, logs, and user feedback

- Preserve existing progress and log behavior unless the task explicitly asks to change it.
- Logs should remain clear, user-facing, and non-destructive.
- Long tasks should show progress or at least visible status where the current UI supports it.
- Failures should be visible when an existing log or status flow exists.
- Avoid silent failures in new UI code.

## UI boundary

- UI files may call business functions from `modules/`.
- Business logic in `modules/` must not import PySide6.
- File dialogs, message boxes, widgets, colors, icons, button states, and layout live in the UI layer.
- Optimizer, archive, FLA, and scanner logic lives in `modules/`.
- If a UI task requires business logic changes, make that a separate scoped commit.

## Error handling

- Use explicit `except Exception:` instead of bare `except:`.
- Do not swallow exceptions in new UI code without a log, status message, dialog, or documented fallback.
- Preserve existing fallback behavior unless explicitly requested.
- Do not turn recoverable UI errors into hard crashes without approval.

## Safe change process

- Read this file before PySide6 behavior or threading changes.
- Also read `docs/rules/ui-pyside6.md` for visual consistency.
- Make small scoped commits.
- Separate visual redesign, UI behavior, and business logic changes.
- In final reports, describe:
  - which UI action changed;
  - whether worker or thread logic changed;
  - how button, progress, and log states are restored;
  - what manual checks were performed.

## Required checks

For PySide6 behavior or threading changes, run:

```powershell
.\.venv\Scripts\python.exe -m compileall modules ui_pyside6 main_pyside6.py
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\ruff.exe check .
```

For real UI or threading changes, also perform manual or smoke checks:

- launch the app manually;
- run the affected button or action;
- verify UI does not freeze during long action;
- verify progress and log output updates;
- verify buttons are disabled and enabled correctly;
- verify repeated clicks do not start duplicate conflicting work;
- verify success and failure paths restore UI state;
- verify no visual redesign happened unless requested.
