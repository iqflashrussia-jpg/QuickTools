# Project Hygiene Rules

These rules keep the repository clean and understandable.

## Must be committed

Source files:
- Python source files;
- stable configuration files;
- documentation;
- tests;
- intentional assets such as `icon.ico` and `oxipng.exe`.

## Must not be committed

Local state:
- `last_project.txt`;
- local paths;
- user-specific settings.

Generated files:
- `project_structure.txt`;
- generated reports;
- logs;
- caches;
- exported diagnostics;
- ZIP outputs;
- installer outputs.

Python/IDE artifacts:
- `.venv/`;
- `__pycache__/`;
- `*.pyc`;
- `.vscode/`;
- `.idea/`.

## Markdown documentation

Documentation is allowed and should be committed.

Important files:
- `README.md`;
- `AGENTS.md`;
- `ARCHITECTURE.md`;
- `CONTRIBUTING.md`;
- `docs/**/*.md`.

## If a generated file is already tracked

Do not delete it from disk without user approval.

Prefer:

```bash
git rm --cached project_structure.txt
git rm --cached last_project.txt
```

Then make sure `.gitignore` prevents it from being added again.
