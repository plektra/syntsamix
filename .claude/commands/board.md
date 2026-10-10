---
description: Start a focused session on one board (or the simulations) and one phase
argument-hint: <channel-card|master|input-module-6p3|power|simulation> [phase, e.g. schematic, pcb, breadboard]
---

Start a focused work session on: $ARGUMENTS

1. Resolve the board folder: `hardware/<board>/` (`input` or `input-module` means `hardware/input-module-6p3/`), or `simulation/` for simulation and breadboard work. If the argument matches nothing, list the boards from `docs/CONTINUE-FROM-HERE.md` and stop.
2. Read only these files (decision 151: keep the start-up small):
   - `docs/CONTINUE-FROM-HERE.md`
   - from `docs/decisions/INDEX.md`, not the whole file: the top up to "## All decisions" (area table and rules), the rows of the board's area files and any row still **[proposed]** (for example `grep -nE '\]\((channel-card|channel-card-parts)\.md\)|proposed|open' docs/decisions/INDEX.md`), and the sections from "Proposed but not confirmed" to the end. Read other rows only when a decision number comes up.
   - from `docs/ARCHITECTURE.md`, only the sections "Invariants" and "Open system items"; read the budgets and chain lines too when the phase touches power, the ribbons, signal levels or the panel (and always for `power`)
   - the board's `CLAUDE.md` and `STATUS.md` (for `simulation/`: `simulation/CLAUDE.md` and the relevant README); also its `CHECKLISTS.md` when the phase is layout, assembly, ordering, cost or component values
   - the board's decision files in `docs/decisions/` (`channel-card` → `channel-card.md` and `channel-card-parts.md`, `master` → `master-card.md` and `master-card-sheets.md`, `input-module-6p3` → `input-module.md`; `power` also reads decisions 40 and 80 in `system.md`): in full when the phase changes the circuit (schematic, breadboard, simulation, or no phase given); for other phases (PCB, mock-up, ordering, cost) read only the decisions that `STATUS.md`, `CHECKLISTS.md` or the topic names, by number, and read in full before any change to the circuit
   - `hardware/CLAUDE.md`, when the phase involves schematics or PCB
   Read `docs/SPEC.md`, `docs/CHAIN.md`, `docs/INPUT-MODULE.md`, `docs/MECHANICAL.md` or other boards' files only when the task needs them.
3. Reply briefly: where the board stands, any **[proposed]** items waiting for the user, and the next step for the requested phase (or, if no phase was given, the next step from `STATUS.md`).
4. Then raise the first open topic: a recommendation with alternatives, one topic at a time. Do not change files until the user answers.

If a choice would change a contract (`docs/CHAIN.md`, `docs/INPUT-MODULE.md`, `docs/MECHANICAL.md`), a budget or an invariant in `docs/ARCHITECTURE.md`, stop and say it needs a `/system` session; note it under "For /system" in the board's `STATUS.md`.

Stay on this board for the session. If something comes up for another board, offer to note it in that board's `STATUS.md` rather than working on it. Use sub-agents only when the user asks, and only for bounded jobs with a short result, through the helper agents (decision 151): `part-facts` for datasheet fact checks, `build-check` for build-and-check loops, `sim-run` for simulation runs, `stock-check` for stock and price checks. Do not use a general-purpose agent for these: it would run on the session's (Opus) model.
