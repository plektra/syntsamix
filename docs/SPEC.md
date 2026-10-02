# Specification v0.4 (draft)

Items marked **[confirmed]** were agreed with the user. Items marked **[proposed]** are defaults suggested during the design chat and still need confirmation. See `DECISIONS.md`.

## 1. Goals

- Live-performance mixer for synths, drum machines and modular gear **[confirmed]**
- Modular by design **[confirmed]**
- Inputs accept hot Eurorack modular levels as well as line levels, without an external attenuator **[confirmed]**
- Analog signal path **[proposed]**
- Pro-level headroom: +4 dBu nominal **[proposed]**. On ±15 V rails a single-ended stage tops out at about +20 dBu; +24 dBu is reachable only at the balanced outputs (each leg at +18 dBu) **[proposed]**

## 2. Architecture

- 4 identical stereo channel cards plugged into a backplane (power, main bus, compressor bus, AUX send buses, cue bus, sidechain bus) **[proposed]**
- Summing buses: main L/R, compressor L/R, AUX1 L/R, AUX2 L/R (8 lines), plus cue L/R (2 lines), a "PFL active" logic line and the sidechain bus **[proposed]**
- Master/compressor card **[proposed]**
- Power card, external ±15 V supply with local regulation per card **[proposed]**
- Each module is its own KiCad hierarchical sheet and PCB **[proposed]**

Signal flow per channel: input receiver and trim → filter (or bypass) → [PFL tap] → level VCA (fader + mute) → AUX sends and bus assign (main or compressor bus).

## 3. Channel strip (per stereo channel; every element is an L/R pair)

| Block | Spec | Status |
|---|---|---|
| Input | Balanced inputs | confirmed |
| Mono sources | L/MONO input: with only the L jack plugged in, the signal feeds both sides through the R jack's switch contacts. No panel switch, no balance/pan control | confirmed |
| Input connectors | 2x TRS 6.3 mm plus 2x TRS 3.5 mm in parallel (for Eurorack cables); an unbalanced TS plug works with ring and sleeve shorted | 3.5 mm confirmed, 6.3 mm proposed |
| Jack priority | The 6.3 mm jack's switch contacts disconnect its 3.5 mm partner, so plugging both never shorts two sources together; L/MONO normalling follows the same chain | proposed |
| Input level range | From -10 dBV consumer line up to Eurorack hot signals of ±12 V peak (24 Vpp), with no clipping at minimum trim | confirmed |
| Input receiver | THAT1246 at -6 dB, DC-coupled inputs as THAT recommends (availability to check) | proposed |
| Input trim | One wide trim, no pad switch: overall gain about -20 to +20 dB (input to internal +4 dBu nominal); the trim stage after the receiver spans about -14 to +26 dB | confirmed |
| Input DC blocking | AC coupling after the receiver, corner about 3 Hz; Eurorack outputs can carry DC offsets | proposed |
| Input peak LED | Per-channel peak LED to help set the trim | proposed |
| Filter | 24 dB/oct (4-pole) ladder LPF with resonance and cutoff controls | confirmed |
| Filter part | SSI2144 baseline, AS3320 fallback | confirmed |
| Filter bypass | Per-channel bypass switch around the filter | confirmed |
| Filter gain structure | "Hot" drive: +4 dBu maps to the datasheet nominal of ±20 mV at the SSI2144 input; the filter saturates musically from about +12 dBu. Make-up gain after the filter | confirmed |
| Filter tracking | One control path drives L and R, plus a frequency offset trim and a temperature-compensating resistor per chip | confirmed |
| Resonance limit | Fixed maximum Q current of about 300 µA so no chip self-oscillates | confirmed |
| Resonance bass loss | Compensate the passband gain drop that comes with resonance | confirmed |
| Level | Level fader | confirmed |
| Fader type | 60 mm, controlling a VCA (THAT 2180-class or SSI2164 quad; choose after comparing) | VCA control confirmed, part open |
| Mute | Mute; click-free via VCA | mute confirmed, method proposed |
| Bus assign | Per-channel switch: main bus or compressor bus | confirmed |
| PFL | Latching button; taps the stereo signal after the filter and before the fader VCA (so also pre-mute) onto the cue bus, and pulls the "PFL active" line | confirmed |
| AUX | Two stereo AUX sends, each a level control feeding a stereo AUX bus | confirmed |
| AUX pre/post | Post-fader by default; a PCB jumper per send selects pre-fader | confirmed |
| Cutoff CV input | Per-channel jack into the filter control summer | confirmed |
| HPF | Dropped from the prototype; reserve space for later | confirmed |

Notes on the filter (SSI2144 datasheet Rev 3.0, January 2018, verified):
- Supply ±4 V to ±16 V, absolute maximum ±18 V; datasheet specs are measured at ±12 V.
- Differential input, nominal ±20 mV, clips at ±50 mV.
- Dynamic range 92 dB A-weighted (noise floor to 1% THD).
- Frequency control -19 mV/octave, untrimmed offset up to ±10 mV (about half an octave between chips).
- Q current at oscillation 350 to 450 µA; more Q lowers the passband and bass gain.
- Current output, ±300 µA minimum; can drive an SSI2164 VCA input directly.
- SSOP-16 only. The chip is a reissue of the SSM2044 (Rossum improved ladder).
- Resonance is on the LPF only (HPF is dropped). 8 filter cores in total (4 channels x L/R).

Notes on input levels:
- Eurorack audio is typically 10 Vpp (±5 V), about +13 dBu for a sine (Doepfer A-100 technical details). Many modules swing further toward the ±12 V rails; ±10 V outputs are common. Eurorack is unbalanced, on 3.5 mm TS.
- Waveforms are often square or saw, so plan by peak voltage, not dBu. A ±10 V square wave is about +22 dBu RMS.
- Gain needed to reach +4 dBu nominal (1.74 V peak): ±5 V peak about -9 dB, ±10 V about -15 dB, ±12 V about -17 dB. Line +4 dBu needs 0 dB; -10 dBV needs about +12 dB. Weak sources get up to +20 dB.
- THAT1246 (datasheet Rev 05, verified): gain -6 dB; with ±15 V rails the output swings to about +21.1 dBu, so differential inputs up to about +27 dBu (about ±24 V peak) pass cleanly, well above any Eurorack level. Common-mode input range +31 dBu. Input impedance 24 kΩ differential and 18 kΩ common mode (±25%). Output noise -106 dBu. THAT recommends the 1243 (-3 dB) for pro +24 dBu inputs, but the 1246 suits this mixer better because of the hotter Eurorack peaks.
- A TS cable shorts ring to sleeve at the source, so the receiver still rejects ground noise between the case and the mixer (pseudo-balanced).

Notes on mono/stereo (L/MONO convention everywhere):
- Channel inputs, AUX send outputs and AUX returns all use L/MONO jacks.
- Mono handling for AUX lives on the master card, not per channel.
- Jack part with tip and ring switch contacts is still to be chosen and verified from its datasheet.

## 4. Master and compressor

- Compressor with selectable/routable sidechain input **[confirmed]**
- The compressor processes a dedicated **compressor bus**; each channel chooses main or compressor bus, and the compressor output sums into the main bus **[confirmed]**
- Sidechain has an LPF so the detector reacts mainly to bass; purpose is bass pumping **[confirmed]**
- Sidechain LPF range about 40 to 500 Hz with bypass switch **[proposed]**
- Sidechain source select: compressor bus, external jack, or a backplane bus (selected channel/AUX, for example the kick channel kept on the main bus) **[proposed]**
- Stereo-linked VCA compressor with threshold, ratio, attack, release, makeup gain **[proposed]**
- Fast attack and long adjustable release suit pumping **[proposed]**
- Master level control **[proposed]**
- AUX send outputs: L/MONO and R jacks per send; with only L plugged in, L outputs (L+R)/2 **[confirmed]**
- AUX returns: stereo, L/MONO normalled (only L plugged in feeds both sides); controls: level and a main/compressor bus switch, so for example a reverb return can pump with the kick **[confirmed]**
- Headphone output: master bus normally, cue bus automatically while any PFL is active **[confirmed]**
- PFL-active LED **[confirmed]**
- Stereo LED level meter: cue bus during PFL, master bus otherwise **[confirmed]**; scale and segment count to be defined
- Balanced stereo outputs **[proposed]**
- No solo-in-place **[confirmed]**

## 5. Performance targets (all proposed, to refine)

With the filter bypassed:
- Frequency response 20 Hz to 20 kHz within +-0.5 dB
- THD+N below 0.01% at +4 dBu
- Dynamic range above 100 dB
- Crosstalk below -80 dB

With the filter engaged:
- Dynamic range about 85 to 90 dB (limited by the SSI2144's 92 dB)
- Distortion above +12 dBu is accepted as part of the filter character

## 6. Tooling

- KiCad, driven through its MCP server **[confirmed]**
- Hierarchical schematics, custom symbol and footprint libraries, ngspice simulation, ERC/DRC checks, BOM export **[proposed]**
