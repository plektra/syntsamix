# Continue from here

Project-level handoff, updated 2026-10-09. Read `CLAUDE.md` first. Board detail lives in each board's `STATUS.md` and `CLAUDE.md`; shared schematic workflow in `hardware/CLAUDE.md`; decisions in `docs/decisions/` (start at `INDEX.md`).

## Boards

| Board | Schematic | PCB | Status file |
|---|---|---|---|
| Input module | done, ERC clean | not started | `hardware/input-module-6p3/STATUS.md` |
| Channel card | done, ERC 0/0 (decisions 97, 98, 102 drawn) | not started (waits for the breadboard) | `hardware/channel-card/STATUS.md` |
| Master card | done, ten sheets, ERC 0/0 (decisions 97, 98, 103, 104 drawn) | not started | `hardware/master/STATUS.md` |
| Power board | done, four sheets, ERC 0/0; values confirmed, start-up ramp added | not started | `hardware/power/STATUS.md` |

Decisions 1-109; last pushed commit: see `git log -1`.

## Order of work

1. **Decision 97 and 98 board changes**: done on the channel card (with decision 102) and on the master card (2026-10-08, with decisions 103 and 104: master fader-law op amps on OPA2171s, SC_ENV from a negative DEPTH through the existing follower). Remaining before layout: the [proposed] op amp power levers and the checks in each `STATUS.md`.
2. **SSI2144 breadboard** when the parts arrive (`simulation/filter/BREADBOARD.md`); it settles the provisional filter values on the channel card.
3. **Chain cable mock-up** before the first PCB order (decision 109): header orientation, crimping and jumper length.
4. **Channel card PCB**, then the input module, master card and power board PCBs.

## System

Cross-board budgets, chain lines and invariants: `docs/ARCHITECTURE.md` (budgets rerun after decisions 102 and 103 on 2026-10-08). Mechanical contract `docs/MECHANICAL.md`: strip envelope, panel stack, card fixing and chain headers settled (decisions 106-109); still open: the rear, the master section and power board, and the heat budget. Flags from board sessions sit under "For /system" in each `STATUS.md`. Validator reports: `docs/reviews/`.

## Waiting for the user's confirmation

The **[proposed]** parts of decisions 89-94 (master card); listed in `hardware/master/STATUS.md`.

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
