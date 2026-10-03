# SSI2144 breadboard test plan

Goal: verify the simulation in `README.md` against the real chip, and fix the values the channel card schematic needs (output scale, resonance limit, drive setting). Record every measurement in the result tables below.

Reference: SSI2144 datasheet Rev 3.0 (January 2018), Figures 1 and 3. Where this plan says "per Figure 1", copy the datasheet values exactly; they set the filter's frequency scale and are not repeated here, so they cannot be copied wrong.

## 1. Shopping list

| Qty | Part | Notes |
|---|---|---|
| 3 | SSI2144 (SSOP-16) | One for the test, one for the L/R tracking test, one spare. Thonk, synthCube, Modular Addict |
| 5 | SSOP-16 to DIP adapter board, 0.65 mm pitch | Spares for soldering mistakes |
| 3 | TL072 (DIP-8) | Control summer, output stage, spare |
| 1 | NE5532 or OPA1642 (DIP-8 or on adapter) | Optional: lower-noise output stage for comparison |
| 1 set | 1% metal film resistors, E96 | Must include: 17.4 kΩ, 200 Ω (3), 330 Ω, 49.9 kΩ, 33.2 kΩ, 499 Ω, 1 kΩ, 100 kΩ, plus the values in Figures 1 and 3 |
| 1 set | C0G/NP0 capacitors, 5% | The filter capacitor values from Figure 1, plus 10 nF |
| 10 | 100 nF ceramic | Supply decoupling at each IC |
| 4 | 10 µF electrolytic, 25 V or more | Supply rail bulk decoupling |
| 2 | 10 µF film or electrolytic | Input and output coupling |
| 2 | 10 kΩ linear pot | Cutoff, spare |
| 1 | 10 kΩ pot, reverse-audio (Bourns PDB181 class) or linear | Resonance (Figure 3) |
| 3 | 10 kΩ and 50 kΩ multiturn trimmers | Cutoff offset, output gain |
| 2 | 6.3 mm jacks with short leads | Input and output |
| 1 | Solderless breadboard and jumper wire | |
| – | Flux, fine solder (0.5 mm), fine tip, magnifier | For the SSOP adapter |

Equipment:
- Dual bench supply, ±15 V, current limit about 50 mA per rail
- Audio interface with balanced line outputs and inputs (able to reach +18 dBu or more), on a computer with REW (Room EQ Wizard, free)
- True-RMS multimeter (1.228 V RMS at 1 kHz = +4 dBu)
- Oscilloscope (optional)

## 2. Build

### Chip on adapter
Flux the pads, tack two opposite corner pins, check alignment, then solder the rest or drag-solder. Inspect for bridges under magnification and check pin-to-pin continuity with the multimeter before powering.

### Power
±15 V from the bench supply, current limit 50 mA. 100 nF ceramic from each supply pin to ground right at the chip and at each op amp; 10 µF per rail at the breadboard's supply entry. Note the supply current at power-up (datasheet: about 5 mA per rail typical).

### Circuit blocks

| Block | Build |
|---|---|
| Input coupling | 10 µF in series with the input jack (stands in for the channel's 3 Hz AC coupling) |
| Input attenuator (hot drive) | 17.4 kΩ from the coupled input to SIG IN+, 200 Ω from SIG IN+ to ground: +4 dBu (1.74 V peak) becomes about ±19.7 mV |
| Medium drive jumper | Jumper that adds a resistor in parallel with the 200 Ω: 330 Ω gives 124.5 Ω (about -4 dB), 200 Ω gives 100 Ω (about -6 dB). Try both |
| SIG IN- | 200 Ω to ground, as the datasheet says for an unused input |
| Filter capacitors | Per Figure 1 |
| Cutoff control | Control summer per Figure 1 (TL072) with the 10 kΩ linear pot and a trimmer for frequency offset. The datasheet values are for ±12 V; on ±15 V check the sweep in test 1 and scale the pot's input resistor if needed. Use a fixed 1 kΩ in place of the temperature-compensating resistor (datasheet allows this) |
| Resonance | Per Figure 3, fed from +15 V. Series resistor into the Q pin: 33.2 kΩ for test 2 (allows up to about 450 µA), then 49.9 kΩ (limits to about 300 µA). Keep the 499 Ω / 10 nF from Figure 3. The Q pin is a virtual ground, so Q current = wiper voltage / series resistance: measure the wiper voltage instead of using an ammeter |
| Output | Current-to-voltage stage per Figure 1. Put a trimmer in series with the feedback resistor so the gain can be set to unity in test 5 |

## 3. Tests

Calibrate levels first: generate a 1 kHz sine from REW and set the interface output so the multimeter reads 1.228 V RMS (+4 dBu) at the breadboard input. Loop the interface output to its input with a cable and run a REW calibration so the interface's own response is removed.

### Test 1: Cutoff sweep
Sweep the frequency response with the cutoff knob at minimum, noon and maximum, resonance at zero.

| Knob | Expected cutoff | Measured -3 dB point (or -12 dB point of the 4-pole) |
|---|---|---|
| Min | about 20 Hz | |
| Noon | about 630 Hz | |
| Max | about 20 kHz | |

### Test 2: Resonance onset and limit
With the 33.2 kΩ series resistor and cutoff at about 1 kHz, raise resonance slowly until the output sine-oscillates with no input. Record the wiper voltage and compute the current. Then change to 49.9 kΩ and confirm no oscillation at full resonance.

| Measurement | Datasheet / plan | Measured |
|---|---|---|
| Q current at oscillation onset | 350 to 450 µA | |
| Max Q current with 49.9 kΩ | about 300 µA | |
| Oscillates at max with 49.9 kΩ? | No | |

### Test 3: Bass loss with resonance
Frequency response at cutoff about 1 kHz, resonance at 0, 1/3, 2/3 and full (49.9 kΩ).

| Q current | Simulated 20 Hz gain | Measured | Simulated peak | Measured |
|---|---|---|---|---|
| 0 | 0 dB | | – | |
| about 100 µA (k = 1) | -6.0 dB | | -3.7 dB | |
| about 200 µA (k = 2) | -9.5 dB | | -1.8 dB | |
| about 300 µA (k = 3) | -12.0 dB | | +3.5 dB | |

### Test 4: Distortion against level (hot drive)
100 Hz sine, resonance 0. THD+N from REW.

| Level | Sim, cutoff open | Measured, cutoff open | Sim, cutoff 1 kHz | Measured, cutoff 1 kHz |
|---|---|---|---|---|
| 0 dBu | 0.03% | | 0.53% | |
| +4 dBu | 0.08% | | 1.3% | |
| +8 dBu | 0.21% | | 3.4% | |
| +12 dBu | 0.60% | | 8.7% | |

Repeat the +4 dBu row with the medium drive jumper (both values):

| Jumper | Measured THD, cutoff open | Measured THD, cutoff 1 kHz |
|---|---|---|
| 330 Ω (about -4 dB) | | |
| 200 Ω (about -6 dB) | | |

### Test 5: Output scale
With the cutoff fully open and resonance 0, set the output trimmer so +4 dBu in gives +4 dBu out. Measure the total feedback resistance (fixed plus trimmer) with power off.

| Measurement | Value |
|---|---|
| Feedback resistance for unity gain (hot drive) | |
| Same with medium drive jumper | |

### Test 6: Noise
Terminate the input (short the jack's tip to sleeve through about 100 Ω). Measure output noise in REW, 20 Hz to 20 kHz, A-weighted, at the same unity gain setting.

| Setting | Estimated SNR at +4 dBu | Measured noise (dBu A) | Measured SNR |
|---|---|---|---|
| Hot drive | about 93 dB | | |
| Medium drive (-4 dB) | about 89 dB | | |

### Test 7: Listening
Play synths, drums and a full mix through the filter at +4 dBu. Sweep the cutoff, add resonance, push the level to +8 and +12 dBu. Compare hot and medium drive and note which sounds right as the default.

| Material | Hot drive | Medium drive | Preferred |
|---|---|---|---|
| | | | |

### Test 8: L/R tracking (optional, second chip)
Build a second core sharing the same control voltage. With both cutoffs at the same knob position, measure each one's cutoff, then adjust one offset trimmer until they match.

| Measurement | Value |
|---|---|
| Untrimmed cutoff difference (octaves) | |
| Trimmer range needed (mV at the frequency pin) | (plan: at least ±12 mV) |

## 4. After the tests

- Copy the measured values into `README.md` next to the simulated ones.
- Update `docs/DECISIONS.md`: drive default, resonance series resistor, output feedback resistance, any differences from the model.
