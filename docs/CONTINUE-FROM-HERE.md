# Continue from here

Project-level handoff, updated 2026-10-09. Read `CLAUDE.md` first. Board detail lives in each board's `STATUS.md` and `CLAUDE.md`; shared schematic workflow in `hardware/CLAUDE.md`; decisions in `docs/decisions/` (start at `INDEX.md`).

## Boards

| Board | Schematic | PCB | Status file |
|---|---|---|---|
| Input module | done, ERC clean | not started | `hardware/input-module-6p3/STATUS.md` |
| Channel card | done, ERC 0/0; mechanical parts chosen and settled with /system 2026-10-09 (decisions 110-122); meter LEDs 0805 and op amp power levers drawn (decision 123); pot MPNs on the symbols, R184 12 k for the RESONANCE pot rating (decision 129); TFPT tempco pair (decision 130) | not started (waits for the breadboard, the SSI2144/SSI2162 RoHS declaration and the cable mock-up) | `hardware/channel-card/STATUS.md` |
| Master card | done, ten sheets, ERC 0/0; pre-layout session 2026-10-09: open points of 89-94 confirmed, DRV135 replaces the end-of-life THAT1646, TL062 levers, SMD electrolytics, both raw rails watched (decisions 125-128); RELEASE pot C100K for the pot rating (decision 131) | not started (waits for `/system mechanical` on the master section: TO-220 heatsinks, meter LED form; and the RV501 C100K dual pot) | `hardware/master/STATUS.md` |
| Power board | done, four sheets, ERC 0/0; values confirmed, start-up ramp added | not started | `hardware/power/STATUS.md` |

Decisions 1-131; last pushed commit: see `git log -1`.

## Order of work

1. **Decision 97 and 98 board changes**: done on the channel card (with decision 102) and on the master card (2026-10-08, with decisions 103 and 104: master fader-law op amps on OPA2171s, SC_ENV from a negative DEPTH through the existing follower). Remaining before layout: the checks in each `STATUS.md` (master power levers done, decision 126).
2. **SSI2144 breadboard** when the parts arrive (`simulation/filter/BREADBOARD.md`); it settles the provisional filter values on the channel card.
3. **Channel card schematic touch-up**: done 2026-10-09 (meter LEDs 0805, decision 119; power levers, decision 123).
4. **RoHS audit** (decision 122): done 2026-10-09, report `docs/reviews/2026-10-09-rohs-audit.md`. Gaps: declarations for the SSI2144, SSI2162 (channel) and the AS3046D (master; the Alpha pots are cleared by Alpha's declaration, decision 124), 25 rows with no part chosen yet, and End of Life at Mouser for the ERA-V33J102V tempco resistor on the master's R421 (the channel card replaced it with a Vishay TFPT pair, decision 130). The THAT1646 End of Life is closed by decision 125 (DRV135UA).
5. **Chain cable mock-up** before the first PCB order (decision 109): header orientation, crimping and jumper length.
6. **Channel card PCB**, then the input module, master card and power board PCBs.

## System

Cross-board budgets, chain lines and invariants: `docs/ARCHITECTURE.md` (budgets rerun after decision 123 on 2026-10-09). Mechanical contract `docs/MECHANICAL.md`: strip envelope, panel stack, card fixing and chain headers settled (decisions 106-109), jack sizes, channel meter bezel, single panel screw, underside and bottom cover (decisions 118-121); invariant 9 RoHS (decision 122); still open: the rear (rear panel, input module position, cover height and keep-out values from the mock-up), the master section and power board, and the heat budget. Flags from board sessions sit under "For /system" in each `STATUS.md`. Validator reports: `docs/reviews/`.

## Waiting for the user's confirmation

The master's proposals (89-94, power levers) were decided on 2026-10-09 with the user's delegation (decisions 125-128; review them in `hardware/master/STATUS.md`).

- **Cost (2026-10-09):** the user asked for a large cost cut, then set the frame: the prototype is 4 channel cards, maybe 2 (first trial-and-error versions); the full 16-channel console's cost stays in view for a possible product; the ladder filter stays (rejected as a fitting option). Estimates from `tools/costs.py` (prototype about €1,115 for 4 channels, €960 for 2; full console about €2,110; before VAT and shipping) and levers: `docs/ROADMAP.md`, Cost review; board levers in each `STATUS.md`. Done: Rean NYS216 jacks (decision 132); through-hole parts hand-soldered by the user (decision 133). Value selection is each board's own job (decision 134: E24 by default; off-series lists in each `STATUS.md`). Cost principle: live device, not studio gear (decision 135). Fee-free JLCPCB parts first: basic, then preferred (decision 137; candidates in the board STATUS files). Cost control: `/cost <scope>` (cost-controller sub-agent), `tools/costs.py`, and the private ledger of realized costs, `/cost ledger` (decision 136); the first Electrokit breadboard order is recorded. Open, all [proposed]: prototype fees (one JLCPCB order, the two-board minimum), and the per-channel levers for the console (op-amp receiver, fewer DG413s, cheaper and fewer trimmers).

## Pending outside the boards

- Second Electrokit order on hold: `simulation/filter/electrokit-order-2.csv`. Not needed to start the breadboard (tests 1-7 and a reduced test 10 run on the first order, `BREADBOARD.md`); release it for tests 8 and 9 and for the GPBS850N buttons (button cap prints and LED brightness). The full test 10 also needs an OPA2171 on an SOIC-8 adapter (Mouser or LCSC).
- RoHS declarations requested by the user (2026-10-09, by email) for the SSI2144 and SSI2162 (channel) and the AS3046D (master); without them these parts block the PCB order.
- Panel pots: Taiwan Alpha's RoHS II declaration (via Thonk, 2026-10-09) covers every standard Alpha pot (decision 124): the four channel pots are cleared, the master's Alpha pots get their source when chosen. Supplier declarations live in git-ignored `docs/rohs/` (not ours to publish).
- RoHS is strict for every part on every board (decision 116): record a `RoHS: <source>` in `docs/parts.csv` when choosing a part.
- Ground-lift switch part to choose (decision 61).
- Backlog (now including mains power: external linear box or internal supply, decision 101), cost-cut and power-cut candidates: `docs/ROADMAP.md`.

## How the user likes to work

- Commit and push only when asked; pause for review before each commit.
- "Commit & push" means Claude puts the commit on `main` on origin itself; from a background worktree: `git push origin HEAD:main` (fast-forward only, rebase first if main moved, never force; allowed by the rule in `.claude/settings.json`). The user does not merge or push by hand.
- Give a recommendation with alternatives; one topic at a time; tight budget (flag cost-cut candidates).
- Mark proposals as proposed until confirmed; ask before changing a confirmed decision.
