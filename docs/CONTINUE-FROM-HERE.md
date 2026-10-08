# Continue from here

Project-level handoff, updated 2026-10-08. Read `CLAUDE.md` first. Board detail lives in each board's `STATUS.md` and `CLAUDE.md`; shared schematic workflow in `hardware/CLAUDE.md`; decisions in `docs/decisions/` (start at `INDEX.md`).

## Boards

| Board | Schematic | PCB | Status file |
|---|---|---|---|
| Input module | done, ERC clean | not started | `hardware/input-module-6p3/STATUS.md` |
| Channel card | done, ERC 0/0 | not started (waits for the breadboard) | `hardware/channel-card/STATUS.md` |
| Master card | done, ten sheets, ERC 0/0 | not started | `hardware/master/STATUS.md` |
| Power board | done, four sheets, ERC 0/0 | not started | `hardware/power/STATUS.md` |

Decisions 1-101; last pushed commit: see `git log -1`.

## Order of work

1. **Decision 97 and 98 board changes** (SC_ENV negative into the control summer's virtual earth; PFL_ACT drivers and button pull-downs to PGND): `/board channel-card schematic` and `/board master schematic` (also the R421 footprint, finding 3). Details in each `STATUS.md`. In the same sessions, before layout: the fader buffer input range (TL072 input at −15 V at the bottom of the fader) and the [proposed] op amp power levers, both under "Check before layout" in each `STATUS.md`.
2. **SSI2144 breadboard** when the parts arrive (`simulation/filter/BREADBOARD.md`); it settles the provisional filter values on the channel card.
3. **Channel card PCB**, then the input module, master card and power board PCBs.

## System

Cross-board budgets, chain lines and invariants: `docs/ARCHITECTURE.md` (no open items after decisions 96-101; decision 101 adds invariant 8, floating supply). Flags from board sessions sit under "For /system" in each `STATUS.md`. Validator reports: `docs/reviews/`.

## Waiting for the user's confirmation

The **[proposed]** parts of decisions 89-94 (master card); listed in `hardware/master/STATUS.md`.

The **[proposed]** values of decision 100 (power board); listed in `hardware/power/STATUS.md`.

The **[proposed]** op amp power levers (`docs/ROADMAP.md`, Power-cut candidates 1 and 2), checked per position in the channel and master `/board` sessions.

## Pending outside the boards

- Second Electrokit order on hold: `simulation/filter/electrokit-order-2.csv`.
- Ground-lift switch part to choose (decision 61).
- Backlog (now including mains power: external linear box or internal supply, decision 101), cost-cut and power-cut candidates: `docs/ROADMAP.md`.

## How the user likes to work

- Commit and push only when asked; pause for review before each commit.
- "Commit & push" means Claude puts the commit on `main` on origin itself; from a background worktree: `git push origin HEAD:main` (fast-forward only, rebase first if main moved, never force; allowed by the rule in `.claude/settings.json`). The user does not merge or push by hand.
- Give a recommendation with alternatives; one topic at a time; tight budget (flag cost-cut candidates).
- Mark proposals as proposed until confirmed; ask before changing a confirmed decision.
