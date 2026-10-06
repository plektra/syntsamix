# Compressor side-chain simulation

`run.py` builds a transistor-level ngspice model of the master card compressor's side chain (Compressor sheet, decision 89) and prints the results in `results.txt`. Run it with `python3 simulation/compressor/run.py` (needs ngspice on PATH).

## What is modelled

- **Detector:**
  - precision full-wave rectifier (TL072, 1N4148);
  - log converter on an AS3046-class matched pair, with Q1 carrying the signal and Q2 a diode-connected reference;
  - buffer, and gain -11 with the ERA-V33 temperature-compensating resistor.
- **Timing:** peak hold with a 470 Ω / 1 µF attack, and a current-mirror release set by the RELEASE pot.
- **Gain computer:** threshold and 4:1 ratio, makeup from Amount, the on/off ramp, the VC summer and the gain-reduction inverter.
- **Op-amps:** a TL072-like model (3 MHz, 13 V/µs, ±13.5 V swing).

The SSI2162 itself is not modelled: gain reduction is read from VC at 33 mV per dB.

## Results (25 °C)

| Check | Result |
|---|---|
| Static curve | 4:1 above threshold, within 0.5 dB of ideal for AMOUNT 0, 0.5 and 1 |
| Control ripple (100 Hz) | 0.08 dB |
| Temperature drift (15 to 45 °C) | 0.02 dB |
| Attack (-20 to +14 dBu step) | 63 % in 0.93 ms, 90 % in 2.2 ms |
| Release per 10 dB | 44 ms (CCW), 351 ms (middle), 1.42 s (CW) |
| On/off | smooth ramps of about 20 ms; at most 1.5 dB past the settled gain |
| Log converter at 10 kHz | stable at -30 and +18 dBu |

The threshold at AMOUNT 0 is +14.6 dBu sine peak, the channel soft-clip onset. Full AMOUNT lowers it 30 dB and adds 22 dB of makeup. 22 dB is past the SSI2162's specified +20 dB, so check it on the breadboard.

These are simulations with generic models: confirm the values on the breadboard before layout.
