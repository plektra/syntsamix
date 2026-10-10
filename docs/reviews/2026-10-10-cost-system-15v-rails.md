# Cost review: system (±15 V rails), 2026-10-10

Scope: the whole system, with the user's focus: "would it be technically possible and feasible to lower the rail voltage to ±15 V, with compromising the output level to +21 dBu, which is more or less the industry standard anyway in semi-pro audio devices (please verify this too)? Is there any significant cost factor, especially from the external PSU perspective?"

This is a read-only review by the cost controller (decision 136). Nothing below is decided; every lever is a proposal. Prices are before VAT and shipping. "Fee" means the JLCPCB extended-part fee: $3 per type, which is EUR 2.76.

## Short answer

1. **The audio already runs on ±15 V.** Every card regulates its own ±15.1 V with an LM317/LM337 (decisions 40, 78, 87). The ±20 V is only the raw distribution voltage on the power ribbons; it exists to keep the far card's regulators out of dropout. "Lowering the rails to ±15 V" can therefore mean two things:
   - **Scenario A:** ±15 V raw on the ribbons, with each card still regulating locally, to about ±12 V. The audio rails then drop by 3 V.
   - **Scenario B:** a regulated ±15 V made on the power board and used directly by the cards, with no per-card regulators. The audio rails stay at ±15 V, so no output level is lost.
2. **The output level is not what limits this.** Today the balanced outputs reach about +24 dBu, and the DRV135 can swing about +26 dBu differential at ±15 V (decision 125). Even with ±12 V local rails (scenario A), the DRV135 still swings about +24 dBu differential. The internal stages would then limit the output to about +23-24 dBu. Accepting +21 dBu does not save anything by itself.
3. **Both scenarios are technically feasible**, but neither saves much: a few euros to about EUR 20 per prototype and about EUR 10-35 per 16-channel console. The **brick does not change for the prototype**: the GSM120B24 stays, loaded to about 40 W instead of 53 W at the sizing figure. **At 16 channels**, ±15 V raw lets the GSM120B24 (EUR 44.12) replace the GSM160B24 (EUR 51.51). It also brings the single TPS54560 inverter's peak current at the full-size sizing load down from about 5.8-6.1 A to about 5.1-5.3 A, against a 6.3 A minimum current limit.
4. **The significant power-supply cost lies in the architecture, not in the voltage.** At prototype size, the power board costs about EUR 97 in parts, 16 fee types, set-up and its PCB minimum, on top of the brick. Two Class II desktop bricks in series (+ and − around PGND) would replace the brick and the whole power board. That saves about EUR 75-95 per prototype. With 19 V bricks the cards stay as drawn. With 15 V bricks you get the ±15 V raw case (scenario A), plus its redesign. This choice touches must-stay items (connectors, a power cut, hum) and changes confirmed decisions 60, 81 and 100, so it is a question for you, not a recommendation.
5. **+21 dBu is a common ceiling in semi-pro and live gear, but it is not "the standard".** Many semi-pro analog mixers state +21 to +22 dBu, but others state +24 to +28 dBu (details and sources in the "+21 dBu" section below).

## Figures

`python3 tools/costs.py estimate --channels N --md` on main at 7f9a54c (2026-10-10):

| Item | 2 ch | 4 ch | 16 ch |
|---|---|---|---|
| channel-card parts | 106 | 212 | 848 |
| input-module-6p3 parts | 3 | 7 | 26 |
| master parts (1 used, 2 assembled) | 175 | 175 | 175 |
| power parts (1 used, 2 assembled) | 28 | 28 | 28 |
| JLCPCB fees (70 extended/consigned types, 3 designs, placement) | 229 | 232 | 249 |
| PCBs | 75 | 75 | 116 |
| FR4 panels | 55 | 55 | 88 |
| Frame, hardware, ribbons, 24 V brick | 100 | 110 | 170 |
| Knobs and fader caps | 15 | 22 | 64 |
| Consigned parts handling | 30 | 30 | 30 |
| **Total (EUR)** | **817** | **946** | **1,795** |

**Totals under each scenario.** These are hand-adjusted from the line items above, not tool output, and are rounded:

| Scenario | 2 ch | 4 ch | 16 ch |
|---|---|---|---|
| Current design (±20 V raw, ±15.1 V local, 24 V brick, power board) | 817 | 946 | 1,795 |
| A: ±15 V raw from the power board, ±12 V local | about 814 | about 943 | about 1,785 |
| B: regulated ±15.1 V from the power board, no per-card regulators | about 803 | about 930 | about 1,760 |
| Two 19 V Class II bricks in series, no power board, cards as drawn | about 742 | about 871 | about 1,720 |
| Two 15 V Class II bricks in series, no power board, ±12 V local (A without the power board) | about 721 | about 850 | about 1,718 |

The 16-channel current figure still carries one power board as drawn, which cannot supply 16 cards (decision 100). The bricks rows already cover the full load.

**Parts per board** (`costs.py drivers`):
- Channel card: EUR 52.99.
- Master: EUR 111.15.
- Power: EUR 18.77.
- `costs.py unpriced`: nothing unpriced.

**Top cost drivers:**
- Channel card: SSI2144 ×2 8.77, DG413 ×4 5.35, SSI2162 3.85, trimmers ×3 4.74, Alpha pots about 8.4, bipolar 10 µF ×8 2.00.
- Master: SSI2162 ×4 15.40, DG413 ×9 12.03, AD8273 ×2 7.64, DRV135UA ×2 6.63, bipolar 10 µF ×16 4.00, TO-220 heatsinks ×2 3.00.
- Power board: KPJX-4S jack 3.68, 4u7 100 V ×10 2.48, power switch 2.00 (estimate), 330 µF ×4 1.87, TPS54560 ×2 1.65.

**Power-related items.** These are the only items a rail-voltage change can move:

| Item | EUR | Note |
|---|---|---|
| Channel card regulation: LM317D2 0.44, LM337D2 0.39, 10 µF ×5, 47 µF ×2, SS14 ×2, divider | about 0.95 per card | 2 fee types (LM317D2, LM337D2) |
| Master regulation: LM317 0.32, LM337 0.55, two TO-220 heatsinks 3.00 (L7805 stays) | about 3.9 | the heatsinks are also an open mechanical problem: 19.7 mm tall, live tabs (master STATUS) |
| Power board: parts EUR 18.77 per board (28 for two assembled), 16 fee types used only here (EUR 44), set-up 8.93, PCB minimum 15 | about 97 per prototype | |
| Brick: `overheads.csv` brick_eur 50 | GSM120B24-R7B is EUR 44.12, GSM160B24-R7B 51.51 (Mouser, 2026-10-10) | |

**Change since the last cost report** (`2026-10-10-cost-system.md` and the ROADMAP update of the same day, 885 / 1,035 / 2,009 EUR after its corrections): now 817 / 946 / 1,795 EUR, which is −68, −89 and −214 EUR.
- The difference is commit 7f9a54c, the channel-card decisions 139-143: DG412 → DG413, every value on E24 with fee-free parts, the TFPT tempco moved to the backlog, U206 removed (MUTE and DUCK switched by the buttons), and a TL072 difference receiver in place of the AD8273.
- Channel-card parts fell from about EUR 65 to EUR 53 per card. Fee types fell from 80 to 70 (about EUR 193 in fees now).

**Realized costs** (`costs.py ledger`): EUR 53.80 in total. No change.

## Is ±15 V technically feasible? What it touches

### Scenario A: ±15 V raw on the ribbons, local regulation kept at about ±12 V

**Dropout:** a 15 V raw rail, less about 0.3-0.5 V of cable and fuse drop and less the ripple, leaves about 14.2 V at the far card. The LM317/LM337 need about 1.7-2.5 V, so ±12 V is the practical maximum; ±11.5 V is safer at worst case. You cannot keep ±15.1 V local rails on a ±15 V raw supply.

**Levels at ±12 V local:**
- Internal maximum: about +18 dBu instead of about +20 dBu. The design takes the swing as the rail less about 2.8 V: 9.2 V peak is about +18.5 dBu.
- Soft clip (decisions 64, 92): the onset is set by the 6V2 zeners, so it stays at about +14 dBu. The margin from soft clip to hard clip shrinks from about 6 dB to about 4 dB. This touches a "must stay" item (the soft-clip behaviour). It would be heard on the breadboard.
- Balanced outputs: the DRV135 swing is (V+) − 3 V / (V−) + 2 V (TI SBOS094B, quoted in decision 125). At ±12 V that is about 18 V peak differential, about +24 dBu. With the internal maximum at about +18 dBu and the driver's +6 dB, the output reaches about +23-24 dBu. **+21 dBu is met with margin.** The master meter clip point (+17 dBu internal, decision 93) would move down about 2 dB.
- Hot Eurorack inputs (±12 V peak, decision 25, must stay): they still pass. The TL072 difference receiver (decision 143) at G = ½ gives ±6 V out. Its non-inverting input sees a third of the input, about ±4 V, inside the TL072's common-mode range at ±12 V. The cutoff CV input and the master's EXT sidechain input (both "up to ±12 V" through 100 kΩ) sit at the rail limit instead of 3 V inside it. That is fine with the existing series resistors, but check the clamps.

**Part limits at ±12 V** (all from `parts.csv` or `SPEC.md`):
- SSI2144: ±4 to ±16 V. Its datasheet figures are measured at ±12 V.
- SSI2162: up to ±18 V.
- TL072 and NE5532: fine.
- OPA2171: 2.7-36 V.
- DG413/DG411: fine, with slightly higher on-resistance.
- LM13700, LM339 and AD8273 (±2.5 to ±18 V): fine.
- TPA6120A2: ±5 to ±15 V.
- DRV135: fine.
- G6K-2F-Y DC12: the 12 V coil would run directly from +12 V. Operate is at 80 % maximum, so 9.6 V, which is fine.
- **TL062 meter amplifiers:** the TL062's ±10 V minimum swing is specified at ±15 V only. The master meter inverters need ±7.75 V at clip (decision 126), or about ±6.2 V after rescaling. That is probably fine but outside a datasheet minimum: UNVERIFIED.

**Circuits that take their reference from the rails, and would all need new values and new simulations:**
- the fader law and the mute voltage (fader to −15 V, decisions 72, 102, 142)
- the CUTOFF pot across ±15.1 V and the RESONANCE chain (decision 129)
- the compressor RELEASE network (decision 131) and the ducker DEPTH (R518 to −15 V, decision 104)
- the meter ladders from +15 V (decisions 76, 93)
- the relay drop-out comparators: they trip at 17.9 V raw today (decisions 92, 128), and would need new thresholds near 13.5 V
- the relay coil resistor

Roughly 20-30 value changes over the channel card and master, plus reruns of `simulation/level/`, the compressor and the sidechain simulations.

**Power board:**
- Only the feedback dividers change.
- The buck duty drops from 83 % to 63 %, which removes the open minimum-off-time question in the power STATUS.
- The inverter IC sees VIN + |Vo| = 39.7 V instead of 44.7 V.
- The 100 V input ceramics still see up to 53.9 V during a TVS clamp (38.9 + 15), so they stay 100 V parts.

**Verdict on A:** feasible, but it costs about 2 dB of internal headroom and a large redesign, and saves almost nothing (Levers, below).

### Scenario B: regulated ±15.1 V from the power board, no per-card regulators

**Levels:** unchanged. The internal maximum stays at about +20 dBu, the outputs at about +24 dBu, and Eurorack headroom is unchanged. No IC limit changes.

**Changes:**
- **Invariant 3** ("every card regulates its own rails; no regulated rail crosses a ribbon") and decisions 40, 78, 87 and 110 change. This is a `/system` matter.
- The relay drop-out loses its early warning. Today the comparators see the raw rail sag before ±15 V collapses. With no raw rail, the relays need a power-fail signal from the power board (a contract change on the power ribbon) or a threshold just under 15 V. Must stay: no pops at power-down.

**Risks:** all on the "must stay" side (noise and hum for a loud PA):
- The 400 kHz converter residue (about 63 dB down at the cards today, with the LC filter's peaking of about 4.4 dB near 4 kHz) reaches the audio rails with no LM317/LM337 rejection.
- Several controls take their voltage from the rails: the fader law, the mute voltage, the CUTOFF pot and the meter ladders. So rail noise and load-dependent sag modulate the VCA gain and the filter cutoff directly, not only through the op amps' PSRR. At −33 mV/dB, 10 mV of rail disturbance is about 0.3 dB of gain modulation.
- The headphone amplifier (TPA6120A2, hundreds of mA in signal-dependent peaks) sits on the same rails as every channel. Its current would then imprint the headphone signal on every card's gain control. The master would probably have to keep a local regulator, which means a second raw voltage.

**Verdict on B:** feasible on paper. It saves about EUR 1 per card, plus EUR 4 on the master and the master's heatsink-height problem, and about 20 W of heat at full size. But it removes the stage that keeps rail noise out of rail-referenced control voltages. Not recommended without a bench test of rail noise against gain modulation.

### Scenario C: an external ±15 V supply instead of the brick and the power board

- **Dedicated symmetric ±15 V supplies of this power are rare and expensive.**
  - The Traco TXL 035-1515D (±15 V, 35 W, metal chassis case) costs EUR 54.70 and is below the prototype's 1.28 A sizing figure.
  - The Mean Well RT-65C and RT-125C triple-output units give only 0.5 A or 1 A on −15 V (EUR 19.09 and 29.92).
  - None found is a Class II desktop unit with a floating output (invariant 8).
- **The practical way to get "±15 V external" is two single-output Class II bricks in series**, + and − around PGND. Two Mean Well GSM60B15-P1J (15 V, 4 A, 60 W, 2-pole) cost about EUR 41; two GSM90B15-P1M (6 A, for the full console) about EUR 60.
  - Their output is already regulated (about 100 mVp-p ripple, datasheet via distributor), so the cards could not regulate to ±15.1 V again. It becomes scenario A (±12 V local) without the power board.
  - **The same idea with 19 V bricks keeps every card as drawn:** two GSM90B19-P1M (19 V, 4.74 A, EUR 30.10 each) give ±19 V raw, enough for the LM317/LM337 to make ±15.1 V and enough for the full 16-channel sizing figure (3.37 A per rail). See prototype lever 1.

## Is +21 dBu the semi-pro norm?

**Partly.** +21 to +22 dBu is a common maximum output, especially on digital live consoles and some compact analog mixers. Many semi-pro analog mixers state +24 to +28 dBu at their XLR mains, so "industry standard" is too strong. "A common, acceptable ceiling for live use" is fair.

| Product | Stated maximum output | Source |
|---|---|---|
| Behringer X32 (XLR outs) | +21 dBu (TRS aux +16 dBu) | Adorama listing; Sound On Sound review measured +21 dBu |
| Allen & Heath ZED-12FX (mains, aux) | +21 dBu (0 dBu nominal) | retailer copies of A&H spec table (idjnow, adorama) |
| Soundcraft Signature 12 (mix out) | +21.5 dBu | retailer copies (Markertek, IDJ Now) |
| Allen & Heath Qu-16 (mix, LR) | +22 dBu (0 dBFS = +18 dBu) | distributor spec listings |
| Yamaha MG10XU (stereo out) | +24 dBu at 600 Ω | Yamaha Japanese datasheet (MG10XUF) |
| Mackie ProFX12v3 (XLR main) | +28 dBu (other outputs +22 dBu) | several retailer spec sheets |

**Context:**
- EBU R68 aligns 0 dBFS at +18 dBu, and SMPTE RP155 is commonly calibrated at +24 dBu for 0 dBFS (Wikipedia "DBFS" and "Alignment level"; Lawo manuals). A +21 dBu output therefore fills EBU-aligned recorders and interfaces with 3 dB to spare. It clips a SMPTE-aligned input about 3 dB before that input's full scale.
- At the mixer's +4 dBu nominal, +21 dBu still gives 17 dB of output headroom.
- Under decision 135 that is a legitimate relaxation (studio nicety, not stage-critical). But as shown above, it buys nothing in this design.

## Levers

Tags:
- **[relax]**: accuracy, calibration or a studio nicety is traded (allowed by decision 135).
- **[neutral]**: no trade-off.
- **[check]**: a "must stay" item is near and needs a test or a decision first.

### Prototype (2-4 channels: fixed costs)

1. **Two series Class II 19 V bricks instead of the 24 V brick and the power board** (scenario C with 19 V). Saves about **EUR 75 per prototype** (about EUR 95 with two GSM60B18 if their price matches the GSM60B15's; UNVERIFIED).
   - **Removes:**
     - the power board: parts EUR 28 for two assembled
     - the 16 fee types only it uses: EUR 44 (SX-C-018, -019, -021, -022, SX-D-009, -012, -013, SX-F-002, SX-L-001, SX-Q-002, SX-R-029, -083 to -086, SX-IC-018)
     - set-up 8.93 and the PCB minimum of 15
     - its open items: the start-up ramp, the minimum off-time, fuse coordination, and the full-size 4 A inverter design.
   - **Adds:**
     - two GSM90B19-P1M (EUR 60.20 against the EUR 50 brick allowance)
     - about EUR 8-12 of passive parts at the injection point: two DC jacks with strain relief, the six PTC fuses, an LC filter per rail against the bricks' ripple, and the three ribbon headers. They could go on the master card as hand-soldered THT parts, or on a small passive board.
   - **Card changes:** none, except the master's drop-out comparator thresholds. 19 V × 0.98 less the drops is about 18.1 V, too close to today's 17.9 V trip, so two resistor values change. The LM317 keeps about 1 V of margin at the far card.
   - **Trade-offs [check]:**
     - Reliability: two mains cords and two barrel plugs. The R7B locking DIN versions exist for some GSM models (GSM120B20-R7B EUR 44.12) but cost about twice as much; a locking or strain-relieved connector is a must-stay item.
     - Power cut: the two bricks start up to some hundreds of ms apart, so the rails rise asymmetrically. The SS14 rail clamps and the relay delay (decision 128 watches both rails) are designed for this, but check on the bench.
     - Hum: two Y-capacitor leakage paths into PGND. The GSM medical series has low leakage, but check with connected gear.
     - Noise: brick ripple of about 120 mVp-p at tens of kHz goes into the LM317s. Add an LC per rail.
     - Series operation of two GSM outputs and their capacitive-load limit against the 0.37-1.2 mF of rail capacitance: UNVERIFIED in Mean Well's data.
   - **Affects:** decisions 60, 81, 100 and 101 (invariant 8 holds: both bricks are Class II with floating outputs), 128, `CHAIN.md` (injection point) and `MECHANICAL.md` (rear panel). Effort: a `/system` decision, then master power-sheet edits. The power board work stops.

2. **The same with two 15 V bricks** (true ±15 V raw, scenario A plus C). About **EUR 95 per prototype** (two GSM60B15 at about EUR 41).
   - Trade-off [check]: everything in lever 1, plus scenario A's 2 dB less internal headroom and the 4 dB soft-clip-to-clip margin, plus the 20-30 value changes and simulations.
   - The extra saving over lever 1 is about EUR 20 per prototype, which does not pay for the redesign. Not recommended over lever 1.

3. **Scenario B: regulated ±15.1 V from the power board, no per-card regulators.** About **EUR 16-20 per prototype** at 4 channels:
   - 4 × 0.95 per card
   - the 2 fee types LM317D2 and LM337D2 (5.52)
   - the master's LM317, LM337 and heatsinks (3.9)
   - the master's TO-220 height and live-tab problem (`MECHANICAL.md`, open)
   - Trade-off [check]: must-stay noise and hum (see scenario B above), and the relay early warning is lost. It changes invariant 3 and decisions 40, 78, 87, 95, 110 and 128. Effort: `/system`, the power sheets on every board, and a bench test of rail noise against VCA and cutoff modulation.

4. **Scenario A on the existing power board: ±15 V raw, ±12 V local.** About **EUR 3-6 per prototype**:
   - The channel D²PAK regulators would dissipate about 0.7 W worst case instead of 1.2 W. The UTC LM317AG-TN3-R DPAK (LCSC C75510, preferred, from the last review) then fits: one fee type and about EUR 0.2 per card.
   - The brick stays the GSM120B24.
   - Trade-off [check]: −2 dB internal headroom and a smaller soft-clip margin, plus the full redesign effort. **Not proposed:** the cost does not justify it.

The general levers of the last review still apply, the largest being "start with 2 channels" (946 → 817 EUR). They are not repeated here.

### Console and product (16 channels, volume)

1. **Two series Class II 19 V bricks** (prototype lever 1). Compared with the 16-channel estimate, which still carries one power board as drawn and a EUR 50 brick, it saves about **EUR 75 per console**. The estimate understates the real saving:
   - At full size the present design needs either a second power board (power lever 1, about EUR 40) or a new external-MOSFET inverter. Two GSM90B19 carry the full sizing load (3.37 A at 4.74 A rating per rail), so that design work and those parts disappear.
   - At product volume the power board's fees and set-up spread out. Its parts and PCB (about EUR 20-25) then trade against the second brick (about EUR 10-15 more than one GSM160B24), which is roughly EUR 10 per unit in favour of two bricks. The two-cord set-up is the real product question.

2. **Scenario B** (prototype lever 3). About **EUR 35 per console**:
   - 16 × 0.95 = 15.2 in channel regulation
   - 5.5 in fees
   - 3.9 on the master
   - the brick drops from GSM160B24 to GSM120B24 (7.4), because the brick then sees about 105 W instead of 140 W at the sizing figure
   - Also about 20 W less heat inside the unit at typical load (79 W → 59 W), which helps the open ventilation item.
   - Same trade-off as prototype lever 3 [check].

3. **±15 V raw on the existing power board (scenario A).** About **EUR 10 per console**: the brick goes from GSM160B24 to GSM120B24 (7.4) and one DPAK fee type is removed.
   - Its real value is technical. The inverter's peak current at the full-size sizing load falls from about 5.8-6.1 A to about 5.1-5.3 A (TPS54560 minimum limit 6.3 A; `design.py` equations, 275-400 kHz, 22 µH), so one TPS54560 inverter might carry 16 cards. That avoids power lever 1 (a second board, about EUR 40) or the external-MOSFET design.
   - UNVERIFIED: the inductor rating, the IC thermals and the start-up at full load.
   - Trade-off [check]: the headroom and redesign of scenario A. Not proposed for cost alone.

4. **Internal Class I supply** (question 2 below). Two Mean Well LRS-100-15 (EUR 13.87 each, adjustable 13.5-18 V per resellers) in series, set to about ±18 V, feeding the cards as drawn, would replace the brick and the power board for about EUR 28 plus an IEC inlet with fuse and switch. That is about **EUR 60-80 less than the brick plus a full-size power board** per unit. The cheapest supply found, but it puts mains inside the mixer.

## Rule findings

E24 (decision 134):
- Channel card: every value is now E24 with a fee-free part, except R217 30k1 (decision 140, reason recorded).
- Master: 24 off-E24 types (SX-R-014, -023 to -028, -038, -058, -068 to -080, -082 39R2), plus 560k (E24, no fee-free part). This is unchanged since the last review.
- Power: 732k, 42k2, 15k8 and 243k off E24, plus 240k with no fee-free part. A ±15 V output (scenarios A or B) would change the feedback divider anyway, so pick E24 fee-free values then.
- Input module: none.

JLCPCB class (decision 137): 70 extended or consigned types (was 80): 16 only on the power board, the rest on the channel card and master.
- On the power side: the 4u7 100 V 1210 (SX-C-018) has no fee-free 1210 part. A 4.7 µF 50 V X7R 1206 is basic (FH 1206B475K500NT, LCSC C29823, $0.032; jlcsearch 2026-10-10). It does not suit the inverter input, which sees up to 53.9 V at a TVS clamp even at ±15 V, or 58.9 V at ±20 V. The type therefore stays, whatever the rail voltage.
- No new fee-free LM337 was found. The LM317 DPAK (C75510, preferred) only becomes thermally acceptable under scenario A or B.

## Questions for the user

1. **Two bricks instead of one brick and the power board** (prototype lever 1, console lever 1). This saves about EUR 75-95 per prototype, and avoids the full-size inverter design. But it reverses confirmed decisions 60, 81 and 100, and it touches must-stay items: reliability with two cords and two connectors, recovery after a power cut, and hum. Would you consider it, and if so with 19 V bricks (cards unchanged) or 15 V bricks (true ±15 V, scenario A redesign)?
2. **Internal mains supply for a product** (console lever 4, the backlog item of decision 101). It is the cheapest supply found, but it needs a Class I mains design: IEC inlet, fuse, earth bonding, and the ground-lift between signal ground and chassis. Safety and certification are must-stay items.
3. **Invariant 3 (local regulation)**: would you reopen it for scenario B (about EUR 16-35)? It is the only way to lower the distribution voltage to ±15 V without losing headroom, and it trades a regulator stage that protects the noise floor.

## Prices to update (for `docs/costs/prices.csv` and `overheads.csv`; checked 2026-10-10)

| ProjectPN | Price | Currency | Break | Source | Note |
|---|---|---|---|---|---|
| SX-MECH-003 GSM120B24-R7B | 44.12 | EUR | 1+ | Mouser 709-GSM120B24-R7B (API) | 40.16 at 10+; 16 in stock. `overheads.csv` brick_eur 50 can become 44.12 for 2-4 channels |
| (16 ch brick) GSM160B24-R7B | 51.51 | EUR | 1+ | Mouser 709-GSM160B24-R7B (API) | No stock at Mouser |
| (candidate) GSM90B19-P1M | 30.10 | EUR | 1+ | Mouser 709-GSM90B19-P1M (API) | 19 V 4.74 A, Class II medical, 151 in stock; P1M barrel plug |
| (candidate) GSM60B15-P1J | 20.62 | EUR | 1+ | Mouser 709-GSM60B15-P1J (API) | 15 V 4 A, 2-pole; no stock (GSM60A15-P1J, 3-pole, EUR 20.55, 122 in stock) |
| (candidate) GSM120B20-R7B | 44.12 | EUR | 1+ | Mouser 709-GSM120B20-R7B (API) | 20 V 6 A, R7B locking DIN |
| (candidate) GSM120B15-R7B | 44.12 | EUR | 1+ | Mouser 709-GSM120B15-R7B (API) | 15 V 7 A (105 W), R7B |
| (candidate) GSM90B15-P1M | 30.10 | EUR | 1+ | Mouser 709-GSM90B15-P1M (API) | 15 V 6 A; no stock |
| (candidate) LRS-100-15 | 13.87 | EUR | 1+ | Mouser 709-LRS100-15 (API) | Class I enclosed, 15 V 7 A, adjustable 13.5-18 V (reseller copies of the datasheet) |
| (reference) RT-65C / RT-125C | 19.09 / 29.92 | EUR | 1+ | Mouser 709-RT65C, 709-RT-125C (API) | −15 V only 0.5 / 1 A: unsuitable |
| (reference) TXL 035-1515D | 54.70 | EUR | 1+ | Mouser 495-TXL-035-1515D (API) | ±15 V 35 W: too small for the prototype |
| (candidate) 4.7 µF 50 V X7R 1206 | 0.0317 | USD | 1+ | jlcsearch, LCSC C29823 (FH 1206B475K500NT), basic | Only where ≤ 25 V DC is present; not for the inverter input |

## Not checked

- No Mean Well datasheet was read directly (no PDF text tools in this session), only Mouser listings and distributor or reseller copies. Not confirmed in Mean Well's own documents:
  - GSM60B model list and ripple (100 mVp-p at 15 V, 120 mVp-p at 18 V)
  - Class II for each model
  - series-connection permission
  - capacitive-load limit
  - set-up time
  - R7B availability for the 60 and 90 W models
  - the LRS-100-15 adjustment range
- GSM60B18 price: not found at Mouser.
- The TI DRV135 swing at ±12 V is extrapolated from the (V+) − 3 V / (V−) + 2 V figure recorded in decision 125. The TL062 swing at ±12 V is not specified in SLOS078N.
- The full-size inverter peak currents come from the `design.py` equations (copied to scratch). Not checked: inductor saturation (Bourns SRP1265A), IC thermals, start-up with 1.2 mF per rail.
- Gain modulation from rail noise in scenario B is estimated, not simulated.
- The `pcbparts` MCP tools were not available. Fee-free searches used the jlcsearch API (at most 100 results per query).
- Maximum-output figures for the mixers are mostly from retailer copies of maker spec sheets. The EBU R68 and SMPTE RP155 figures are from secondary sources (Wikipedia, Lawo), not the standards themselves.

Sources:
- Mouser Search API through `tools/mouser.py` (bricks, RT, TXL, LRS), 2026-10-10.
- [jlcsearch.tscircuit.com](https://jlcsearch.tscircuit.com) capacitor list (C29823), 2026-10-10.
- [Mean Well GSM60B spec (Arrow copy)](https://static6.arrow.com/aropdfconversion/6586dd3b56e2ca230d4e4fbfe5ee3e0a0fc4f5f0/gsm60bspec.pdf), [GSM60B15 test report (Simpex)](https://simpex.ch/wp-content/uploads/2021/07/GSM60B15-rpt.pdf), [LRS-100-15 (openelab)](https://openelab.io/products/meanwell-lrs100-15-switching-power).
- [Behringer X32 (Adorama)](https://www.adorama.com/behringer-x32-32-channel-digital-mixing-console/p/bex32f), [Sound On Sound X32 review](https://www.soundonsound.com/node/4904253).
- [Allen & Heath ZED-12FX (idjnow)](https://www.idjnow.com/allen-and-heath-ah-zed12fx-mixer.html), [Allen & Heath Qu-16 (ProAcoustics)](https://www.proacousticsusa.com/allen-heath-qu-16-rackmountable-digital-mixer.html).
- [Soundcraft Signature 12 (Markertek)](https://www.markertek.com/product/scft-signature12/soundcraft-signature-12-12-input-compact-analogue-mixer).
- [Yamaha MG10XUF datasheet (JP)](https://jp.yamaha.com/files/download/other_assets/5/1201305/MG10XUF.pdf).
- [Mackie ProFX12v3 (Markertek)](https://markertek.com/product/mck-profx12v3/mackie-profx12v3-12-channel-professional-effects-mixer-with-usb).
- [DBFS (Wikipedia)](https://en.wikipedia.org/wiki/DBFS), [Alignment level (Wikipedia)](https://en.wikipedia.org/wiki/Alignment_level), [Lawo system reference levels](https://docs.lawo.com/audio-production-mc-mixing-consoles/power-core-rp-v2-user-manual/power-core-rp-v2-data-and-specifications/power-core-rp-v2-system-reference-levels).

## Outcome (added 2026-10-10, /system power brick)

- The user found the ±15 V savings marginal; the rails stay as they are (±20 V raw, ±15.1 V regulated on each card).
- Two bricks (in series or otherwise) were rejected by the user: two mains cords look and feel unprofessional. Supply levers keep one power input.
- A follow-up survey of single 24 V bricks led to decision 145: the GSM220B24-R7B (221 W, EUR 72.90 at TME) replaces the GSM160B24-R7B for 16 cards; the prototype keeps the GSM120B24-R7B. `tools/costs.py` now takes the brick price from `docs/costs/prices.csv` (SX-MECH-003 up to 8 channels, SX-MECH-005 above).
- The user set the realistic builds to 4, 8 and 16 channels; `tools/costs.py estimate` now shows them side by side: €941 / €1,221 / €1,818.
