---
description: Run the cost controller on a board or the whole system, or show and record realized costs
argument-hint: <channel-card|master|input-module-6p3|power|system> [focus] | ledger [add ...]
---

Arguments: $ARGUMENTS

**If the first argument is `ledger`:** this is about realized costs (decision 136), not a review; do not start a sub-agent.
- `ledger` alone: run `python3 tools/costs.py ledger` and `python3 tools/costs.py estimate` (4, 8 and 16 channels; `--channels N` for channel count the user names), and show the realized totals by category, board and supplier next to the estimate.
- `ledger add ...` or a description of an order or payment: collect date, supplier, order reference, category (parts, pcb, assembly, panels, mechanical, tools, shipping, tax, other), board (or `system`), amount and currency, asking the user only for what is missing; then run `python3 tools/costs.py ledger add ...` and show the new total. Several orders at once are fine. The ledger is private (git-ignored); never copy its entries into tracked files.

**Otherwise:** launch the `cost-controller` sub-agent with this scope and focus, passed through unchanged. Add nothing from this conversation's design reasoning: like the validator, it works from the files, the prices and decision 135 alone. It may run for a long time; it writes its report to `docs/reviews/`.

When it returns, give the user the report path, the estimate totals for 4, 8 and 16 channels, and the largest levers (prototype and console separately), each with its saving and trade-off. Do not change anything yet: offer to add the prices it found to `docs/costs/prices.csv`, and the accepted levers to the boards' `STATUS.md` ("Cost-cut levers"), and handle each lever as a normal topic, one at a time, in a `/board` or `/system` session.
