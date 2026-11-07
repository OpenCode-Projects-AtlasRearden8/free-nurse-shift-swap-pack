# STATUS.md — Nurse Shift-Swap Pack

## What was built

A free, print-ready **nurse shift-swap pack** (education only, never medical advice):
kind request scripts for texts, request emails for colleague + manager, a
unit-approval checklist, a coverage-math one-pager, swap-confirmation tracker cards,
and thank-you coupons — in Markdown (`docs/`) plus print-ready HTML (`print/`), with a
build script that assembles one combined packet with a cover page. All templates use
neutral placeholders only (`[Name]`, `[Date]`, `[Unit]`); no hospital names.

Distinct from `free-nurse-week-appreciation-pack` (whole-unit thanks) and
`night-shift-survival-guide` (nurse endurance).

## How to run

```bash
python3 build.py                                  # builds _build/nurse-shift-swap-packet.html
python3 -m unittest discover -s tests -v          # runs the test suite
```

Python 3, stdlib only — no dependencies to install.

## Verification results

Last full run: 2026-11-07, Python 3.13.5.

- `python3 build.py` — succeeds; writes `_build/nurse-shift-swap-packet.html`
  (~26.7 KB, cover + all 6 sheets, CSS inlined so it is fully self-contained).
- `python3 -m unittest discover -s tests -v` — **10/10 tests pass (OK)**, covering:
  - structure: every promised file exists (README, LICENSE, STATUS, build.py,
    styles.css, 6 markdown docs, 6 print sheets);
  - LICENSE contains the exact line `Copyright (c) 2026 Asdale Dynamics, LLC` and
    MIT text; README credits Asdale Dynamics, LLC;
  - every doc carries an education-only / "not medical advice" disclaimer;
  - docs use only neutral `[Placeholder]`s (no invented hospital/facility names);
  - key content checks per doc, plus cross-references between pack members;
  - explicit distinction from `free-nurse-week-appreciation-pack` (whole-unit
    thanks) and `night-shift-survival-guide` (endurance) in the README;
  - every HTML sheet parses with balanced tags and links the shared stylesheet;
  - built packet contains cover + all six sheets, no external CSS dependency,
    includes `@page` print rules.

## Known gaps / future ideas

- Individual HTML sheets keep `styles.css` external (one small extra file when printing
  singles); the built packet inlines everything for single-file sharing.
- No .docx / editable-formats exports; ASCII card art relies on a monospace font.
- Coupons and cards are one-per-page style layouts, not n-up print imposition.
- Percentage math in the coverage doc uses a standard 3×12 week; schedulers with
  different workweeks should adapt the illustration.

## Maintainer notes

- License: MIT, `Copyright (c) 2026 Asdale Dynamics, LLC` (exact line in LICENSE).
- README credits Asdale Dynamics, LLC. No secrets, API keys, or personal data in files.
