# QuickTools / FlowDesk Architecture

This document describes the intended architecture of the project so that future developers and AI coding agents can understand how to work with the codebase.

## Application type

QuickTools / FlowDesk is a Windows desktop application written in Python.

The current UI stack is PySide6.

## Entry point

`main_pyside6.py` is the application entry point.

It is responsible for:
- creating the Qt application;
- creating the main window;
- loading the start page;
- switching to main tabs after project selection;
- saving and loading the last selected project path.

It should not become a large business-logic file.

## UI layer

Directory:

```text
ui_pyside6/
```

Purpose:
- desktop interface;
- tabs;
- reusable widgets;
- styling;
- icons;
- user interactions.

UI code can call functions/classes from `modules/`, but should not contain heavy file-processing logic.

Examples of UI responsibilities:
- render forms;
- show buttons and progress;
- collect user input;
- display logs and results;
- call business logic.

## Business logic layer

Directory:

```text
modules/
```

Purpose:
- file operations;
- archive creation;
- image optimization;
- project creation;
- folder scanning;
- settings detection;
- renaming;
- FLA helper operations.

Business logic should not depend on PySide6 widgets.

Good business logic can be called from:
- the UI;
- a CLI/script;
- tests.

## Local state

`last_project.txt` stores the last selected local project path.

This is local user state and should not be committed.

Future improvement:
- move local state to an application data directory;
- keep repository root clean from user-specific paths.

## Generated files

Generated files must not be treated as source of truth.

Examples:
- `project_structure.txt`;
- reports;
- temporary ZIP files;
- logs;
- caches;
- exported diagnostics.

If a generated file is useful for debugging, it may be created locally, but should not be committed unless explicitly requested.

## External tools

`oxipng.exe` is an external optimizer binary intentionally stored in the repository.

Do not remove it unless the optimization workflow is changed deliberately.

## Dependency management

`requirements.txt` must describe the packages required to run the current app.

When imports change, dependencies must be reviewed.
