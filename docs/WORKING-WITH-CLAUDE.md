# Working with Claude Code on Syntsamix

How to run development sessions so the conversation stays small and nothing gets lost between sessions. The files carry the project forward, not a long chat.

## Where things live

| What | Where |
|---|---|
| Project overview and rules for Claude | `CLAUDE.md` |
| Which board is where, order of work | `docs/CONTINUE-FROM-HERE.md` |
| Every decision, with status and area file | `docs/decisions/INDEX.md` |
| Decisions by area | `docs/decisions/system.md`, `channel-card.md`, `channel-card-parts.md`, `input-module.md`, `master-card.md`, `master-card-sheets.md`, `power.md`, `mechanical.md`, `process.md` |
| Shared schematic workflow and hard-won rules | `hardware/CLAUDE.md` |
| One board's specifics and status | `hardware/<board>/CLAUDE.md`, `hardware/<board>/STATUS.md` |
| Simulation notes | `simulation/CLAUDE.md` |
| System diagram, cross-board budgets, chain lines, invariants | `docs/ARCHITECTURE.md` |
| Interfaces between boards (contracts) | `docs/CHAIN.md`, `docs/INPUT-MODULE.md`, `docs/MECHANICAL.md` |
| Validator reports | `docs/reviews/` |
| Commands and sub-agents | `.claude/commands/`, `.claude/agents/` |

Boards: `channel-card`, `master`, `input-module-6p3`, `power`.

## Roles

Claude has no memory between sessions; each role is a kind of session (or sub-agent) plus the files it owns.

| Role | How you start it | Owns | Decides? |
|---|---|---|---|
| **Board designer** | `/board <board> [phase]` | that board's files, its `STATUS.md`, its decision file | proposes; you decide |
| **Architect** | `/system [topic]` | `docs/ARCHITECTURE.md`, `docs/decisions/system.md`, `CHAIN.md`, `INPUT-MODULE.md`, `MECHANICAL.md`, the root rules, the order of work | proposes; you decide |
| **Architecture reviewer** | runs automatically in `/handoff` (sub-agent `architect`) | nothing (read-only) | no; reports conflicts with contracts, budgets and invariants |
| **Validator** | `/validate <scope>` (sub-agent `validator`) | its reports in `docs/reviews/` | no; reports findings by severity |
| **Cost controller** | `/cost <scope>` (sub-agent `cost-controller`) | its reports in `docs/reviews/` | no; proposes cost levers judged by the live-device principle (decision 135) |
| **You** | | every decision | yes |

- The **board designer** stays on one board. When a choice would change a contract, a budget or an invariant, it stops and writes the question under "For /system" in the board's `STATUS.md`.
- The **architect** session picks up those flags, keeps the budgets in `ARCHITECTURE.md` traceable (each figure names its source; unbacked ones are marked **[estimate]**), records system decisions, and tells the affected boards through their `STATUS.md`. "Tidy the handoff" is its job too.
- The **validator** starts from the files and datasheets only, with none of the designer's reasoning, and assumes everything may be wrong: it rechecks pinouts against datasheets, recomputes the circuit math, reruns netlist checks, ERC and simulations, and checks the design against the decisions. It never edits the design. Its findings become normal topics in a `/board` or `/system` session.

## The session loop

1. **Start** with `/board <board> [phase]`, for example `/board power schematic` or `/board channel-card pcb`. Claude reads only the overview, the index and that board's files, sums up where the board stands, and raises the first open topic.
2. **Work on one board and one phase.** Claude proposes one topic at a time with a recommendation and alternatives; you decide. Decisions stay in the main conversation.
3. **End** with `/handoff`. Claude writes the outcome into the board's `STATUS.md`, the decision files and the index, runs the architecture reviewer on the changes, then shows the changes, any conflicts and a commit message. Say "commit & push" when you are happy.
4. **Clear** with `/clear` before the next task. Everything that matters is in the files now.

## When to run what

- **`/system`**: when a board's `STATUS.md` has something under "For /system"; before starting a new board or phase; every few sessions to tidy the handoff.
- **`/validate <board>`**: when a board's schematic is complete (before layout), and again before ordering PCBs. `/validate system` after any contract or budget change, and before the first full order.
- **`/cost <board>`** or **`/cost system`**: before layout and before each order, and whenever the cost needs a fresh look; it prices the BOMs (`tools/costs.py`), checks them against decision 135 (live device, not studio gear) and the E24 rule (decision 134), and proposes new savings.
- **`/cost ledger`**: to see the money spent so far against the estimate; tell Claude about each order or payment (or use `/cost ledger add ...`) so the private ledger stays complete.
- **`/validate simulation`** or **`/validate <board> <sheet>`**: for a narrower check, for example after the breadboard changes the filter values.

## Keeping a session small

- **Delegate noisy jobs.** Claude does not start sub-agents on its own; ask for them when the job has a clear input and a short answer:
  - "Check the pinout and limits of part X in a sub-agent."
  - "Run the build-and-check loop for this sheet in a sub-agent and report the problems."
  - "Rerun the LCSC stock check for the master parts in a sub-agent."
  - "Run the compressor simulation in a sub-agent and give me the results table."

  Datasheets and long logs then stay out of the conversation.
- **Do not delegate design choices.** A sub-agent cannot ask you anything, so it would decide on its own.
- **Something for another board comes up?** Ask Claude to note it in that board's `STATUS.md` and handle it in that board's session.
- **Check the size** with `/context`. If a session runs long, run `/handoff` first, then `/compact <what to keep>` (for example `/compact keep the DC-DC module comparison`). When switching board or phase, prefer `/clear`.

## Decisions

- Each decision has a global number that is never reused; references like "decision 81" or "item 50" stay valid.
- New decisions go into their area file and get one row in `INDEX.md` (`/handoff` does this).
- Text marked **[proposed]** is not settled until you confirm it. Confirmed decisions change only when you ask.
- `docs/CHAIN.md`, `docs/INPUT-MODULE.md`, `docs/MECHANICAL.md` and the budgets and invariants in `docs/ARCHITECTURE.md` are contracts between boards: changing them needs a confirmed decision in a `/system` session, because every board depends on them.

## Parallel sessions

Two sessions can work on different boards at once, but these files are shared and can conflict: `hardware/libs/`, the shared scripts in `hardware/channel-card/scripts/` (the master symlinks to them), `docs/parts.csv`, `docs/decisions/INDEX.md`. If you run sessions in parallel, ask each to work in its own git worktree and merge one at a time. Otherwise, one session at a time.

## Upkeep

- Every few sessions: `/system tidy the handoff` (prune finished items from the `STATUS.md` files, move confirmed proposals off the waiting lists).
- Keep the root `CLAUDE.md` short. If a board's `CLAUDE.md` passes about 5 KB, move details into its scripts README.
- If a decision file passes about 15 KB, split it further (for example `master-card-compressor.md`) and update `INDEX.md`.
