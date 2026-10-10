---
description: Run the independent validator on a board, a sheet, the simulations or the whole system
argument-hint: <channel-card|master|input-module-6p3|power|simulation|system> [sheet or focus] [deep]
---

Launch the `validator` sub-agent with this scope: $ARGUMENTS

Model (decision 150): the validator runs on Sonnet by default. If the arguments contain the word `deep`, drop that word from the scope and launch it with the model override `opus`. Use `deep` for a full board before layout, before a PCB order, and for `system` before the first full order; Sonnet for sheets, `simulation`, rechecks and narrow focuses.

Pass the scope and focus through unchanged, and add nothing from this conversation's design reasoning: the validator's value is that it checks from the files and datasheets alone. It may run for a long time; it writes its report to `docs/reviews/`.

When it returns, give the user the report path, the counts per severity and the CRITICAL and MAJOR findings, each with one line on what it would take to resolve. Do not fix anything yet: offer to add the findings to the board's `STATUS.md` (and the system items to `docs/ARCHITECTURE.md` open items), and handle fixes as normal topics, one at a time, in a `/board` or `/system` session.
