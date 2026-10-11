---
description: Compact progress overview of every board (or one) and what to work on next
argument-hint: [channel-card|master|input-module-6p3|power|simulation]
model: sonnet
---

Show a compact status overview. Scope from the user (empty means every board): $ARGUMENTS

This is read-only: do not change files, start sub-agents or raise design topics.

1. Read only:
   - `docs/CONTINUE-FROM-HERE.md` (board table, order of work, waiting items)
   - each board's `STATUS.md` in `hardware/*/` (or just the named board's; `input` or `input-module` means `input-module-6p3`, `simulation` means `simulation/CLAUDE.md` and `simulation/filter/BREADBOARD.md`)
   - `git branch --no-merged main` and `git log -1 --format='%h %ad %s' --date=short`
2. Reply in at most about 25 lines, in this shape and nothing more:

   **Boards** (one row per board in scope)

   | Board | Schematic | PCB | Blocked by |
   |---|---|---|---|

   Keep each cell to a few words (for example "done, ERC 0/0"; "not started"; "breadboard, SSI2144 RoHS"). No decision histories, figures or dates in the table.

   **Next** (3-5 numbered items from the order of work and the boards' "Next", most urgent first, each one line with the command to start it, for example `/board channel-card breadboard` or `/system mechanical`)

   **Waiting on you**: confirmations and **[proposed]** items, one line each with the board and decision numbers; "none" if there are none.

   **Waiting on others**: declarations, deliveries, orders, one line each.

   **Flags**: open "For /system" items, and any branch not merged into main (its STATUS.md may be ahead of main's). Leave the section out if there are none.

   End with one line: the last commit and today's cost estimate from `CONTINUE-FROM-HERE.md` (4 / 8 / 16 channels).
3. Do not explain or comment beyond that shape. If a STATUS file contradicts `CONTINUE-FROM-HERE.md`, trust the more recently updated one and say so in one line under Flags.
