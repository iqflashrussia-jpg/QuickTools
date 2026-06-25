# Codex Safe Commit Rules

Codex must follow this checklist before preparing any commit.

## Checklist

1. Run:

```bash
git status
```

2. Review changed files.

3. Exclude files that should not be committed:
   - local state;
   - generated reports;
   - caches;
   - temporary files;
   - `.venv/`;
   - ZIP outputs;
   - installer outputs.

4. Run checks when possible:

```bash
python -m compileall .
```

If configured:

```bash
ruff check .
pytest
```

5. Present a commit summary to the user.

## Required final report

```text
Commit candidate:
- file 1 — reason
- file 2 — reason

Excluded:
- file 1 — reason

Checks:
- command — result

Suggested commit message:
...
```

## Never do this

- Never commit automatically without user approval.
- Never claim tests passed without running them.
- Never include unrelated files because they were already modified.
- Never hide failed checks.
