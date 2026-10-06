---
description: Start a focused session on one board (or the simulations) and one phase
argument-hint: <channel-card|master|input-module-6p3|power|simulation> [phase, e.g. schematic, pcb, breadboard]
---

Start a focused work session on: $ARGUMENTS

1. Resolve the board folder: `hardware/<board>/` (`input` or `input-module` means `hardware/input-module-6p3/`), or `simulation/` for simulation and breadboard work. If the argument matches nothing, list the boards from `docs/CONTINUE-FROM-HERE.md` and stop.
2. Read only these files:
   - `docs/CONTINUE-FROM-HERE.md`
   - `docs/decisions/INDEX.md`
   - `docs/ARCHITECTURE.md`
   - the board's `CLAUDE.md` and `STATUS.md` (for `simulation/`: `simulation/CLAUDE.md` and the relevant README)
   - the board's decision file in `docs/decisions/` (`master` → `master-card.md`, `input-module-6p3` → `input-module.md`; `power` also reads decisions 40 and 80 in `system.md`)
   - `hardware/CLAUDE.md`, when the phase involves schematics or PCB
   Read `docs/SPEC.md`, `docs/CHAIN.md`, `docs/INPUT-MODULE.md` or other boards' files only when the task needs them.
3. Reply briefly: where the board stands, any **[proposed]** items waiting for the user, and the next step for the requested phase (or, if no phase was given, the next step from `STATUS.md`).
4. Then raise the first open topic: a recommendation with alternatives, one topic at a time. Do not change files until the user answers.

If a choice would change a contract (`docs/CHAIN.md`, `docs/INPUT-MODULE.md`), a budget or an invariant in `docs/ARCHITECTURE.md`, stop and say it needs a `/system` session; note it under "For /system" in the board's `STATUS.md`.

Stay on this board for the session. If something comes up for another board, offer to note it in that board's `STATUS.md` rather than working on it. Use sub-agents only when the user asks, and only for bounded jobs with a short result (datasheet fact checks, build-and-check loops, simulation runs, stock checks).
