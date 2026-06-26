# Regression Check Rules

These rules define the minimum automated and manual checks Codex should use before committing FlowDesk changes.

## Scope

This document covers:

- required automated checks before commits;
- zone-specific manual and smoke checks;
- final report requirements;
- rules for deciding when a change is safe enough to commit;
- checks for optimizer, archive and publish, folder scanning, FLA, UI and threading, and docs-only changes.

## Always-run automated checks

Baseline checks:

```powershell
.\.venv\Scripts\python.exe -m compileall modules ui_pyside6 main_pyside6.py
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\ruff.exe check .
```

- For docs-only changes, still prefer the baseline checks when practical.
- If checks are skipped, the final report must say why.
- Do not commit when automated checks fail unless the user explicitly approves and the failure is unrelated or known.

## Git safety checks

- Always check `git status --short` before and after changes.
- Always review `git diff --stat` and `git diff`.
- Before commit, review `git diff --cached --stat` and `git diff --cached`.
- Never use `git add .`.
- Stage only expected files.
- Never force push.
- Never touch stash unless explicitly requested.

## Docs-only changes

- Docs-only commits must not change Python or UI behavior.
- Expected checks:
  - compileall modules, UI, and main;
  - pytest;
  - ruff.
- Final report must confirm no code or UI behavior changed.

## UI / PySide6 changes

Manual checks:

- app launches;
- affected tab or action opens;
- buttons restore enabled, disabled, and loading state;
- progress and log output still appears;
- no unexpected visual redesign;
- repeated clicks do not start conflicting work;
- failure path restores UI.

## Optimizer changes

Manual checks:

- use copied sample project only;
- original images are not unexpectedly deleted;
- target KB behavior is preserved or explicitly documented;
- ZIP or output size behavior is verified if touched;
- logs and progress still make sense.

## Publish / Archive changes

Manual checks:

- archive creation works on copied sample project;
- `.fla` files are excluded from ZIP by default;
- source folders and assets are not unexpectedly deleted;
- output location and ZIP naming are verified;
- delete actions affect only intended generated files;
- logs are clear.

## Folder scanning / size parsing changes

Manual checks:

- scan copied sample project only;
- source folders are not renamed or deleted;
- ZIP, export, and cache folders are ignored if expected;
- platform, subchannel, and size detection is verified;
- Cyrillic paths and paths with spaces are verified;
- ambiguous names are reported instead of guessed.

## FLA changes

Manual checks:

- use copied sample project only;
- `.fla` files are not renamed, moved, deleted, or modified;
- open by size targets intended files;
- open all targets only intended `.fla` files;
- missing files or folders produce safe logs or fallback;
- Cyrillic paths and paths with spaces are verified.

## Final report requirements

Every Codex report after a change should include:

- Summary;
- Commit hash and message if committed;
- Changed files;
- Checks with pass or fail;
- Not changed;
- Risks / notes;
- Push status.

## When to stop

- Stop if unexpected files changed.
- Stop if checks fail unexpectedly.
- Stop if Git branch or status is not expected.
- Stop if task requires destructive behavior not explicitly approved.
- Stop if Codex is unsure whether a change is behavior-changing.
