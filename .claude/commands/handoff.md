---
description: Record this session's outcome in the status and decision files, then prepare the commit
argument-hint: [optional note on what to record]
---

Wrap up this session so the next one can start from the files alone. Extra note from the user: $ARGUMENTS

1. Update the `STATUS.md` of every board worked on: where it stands, what is waiting for the user's confirmation, checks before the next phase, next step. Put today's date on the "Updated" line. Remove finished items.
2. Decisions made this session: append each to its area file in `docs/decisions/` with the next free number (check `INDEX.md`), mark unconfirmed parts **[proposed]**, and add one row per decision to `INDEX.md`. When the user confirms a proposal, remove its **[proposed]** marker and update the index status.
3. Working knowledge learned the hard way: the board's `CLAUDE.md` if it is board-specific, `hardware/CLAUDE.md` if it applies to every board, `simulation/CLAUDE.md` for simulations. Keep each short.
4. If a board's status changed (schematic or PCB done, new next step), update the table and the order of work in `docs/CONTINUE-FROM-HERE.md`, and the status line in the root `CLAUDE.md` and `docs/ROADMAP.md`.
5. New part types: `docs/parts.csv`. New files: check they are covered by `REUSE.toml` and run `uvx --from 'reuse[charset-normalizer]' reuse lint`.
6. Launch the `architect` sub-agent on the working-tree changes. Report its CONFLICT and UPDATE NEEDED items to the user; resolve UPDATE NEEDED documentation items now, and leave CONFLICT items for the user to decide (a contract or invariant change belongs in a `/system` session).
7. Show `git status` and a short summary of the changes, and propose a commit message. Do not commit or push until the user says so.
8. Finally, tell the user that `/clear` is safe now that everything is in the files.
