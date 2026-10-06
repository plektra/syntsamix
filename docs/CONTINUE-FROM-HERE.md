# Continue from here

Project-level handoff, updated 2026-10-06. Read `CLAUDE.md` first. Board detail lives in each board's `STATUS.md` and `CLAUDE.md`; shared schematic workflow in `hardware/CLAUDE.md`; decisions in `docs/decisions/` (start at `INDEX.md`).

## Boards

| Board | Schematic | PCB | Status file |
|---|---|---|---|
| Input module | done, ERC clean | not started | `hardware/input-module-6p3/STATUS.md` |
| Channel card | done, ERC 0/0 | not started (waits for the breadboard) | `hardware/channel-card/STATUS.md` |
| Master card | done, ten sheets, ERC 0/0 | not started | `hardware/master/STATUS.md` |
| Power board | not started | not started | `hardware/power/STATUS.md` |

Decisions 1-95; last pushed commit: see `git log -1`.

## Order of work

1. **Power board schematic**: choose the DC-DC module family and the brick voltage (24 or 48 V), then draw it. Inputs in `hardware/power/STATUS.md`.
2. **SSI2144 breadboard** when the parts arrive (`simulation/filter/BREADBOARD.md`); it settles the provisional filter values on the channel card.
3. **Channel card PCB**, then the input module, master card and power board PCBs.

## System

Cross-board budgets, chain lines and invariants: `docs/ARCHITECTURE.md` (its open items: channel card power budget script to replace the 130 mA estimate, supply rating, SC_ENV scale). Flags from board sessions sit under "For /system" in each `STATUS.md`. Validator reports: `docs/reviews/`.

## Waiting for the user's confirmation

The **[proposed]** parts of decisions 72 (channel card) and 89-94 (master card); listed in the two boards' `STATUS.md`.

## Pending outside the boards

- Second Electrokit order on hold: `simulation/filter/electrokit-order-2.csv`.
- Ground-lift switch part to choose (decision 61).
- Backlog and cost-cut candidates: `docs/ROADMAP.md`.

## How the user likes to work

- Commit and push only when asked; pause for review before each commit.
- Give a recommendation with alternatives; one topic at a time; tight budget (flag cost-cut candidates).
- Mark proposals as proposed until confirmed; ask before changing a confirmed decision.
