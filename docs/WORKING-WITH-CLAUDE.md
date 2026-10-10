# Working with Claude Code on Syntsamix

How to run development sessions so the conversation stays small and nothing gets lost between sessions. The files carry the project forward, not a long chat.

## Where things live

| What | Where |
|---|---|
| Project overview and rules for Claude | `CLAUDE.md` |
| Which board is where, order of work | `docs/CONTINUE-FROM-HERE.md` |
| Every decision, with status and area file | `docs/decisions/INDEX.md` |
| Decisions by area: current rulings | `docs/decisions/system.md`, `system-rules.md`, `channel-card.md`, `channel-card-parts.md`, `input-module.md`, `master-card.md`, `master-card-sheets.md`, `power.md`, `mechanical.md`, `process.md` |
| Decisions by area: full text (figures, sources, rejected options) | `docs/decisions/record/` (same file names; decision 154) |
| Shared schematic workflow and hard-won rules | `hardware/CLAUDE.md` |
| One board's specifics and status | `hardware/<board>/CLAUDE.md`, `hardware/<board>/STATUS.md`; checklists, cost levers and value list in `hardware/<board>/CHECKLISTS.md` |
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
| **Validator** | `/validate <scope> [deep]` (sub-agent `validator`) | its reports in `docs/reviews/` | no; reports findings by severity |
| **Cost controller** | `/cost <scope> [deep]` (sub-agent `cost-controller`) | its reports in `docs/reviews/` | no; proposes cost levers judged by the live-device principle (decision 135) |
| **Helpers** | on request in a session (sub-agents `part-facts`, `build-check`, `sim-run`, `stock-check`) | nothing (read-only) | no; return facts, check results, tables |
| **You** | | every decision | yes |

- The **board designer** stays on one board. When a choice would change a contract, a budget or an invariant, it stops and writes the question under "For /system" in the board's `STATUS.md`.
- The **architect** session picks up those flags, keeps the budgets in `ARCHITECTURE.md` traceable (each figure names its source; unbacked ones are marked **[estimate]**), records system decisions, and tells the affected boards through their `STATUS.md`. "Tidy the handoff" is its job too.
- The **validator** starts from the files and datasheets only, with none of the designer's reasoning, and assumes everything may be wrong: it rechecks pinouts against datasheets, recomputes the circuit math, reruns netlist checks, ERC and simulations, and checks the design against the decisions. It never edits the design. Its findings become normal topics in a `/board` or `/system` session.

## The session loop

1. **Start** with `/board <board> [phase]`, for example `/board power schematic` or `/board channel-card pcb`. Claude reads only the overview, that board's rows of the index and that board's files, sums up where the board stands, and raises the first open topic.
2. **Work on one board and one phase.** Claude proposes one topic at a time with a recommendation and alternatives; you decide. Decisions stay in the main conversation.
3. **End** with `/handoff`. Claude writes the outcome into the board's `STATUS.md`, the decision files and the index, runs the architecture reviewer on the changes, then shows the changes, any conflicts and a commit message. Say "commit & push" when you are happy.
4. **Clear** with `/clear` before the next task. Everything that matters is in the files now.

## When to run what

- **`/system`**: when a board's `STATUS.md` has something under "For /system"; before starting a new board or phase; every few sessions to tidy the handoff.
- **`/validate <board> deep`**: when a board's schematic is complete (before layout), and again before ordering PCBs. `/validate system` after any contract or budget change, and `/validate system deep` before the first full order.
- **`/cost <board> deep`** or **`/cost system deep`**: before layout and before each order, and whenever the cost needs a fresh look (plain `/cost` for re-pricing after part changes); it prices the BOMs (`tools/costs.py`), checks them against decision 135 (live device, not studio gear) and the E24 rule (decision 134), and proposes new savings.
- **`/cost ledger`**: to see the money spent so far against the estimate; tell Claude about each order or payment (or use `/cost ledger add ...`) so the private ledger stays complete.
- **`/validate simulation`** or **`/validate <board> <sheet>`**: for a narrower check, for example after the breadboard changes the filter values.

## Keeping a session small

- **Delegate noisy jobs.** Claude does not start sub-agents on its own; ask for them when the job has a clear input and a short answer. Each has a helper agent on a cheaper model:
  - "Check the pinout and limits of part X in a sub-agent." (`part-facts`)
  - "Run the build-and-check loop for this sheet in a sub-agent and report the problems." (`build-check`)
  - "Rerun the LCSC stock check for the master parts in a sub-agent." (`stock-check`)
  - "Run the compressor simulation in a sub-agent and give me the results table." (`sim-run`)

  Datasheets and long logs then stay out of the conversation.
- **Do not delegate design choices.** A sub-agent cannot ask you anything, so it would decide on its own.
- **Something for another board comes up?** Ask Claude to note it in that board's `STATUS.md` and handle it in that board's session.
- **Check the size** with `/context`. If a session runs long, run `/handoff` first, then `/compact <what to keep>` (for example `/compact keep the DC-DC module comparison`). When switching board or phase, prefer `/clear`.

## Models (decision 151)

Each kind of work runs on the cheapest model that does it well; the model is set in each agent's file, so nothing needs choosing by hand.

| Work | Model |
|---|---|
| `/board` and `/system` sessions: design choices with you | Opus (the session's model) |
| `architect` (in `/handoff`), `cost-controller`, `validator` | Sonnet |
| `/validate <scope> deep`: full board before layout or a PCB order, `system` before the first full order | Opus |
| `/cost <scope> deep`: before layout and before each order, `system` when looking for new levers | Opus |
| `part-facts` (datasheets: accuracy matters) | Sonnet |
| `build-check`, `sim-run`, `stock-check` (run a tool, report the output) | Haiku |

- Do not switch models in the middle of a session (`/model`): the switch drops the prompt cache, so the next turn rereads the whole conversation at full price. Sub-agents start with a fresh context, so they save without that cost.
- For a phase where everything is already decided (redrawing a sheet from settled values, PCB clean-up), you may start a fresh session with `/model sonnet` before `/board`; go back with `/model opus` (after `/clear`) for design work.
- `/board` reads only what a session start needs: the board's rows of `INDEX.md`, the invariants and open items of `ARCHITECTURE.md`, `STATUS.md` (kept short), `CHECKLISTS.md` only for layout, assembly, ordering and cost, and the board's decision files in full only when the phase changes the circuit (otherwise by number).
- `/handoff` runs the architecture reviewer only when the changes touch a contract, a budget or a shared part list; otherwise it says it skipped it.
- Hand off and `/clear` after each settled topic rather than at the end of the day: every turn rereads the whole conversation, so a long session costs more per turn as it grows.

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
