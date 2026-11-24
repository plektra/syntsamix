# Sidechain simulation

`run.py` checks the master card's sidechain LPF and the trigger-style ducker (Sidechain sheet, decision 90) in ngspice and prints the results in `results.txt`. Run it with `python3 simulation/sidechain/run.py` (needs ngspice on PATH). It reuses the TL072-like op-amp model from `simulation/compressor/run.py`.

## Results

| Check | Result |
|---|---|
| LPF range (10 kΩ + 100 kΩ dual pot, 22 nF / 47 nF) | B100K linear dual (decision 138): -3 dB at 46 Hz (CCW), 60 Hz (25 %), 85 Hz (middle), 146 Hz (75 %), 510 Hz (CW); track ±20 % moves CCW to 39-57 Hz; no peaking |
| Ducker attack (100 Hz kick, DEPTH -4 V) | 90 % in about 3 ms |
| Ducker peak with 18 loads of 30k on SC_ENV (1.67 kΩ, decision 153; follower fed back after the 100 Ω, decision 97) | -3.91 V (DECAY CCW) to -4.00 V (CW) of -4 V; never above 0 V |
| Recovery of 20 dB after the hit | 33 ms (DECAY CCW) to 0.82 s (CW) |
| Signal 3 dB below THRESHOLD | no trigger |
| THRESHOLD range (decision 199: B10K, R514 75k, R515 1k5, R516 100k load) | 0.26 V (CCW), 1.07 V (middle), 1.83 V (CW) |
| Ducking LED (decision 199) | dark at rest and up to about 2 dB (3 dB in the LED model with the higher forward voltage), about 0.36-0.38 mA at 10 dB, 0.85 mA at 20 dB, 1.8 mA at 40 dB; without the 22k across the LED about 21 uA would flow at rest; −15 V load at most 2.2 mA |
| Eurorack gate 10 V | full depth while high |

These are simulations with generic models: confirm on the breadboard before layout.
