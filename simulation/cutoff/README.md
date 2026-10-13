# Cutoff summer clamp

DC model of the channel card's cutoff summer U107A (filter sheet) with the back-to-back zener clamp D184/D185 of decision 165. Run `python3 simulation/cutoff/run.py`; the output is kept in `results.txt`.

## Why

The SSI2144 datasheet (Rev 3.0, p2) specifies the frequency pin from −120 to +150 mV and gives no absolute maximum for it; above about +175 mV the ladder current falls below the output amplifier's bias, the filter passes nothing and recovers only at about +135 mV, possibly with a thump (p5). Unclamped, the summer swings to about ±13.5 V, which with the 100k / 1k divider and the offset trim reaches about ±165 mV at the pin: past the specified range on both sides and about 10 mV from the dropout. Adding a CV to the pot (and chaining channels, decision 165) makes that easy to reach.

## Model

Total cutoff control (pot plus CV, in CV volts) into 100k; V/oct feedback 182k / 192k / 202k (RV182 trimmed for a −18 / −19 / −20 mV/oct chip); 22p; two BZT52 zeners back to back across the feedback; TL072-like op amp (as `compressor/run.py`); 100k / 1k divider and 470k offset trim at ±10 mV. Zener voltages from the hongjiacheng BZT52 datasheet Rev 2.1 (at 5 mA); the knee below 0.5 mA is not specified, so the breakdown emission coefficient NBV is swept over 2, 4 and 6.

## Outcome

| Zener | Worst error inside the pot range | FCV clamp | Pin extremes (trim ±10 mV) |
|---|---|---|---|
| none | — | ±13.5 V | ±134 mV before the trim, up to ±165 mV with it |
| C9V1 | up to 0.94 oct | ±8.7-10.0 V | ±96-109 mV |
| C10 | up to 0.56 oct | ±9.5-10.9 V | ±104-118 mV |
| **C11 (chosen)** | **≤ 0.015 oct typical knee; 0.19 oct in the worst corner** | **±10.5-12.0 V** | **±113-128 mV** |
| C12 | ≤ 0.019 oct | ±11.4-13.0 V | ±123-138 mV (past the recovery level) |

The worst C11 corner stacks the low end of the zener tolerance, the softest knee and a −20 mV/oct chip, and affects only the last stretch of the sweep. With C11 the low-cutoff side stays below the +135 mV recovery level and about 47 mV clear of the dropout; the high-cutoff side may reach about 8 mV past −120 mV, where the datasheet describes no failure, only the end of its guaranteed control current. Breadboard test 13 (`filter/BREADBOARD.md`) checks the real knee and the dropout.
