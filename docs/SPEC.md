# Specification v0.6 (draft)

Items marked **[confirmed]** were agreed with the user. Items marked **[proposed]** are defaults suggested during the design chat and still need confirmation. See `DECISIONS.md`.

## 1. Goals

- Live-performance mixer for synths, drum machines and modular gear **[confirmed]**
- Modular by design **[confirmed]**
- Relatively tight budget: prefer cost-effective parts where the audible difference is small **[confirmed]**
- Channel strips can be added one at a time as needed. Each stereo channel card is self-contained and has no direct dependency on any other channel card; it talks only to the shared buses **[confirmed]**
- Inputs accept hot Eurorack modular levels as well as line levels, without an external attenuator **[confirmed]**
- Analog signal path **[confirmed]**
- Pro-level headroom: +4 dBu nominal. On ±15 V rails a single-ended stage tops out at about +20 dBu; +24 dBu is reachable only at the balanced outputs (each leg at +18 dBu) **[confirmed]**

## 2. Architecture

- Identical stereo channel cards, 1 to 16 (the prototype has 4), daisy-chained by ribbon cables, with the master card at one end. No backplane PCB **[confirmed]**
- Each channel card has identical IN and OUT connectors wired straight through: a 34-pin IDC audio ribbon (buses, logic lines, interleaved audio grounds, spares) and a keyed 8-pin IDC power ribbon (2× V+, 2× V−, 4× ground; 10- and 16-pin avoided so Eurorack cables cannot be plugged in) **[confirmed]**
- Chain power: unregulated about ±20 V nominal, entering at the master card; each card regulates its own ±15 V; audio ground and power ground on separate conductors **[confirmed]**
- Pinouts, signal definitions and grounding rules: see `CHAIN.md` **[confirmed]**
- Summing buses: main L/R, compressor L/R, AUX1 L/R, AUX2 L/R (8 lines), plus cue L/R (2 lines), a "PFL active" logic line and the sidechain bus (pinout in `CHAIN.md`) **[confirmed]**
- Channel independence rules: every slot is identical (no slot-specific signals); audio buses are summed on the master card, so adding a card only adds a source; logic lines such as "PFL active" are wired-OR; no part is shared between channel cards; each card regulates its own supply **[confirmed]**
- Expansion by the chain: adding a channel means adding one card and one pair of ribbon cables **[confirmed]**
- Master/compressor card **[confirmed]**
- Power card / external supply delivering unregulated about ±20 V into the power chain at the master card; supply rating for 16 cards is open **[open]**
- Each module is its own KiCad project with hierarchical sheets and its own PCB **[confirmed]**

Signal flow per channel: input receiver and trim → filter (or bypass) → [PFL, meter and SC send tap] → level VCA (fader + mute) → AUX sends and bus assign (main or compressor bus).

## 3. Channel strip (per stereo channel; every element is an L/R pair)

| Block | Spec | Status |
|---|---|---|
| Input | Balanced inputs | confirmed |
| Mono sources | L/MONO input: with only the L jack plugged in, the signal feeds both sides through the R jack's switch contacts. No panel switch, no balance/pan control | confirmed |
| Input connectors | 2x 6.3 mm TRS (L/MONO and R), balanced; an unbalanced TS plug works with ring and sleeve shorted, so Eurorack gear connects with a 3.5 mm TS to 6.3 mm TS cable. The R jack needs switch contacts on tip and ring for L/MONO normalling (part to be chosen from datasheets). All jacks on the mixer are 6.3 mm | confirmed |
| Input level range | From -10 dBV consumer line up to Eurorack hot signals of ±12 V peak (24 Vpp), with no clipping at minimum trim | confirmed |
| Input receiver | AD8273 dual difference amplifier at G = ½ (-6 dB), one chip per card for L and R | confirmed; DC-coupled inputs confirmed |
| Input trim | One wide trim, no pad switch: overall gain about -20 to +20 dB (input to internal +4 dBu nominal); the trim stage after the receiver spans about -14 to +26 dB | confirmed |
| Input DC blocking | AC coupling after the receiver, corner about 3 Hz; Eurorack outputs can carry DC offsets | confirmed |
| Level meter | 8-segment mono LED meter (louder of L/R), post-filter and pre-fader (same point as PFL): -30, -20, -10, -5, 0, +3, +6, clip, relative to +4 dBu nominal. Peak-reading with a 1 to 2 s fall. Peak detector plus comparators; low-current LEDs returning to power ground. Replaces the peak LED | confirmed |
| Filter | 24 dB/oct (4-pole) ladder LPF with resonance and cutoff controls | confirmed |
| Filter part | SSI2144 baseline, AS3320 fallback | confirmed |
| Filter bypass | Per-channel bypass switch around the filter | confirmed |
| Filter gain structure | "Hot" drive: +4 dBu maps to the datasheet nominal of ±20 mV at the SSI2144 input; the filter saturates musically from about +12 dBu. Make-up gain after the filter | confirmed |
| Filter tracking | One control path drives L and R, plus a frequency offset trim and a temperature-compensating resistor per chip | confirmed |
| Resonance limit | Fixed maximum Q current of about 300 µA so no chip self-oscillates | confirmed |
| Resonance bass loss | Compensate the passband gain drop that comes with resonance | confirmed |
| Level | Level fader | confirmed |
| Fader type | Linear 60 mm fader (Bourns PTA6043-2015DPB103) generating the control voltage for an SSI2162 dual VCA (one chip per card covers L and R); a resistor network shapes a console-style dB law | confirmed |
| Fader range | +10 dB at the top, -∞ at the bottom (the VCA's -100 dB attenuation, with the control overdriven at the end stop) | confirmed |
| Fader scale | 0 dB at about 75% of travel; markings +10, +5, 0, -5, -10, -20, -30, -40, -60, -∞ | confirmed |
| Mute | Mute; click-free via VCA | confirmed |
| Bus assign | Per-channel switch: main bus or compressor bus | confirmed |
| SC send | Button: adds L+R to the mono sidechain bus, tapped at the same point as PFL (pre-fader, pre-mute) | confirmed |
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
- Resonance is on the LPF only (HPF is dropped). Two filter cores per channel card (8 in the 4-channel prototype).

Notes on input levels:
- Eurorack audio is typically 10 Vpp (±5 V), about +13 dBu for a sine (Doepfer A-100 technical details). Many modules swing further toward the ±12 V rails; ±10 V outputs are common. Eurorack is unbalanced, on 3.5 mm TS.
- Waveforms are often square or saw, so plan by peak voltage, not dBu. A ±10 V square wave is about +22 dBu RMS.
- Gain needed to reach +4 dBu nominal (1.74 V peak): ±5 V peak about -9 dB, ±10 V about -15 dB, ±12 V about -17 dB. Line +4 dBu needs 0 dB; -10 dBV needs about +12 dB. Weak sources get up to +20 dB.
- AD8273 (Analog Devices, datasheet Rev B; figures from datasheet excerpts, full PDF still to read directly): dual, internal precision resistors, G = ½ or 2, ±2.5 V to ±18 V supplies. At ±15 V and G = ½: input voltage range about ±40.5 V (−3VS + 4.5 to +3VS − 4.5), output noise 26 nV/√Hz at 1 kHz (about -106 dBu over 20 kHz if flat), CMRR 77 dB minimum, gain error 0.05% maximum, THD+N 0.00025%. Input resistance not yet confirmed. Active part, about $4.
- Earlier candidate THAT1246 (datasheet Rev 05, verified; replaced because of supply risk and because the AD8273 is a dual): gain -6 dB; with ±15 V rails the output swings to about +21.1 dBu, so differential inputs up to about +27 dBu (about ±24 V peak) pass cleanly, well above any Eurorack level. Common-mode input range +31 dBu. Input impedance 24 kΩ differential and 18 kΩ common mode (±25%). Output noise -106 dBu. THAT recommends the 1243 (-3 dB) for pro +24 dBu inputs, but the 1246 suits this mixer better because of the hotter Eurorack peaks.
- A TS cable shorts ring to sleeve at the source, so the receiver still rejects ground noise between the case and the mixer (pseudo-balanced).

Notes on mono/stereo (L/MONO convention everywhere):
- Channel inputs, AUX send outputs and AUX returns all use L/MONO jacks.
- Mono handling for AUX lives on the master card, not per channel.
- Jack part with tip and ring switch contacts is still to be chosen and verified from its datasheet.

## 4. Master and compressor

- Compressor with selectable/routable sidechain input **[confirmed]**
- The compressor processes a dedicated **compressor bus**; each channel chooses main or compressor bus, and the compressor output sums into the main bus **[confirmed]**
- Sidechain has an LPF so the detector reacts mainly to bass; purpose is bass pumping **[confirmed]**
- Sidechain LPF adjustable about 40 to 500 Hz, 12 dB/octave, with bypass switch **[confirmed]**
- Sidechain source: 3-position switch INT (the compressor bus itself, L+R) / BUS (the mono sidechain bus) / EXT (external jack) **[confirmed]**
- Channels feed the sidechain bus through a per-channel SC send button, tapped after the filter and before fader and mute (same point as PFL and the meter), so a muted channel can still trigger the pumping ("ghost triggering"). The master card never addresses a specific slot **[confirmed]**
- EXT sidechain input: 6.3 mm jack, DC-coupled, accepts audio and Eurorack envelopes or gates up to ±12 V **[confirmed]**
- SC listen button: sends the filtered sidechain signal to the cue bus (headphones) and pulls the PFL-active line **[confirmed]**
- Stereo-linked VCA compressor (SSI2162) with a performance control set **[confirmed]**:
  - **Amount:** one knob that lowers the threshold and raises makeup gain together, through the VCA control circuit
  - **Release ("pump"):** recovery time after each hit
  - **Mix:** dry/wet blend of the uncompressed and compressed compressor bus (parallel compression)
  - **On/off button:** click-free bypass
  - **Gain-reduction LEDs:** about 5 segments
  - Sidechain LPF frequency and bypass, and the sidechain source selector (below)
- Preset inside (trimmers or jumpers, no panel knobs): fast attack tuned for pumping, fixed ratio (about 4:1), makeup range tied to Amount **[confirmed]**
- Master level: linear pot controlling an SSI2162 VCA (accurate L/R tracking) **[confirmed]**
- Headphone volume knob **[confirmed]**
- AUX send outputs: L/MONO and R jacks per send; with only L plugged in, L outputs (L+R)/2 **[confirmed]**
- AUX returns: stereo, L/MONO normalled (only L plugged in feeds both sides); controls: level and a main/compressor bus switch, so for example a reverb return can pump with the kick **[confirmed]**
- Headphone output: master bus normally, cue bus automatically while any PFL is active **[confirmed]**
- PFL-active LED **[confirmed]**
- Stereo LED level meter on the master bus after the master level control (no cue switching): 12 segments per side, -30, -20, -15, -10, -6, -3, 0, +3, +6, +9, +12, clip; 0 = +4 dBu; clip about +17 dBu internal (+23 dBu at the balanced outputs); peak-reading with a 1 to 2 s fall **[confirmed]**
- Balanced stereo outputs on 6.3 mm TRS **[confirmed]**
- No solo-in-place **[confirmed]**

## 5. Performance targets (confirmed; refine after simulation and measurement)

With the filter bypassed:
- Frequency response 20 Hz to 20 kHz within +-0.5 dB
- THD+N below 0.05% at +4 dBu (relaxed from 0.01% for the SSI2162 VCA)
- Dynamic range above 100 dB
- Crosstalk below -80 dB

With the filter engaged:
- Dynamic range about 85 to 90 dB (limited by the SSI2144's 92 dB)
- Distortion above +12 dBu is accepted as part of the filter character

## 6. Tooling

- KiCad, driven through its MCP server **[confirmed]**
- Hierarchical schematics, custom symbol and footprint libraries, ngspice simulation, ERC/DRC checks, BOM export **[confirmed]**
