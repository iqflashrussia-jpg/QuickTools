# Contributing to QuickTools / FlowDesk

This document describes how a human developer or Codex should make safe changes.

## Working principles

- Keep changes small.
- Prefer clear code over clever code.
- Do not mix unrelated fixes.
- Preserve existing behavior unless the task asks to change it.
- Make code understandable for a future external developer.

## Before making changes

Run:

```bash
git status
```

Review the files related to the task.

Do not edit files unrelated to the task.

## During changes

- Keep UI changes inside `ui_pyside6/`.
- Keep business logic changes inside `modules/`.
- Avoid broad refactors.
- Add comments only when they explain a non-obvious reason.
- Prefer explicit names for functions and variables.

## After changes

Run at least:

```bash
python -m compileall .
```

If available:

```bash
ruff check .
pytest
```

Then provide:

```text
Summary:
Changed files:
Checks:
Risks / notes:
```

## Commit rules

Do not commit automatically.

Before a commit:
1. show `git status`;
2. show changed file list;
3. explain why each file belongs in the commit.

Do not commit:
- `.venv/`;
- `__pycache__/`;
- generated reports;
- temporary files;
- local user state;
- `last_project.txt`;
- `project_structure.txt`;
- ZIP outputs;
- installer outputs.
