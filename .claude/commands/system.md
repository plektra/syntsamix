---
description: Architecture session - cross-board decisions, interface contracts, budgets and project rules
argument-hint: [topic, e.g. "power budget", "SC_ENV scale", "tidy the handoff"]
---

This is a system (architecture) session. Topic from the user: $ARGUMENTS

You own the project's constitution in this session: `docs/ARCHITECTURE.md` (system diagram, cross-board budgets, chain lines, invariants), `docs/decisions/system.md`, the interface contracts `docs/CHAIN.md` and `docs/INPUT-MODULE.md`, the rules in the root `CLAUDE.md`, and the order of work in `docs/CONTINUE-FROM-HERE.md` and `docs/ROADMAP.md`.

1. Read: `docs/ARCHITECTURE.md`, `docs/CONTINUE-FROM-HERE.md`, `docs/decisions/INDEX.md`, `docs/decisions/system.md`, `docs/CHAIN.md`, `docs/INPUT-MODULE.md`, and every `hardware/*/STATUS.md`. Read board decision files, schematic scripts or budget scripts only where the topic needs them.
2. Reply briefly: anything in the board `STATUS.md` files that touches a contract, a budget or an invariant (flags left by board sessions), budgets in `ARCHITECTURE.md` that are out of date or still **[estimate]**, and open system items. Then the topic (or, with no topic, the most important of these).
3. Work one topic at a time: a recommendation with alternatives; the user decides. A change to a contract or an invariant is a decision: record it in `docs/decisions/system.md` (next free number, row in `INDEX.md`), then update `ARCHITECTURE.md` and the contract document together, and add a note to the `STATUS.md` of every board that must follow.
4. Keep budgets traceable: every figure in `ARCHITECTURE.md` names its source (decision, script, measurement); mark unbacked figures **[estimate]**.
5. "Tidy the handoff": prune finished items in the `STATUS.md` files, move confirmed proposals off the waiting lists (remove their **[proposed]** markers and update `INDEX.md`), keep the root `CLAUDE.md` short, and split decision files past about 15 KB.

Do not do board design work here (drawing sheets, layout); hand it to a `/board` session through that board's `STATUS.md`. End with `/handoff`.
