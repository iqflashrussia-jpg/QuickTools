# Git Workflow Rules

## Core rule

One task = one logical diff.

Good examples:
- add Codex rules;
- update `.gitignore`;
- fix one parser bug;
- update one UI block;
- add one regression test.

Bad examples:
- redesign UI and fix parser in the same commit;
- cleanup whole project while fixing a button;
- rename files while changing behavior.

## Before work

Run:

```bash
git status
```

If there are existing uncommitted changes, do not overwrite them.

Ask for user direction or clearly isolate the new changes.

## Before commit

Run:

```bash
git status
git diff --stat
```

Check that the commit does not include:
- local state;
- generated files;
- unrelated files.

## Commit message style

Use short, clear messages:

```text
Add Codex project rules
Fix repository ignore rules
Update runtime dependencies
Add architecture documentation
```

## Safe cleanup

For tracked generated files:

```bash
git rm --cached project_structure.txt
git rm --cached last_project.txt
```

This removes them from Git tracking but keeps local files on disk.
