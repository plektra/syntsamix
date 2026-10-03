# Filter gain-structure simulation

Simulates one SSI2144 filter core to check the gain structure before the channel card schematic (`CLAUDE.md`: simulate before layout).

Run: `python3 simulation/filter/run.py` (needs ngspice on PATH; tested with ngspice 47). Output of the last run: `results.txt`.

## Model and its limits

Sound Semiconductor publishes no SPICE model for the SSI2144. `ladder.lib` is a behavioural 4-pole ladder: four gm-C stages whose transconductors saturate as tanh(v / 2Vt), with resonance as feedback k from output to input (k = 4 is self-oscillation, 12 dB of feedback, as in the datasheet). It reproduces the ladder's small-signal response exactly and its large-signal saturation approximately.

What it is good for: level against distortion, the passband loss caused by resonance, and resonance compensation.

What it is not good for:
- The SSI2144 uses Rossum's "improved ladder" (SSM2044 topology), which may be more or less linear than the plain ladder model. Treat THD figures as estimates within a few dB of level.
- Noise is not modelled. The noise figures below come from the datasheet (92 dB A-weighted dynamic range, noise floor to 1% THD).
- The chip's output current scale is not modelled; the make-up gain after the filter is set on the breadboard.

Levels: "internal dBu" is the level in the channel before the filter attenuator. Two gain structures are compared:
- **hot** (confirmed, `DECISIONS.md` item 12): +4 dBu maps to ±20 mV at the chip, the datasheet nominal.
- **clean** (rejected alternative): +20 dBu maps to ±50 mV, the datasheet clip point. This puts +4 dBu at ±7.9 mV, 8 dB lower.

## Results

### Passband loss with resonance (fc = 1 kHz, small signal)

| k (Q current about k x 100 µA) | gain at 20 Hz | resonant peak | peak freq | with half compensation: 20 Hz / peak |
|---|---|---|---|---|
| 0 | 0.0 dB | – | – | 0.0 / – |
| 1 | -6.0 dB | -3.7 dB | 617 Hz | -3.0 / -0.7 dB |
| 2 | -9.5 dB | -1.8 dB | 818 Hz | -4.8 / +3.0 dB |
| 3 (max, 300 µA on a typical chip) | -12.0 dB | +3.5 dB | 928 Hz | -6.0 / +9.5 dB |
| 3.43 (300 µA on a chip that oscillates at 350 µA) | -12.9 dB | +8.1 dB | 961 Hz | -6.5 / +14.6 dB |

- The bass loss is exactly 1/(1+k): -12 dB at maximum resonance.
- Full compensation (make-up gain 1+k) restores the bass but lifts the resonant peak to about +15.5 dB above nominal, which would clip the stage after the filter (16 dB of headroom above +4 dBu). **Half compensation** (make-up gain √(1+k), half the dB loss) keeps the peak at about +9.5 dB on a typical chip and is the practical choice.
- At the 300 µA limit, the chip spread (oscillation at 350 to 450 µA) moves k between about 2.7 and 3.4; the worst case still stays below oscillation.

### THD against level, filter open (fc = 20 kHz, k = 0, 100 Hz tone)

| internal dBu | -10 | -6 | 0 | +4 | +8 | +12 | +16 | +20 |
|---|---|---|---|---|---|---|---|---|
| hot | 0.003% | 0.008% | 0.03% | 0.08% | 0.21% | 0.60% | 2.1% | 10% |
| clean | <0.001% | 0.001% | 0.005% | 0.01% | 0.03% | 0.08% | 0.20% | 0.59% |

### THD against level, cutoff lowered (fc = 1 kHz, k = 0, 100 Hz tone)

| internal dBu | -10 | -6 | 0 | +4 | +8 | +12 | +16 | +20 |
|---|---|---|---|---|---|---|---|---|
| hot | 0.05% | 0.13% | 0.53% | 1.3% | 3.4% | 8.7% | 19% | 26% |
| clean | 0.008% | 0.02% | 0.08% | 0.21% | 0.53% | 1.3% | 3.4% | 8.6% |

A ladder stage distorts little while the signal is far below cutoff (each stage follows its input) and more as the signal approaches cutoff. So distortion depends on where the cutoff is, not only on level.

### THD at +4 dBu with resonance (hot, fc = 1 kHz, 100 Hz tone)

k = 0: 1.3%, k = 1: 0.23%, k = 2: 0.07%, k = 3: 0.03%. The resonance feedback linearises the passband (and lowers its level).

### Noise (from the datasheet, not simulated)

The datasheet's 92 dB dynamic range runs from the noise floor to 1% THD. In the model, 1% THD with the cutoff lowered sits at about +3 dBu (hot) or +11 dBu (clean). That puts the noise floor at about -89 dBu (hot) or -81 dBu (clean), so the SNR at +4 dBu with the filter engaged is about **93 dB (hot)** or **85 dB (clean)**, A-weighted. Both meet the 85 to 90 dB target for the engaged filter.

### L/R tracking trim (from the datasheet, calculated)

Untrimmed frequency-control offset up to ±10 mV at -19 mV/octave is up to ±0.53 octave between chips. The per-chip trim must inject at least ±12 mV at the frequency control pin (with margin).

## Conclusions

1. **Hot drive works but is more coloured than the spec assumed.** With the cutoff open, +4 dBu gives under 0.1% THD. With the cutoff lowered toward the signal, it gives about 1.3% at +4 dBu and saturates clearly from about +8 dBu, not +12 dBu as `SPEC.md` assumed. The datasheet's "nominal ±20 mV" lines up with its 1%-THD reference, which is consistent with this.
2. **The trade is about 8 dB of SNR for about 6x less distortion.** Hot: about 93 dB SNR, about 1.3% THD at nominal with the cutoff low. Clean: about 85 dB, about 0.2%.
3. **Use half resonance compensation**, scaled with the Q control: passband loss at maximum Q drops from -12 dB to -6 dB and the resonant peak stays within the stage's headroom.
4. **Bench verification is required** for the real chip's distortion, noise and output scale before the channel card layout.
