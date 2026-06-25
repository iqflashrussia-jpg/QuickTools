# PySide6 UI Rules

These rules protect the approved UI direction.

## General direction

The UI should remain:
- dark;
- restrained;
- clean;
- desktop-oriented;
- consistent across tabs.

## Visual principles

- Use consistent cards, spacing, typography, and button styling.
- Primary actions should be visually prominent.
- Do not make CTAs look like secondary dark buttons.
- Keep table separators and row readability.
- Avoid unnecessary nested dark rectangles.
- Keep icons visually consistent.

## Button states

Common button states:
- default;
- hover;
- pressed;
- focused;
- disabled;
- loading, only for long operations;
- current, for active navigation sections;
- checked, for toggles and filters.

## Architecture

UI files should stay in `ui_pyside6/`.

Do not move business logic into UI blocks.

Prefer reusable widgets in `common_widgets.py` when the same UI pattern repeats.

## Change rule

Do not redesign an entire screen unless the user explicitly asks for redesign.

For a UI bug, change only the affected block.
