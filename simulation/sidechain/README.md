# Sidechain simulation

`run.py` checks the master card's sidechain LPF and the trigger-style ducker (Sidechain sheet, decision 90) in ngspice and prints the results in `results.txt`. Run it with `python3 simulation/sidechain/run.py` (needs ngspice on PATH). It reuses the TL072-like op-amp model from `simulation/compressor/run.py`.

## Results

| Check | Result |
|---|---|
| LPF range (10 kΩ + 100 kΩ dual pot, 22 nF / 47 nF) | -3 dB at 46 Hz (CCW), 255 Hz (middle), 510 Hz (CW); no peaking |
| Ducker attack (100 Hz kick, DEPTH -4 V) | 90 % in about 3 ms |
| Ducker peak with 18 loads of 30k1 on SC_ENV (1.7 kΩ; follower fed back after the 100 Ω, decision 97) | -3.91 V (DECAY CCW) to -4.00 V (CW) of -4 V; never above 0 V |
| Recovery of 20 dB after the hit | 33 ms (DECAY CCW) to 0.82 s (CW) |
| Signal 3 dB below THRESHOLD | no trigger |
| Eurorack gate 10 V | full depth while high |

These are simulations with generic models: confirm on the breadboard before layout.
