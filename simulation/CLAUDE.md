# Simulation

ngspice models and results. Each folder has a `run.py` (or netlists), a `results.txt` and a `README.md`.

- `filter/`: SSI2144 behavioural model and gain structure (decisions 12, 50); also the breadboard plan (`BREADBOARD.md`), its schematic, layout and order files.
- `compressor/`: detector and gain computer (decision 89).
- `sidechain/`: sidechain LPF and ducker (decision 90).

Working knowledge:
- `compressor/run.py` and `sidechain/run.py` share a TL072-like op-amp model (GBW from 53 pF, about ±0.69 mA output current limit).
- AC `.measure` needs `.save v(node)`; `vm()`/`vdb()` give a harmless parse warning. Avoid the node name `in`.
- Record outcomes in the decision files (`docs/decisions/`) and keep `results.txt` in sync with the scripts.
