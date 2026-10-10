# Level control simulation

`run.py` checks the channel card's fader law and ducking in ngspice (Level sheet; decisions 72, 97, 102) and writes `results.txt`. Run it with `python3 simulation/level/run.py` (needs ngspice on PATH). The superdiodes use the TL072-like model from `simulation/compressor/run.py`; the fader buffer and control summer use an OPA2171-like model (no input limit at V−, output within about 0.45 V of the rails).

## Results

| Check | Result |
|---|---|
| Fader law, +10 to −60 dB (100 % to 14 % of travel) | within 1.2 dB of decision 72 (worst: −41.4 dB at 19 %, design −40 dB) |
| Bottom of the fader | about −102 dB (design −113 dB): the OPA2171 output stops about 0.45 V above −15 V |
| Ducking, SC_ENV −1 V (decision 97) | −10.10 dB at every fader position (15, 50, 75, 100 %; R217 30k, decision 153) |
| Ducking attack, SC_ENV 0 to −4 V | 40.4 dB; 90 % after 23 ms (10 ms time constant of R215 and C224) |

These are simulations with generic models: confirm on the breadboard fader test (`simulation/filter/BREADBOARD.md`).
