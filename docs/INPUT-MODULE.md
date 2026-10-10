# Input module interface

Status: **[confirmed]** by the user (decisions 62, 67, 68, 99 and 105; the pinout below by decision 105).

The channel card carries no input jacks. Its input sockets connect to a small **input module** that holds the connectors. The module options are interchangeable:

| Module | Connectors | Mono handling | Status |
|---|---|---|---|
| `input-module-6p3` | 2x 6.3 mm TRS (L/MONO, R) | R jack switch contacts normal L to R | Prototype |
| `input-module-3p5` | 2x 3.5 mm stereo switched jacks | Same as 6.3 mm | Backlog |
| `input-module-dsub` | One DB-25 carrying several channels (common 8-channel analog pinout), cables to each card's header | Jumper or switch per channel | Backlog |

The module is passive: connectors, normalling and nothing that needs power. The input receiver (a TL072 difference amplifier, G = ½, decision 143; the AD8273 before it), its protection, the AC coupling and the trim stay on the channel card, so every module gets the same hot-level handling (up to ±12 V peak, decision 25).

## Input header: 10 pins, 2.54 mm, single row, polarised

| Pin | Signal | Notes |
|---|---|---|
| 1 | AGND | |
| 2 | L+ | Hot, left (or mono) |
| 3 | L− | Cold, left. Tied to AGND at the jack sleeve for unbalanced sources |
| 4 | AGND | |
| 5 | R+ | Hot, right. Carries L+ when the module normals mono |
| 6 | R− | Cold, right. Carries L− when the module normals mono |
| 7 | AGND | |
| 8 | DO_L | Reserved for the pre-fader direct output, left (backlog). Unconnected on the prototype |
| 9 | DO_R | Reserved for the pre-fader direct output, right (backlog). Unconnected on the prototype |
| 10 | AGND | |

- Ground between the two channels.
- The cutoff CV jack is not on the input module: it belongs to the filter section on the channel card (decision 67).
- Pins 8 and 9 are reserved for the stereo pre-fader direct output in the backlog (decision 68), so adding it later needs no interface change. Direct output jacks would sit on the input module.
- Connector: a keyed, polarised single-row 1x10 header (Molex KK 254-style friction lock, footprint `Molex_KK-254_AE-6410-10A`). Exact part chosen during the schematic. Its size must not match the chain connectors (`CHAIN.md`).
- The jack sleeves and the D-SUB shell connect to AGND through the module's AGND pins, matching the grounding rules in `CHAIN.md`.

## Cable (decision 99)

Both the channel card and the module carry male KK 254 headers. They are linked by a 10-way cable wired 1:1 (pin 1 to pin 1, pin 10 to pin 10):

| Item | Part |
|---|---|
| Housing, both ends | Molex 22-01-3107 (KK 254 crimp housing, 2695 series, 10 positions, friction ramp), `SX-CONN-009` |
| Crimps | Molex 08-50-0114 (KK 254, 22-30 AWG, tin), `SX-CONN-010`, 20 per cable |
| Wire | 26 or 28 AWG stranded; twist L+/L− (pins 2-3) and R+/R− (pins 5-6) as pairs |
| Length | set in the mechanical layout (about 10 to 15 cm expected) |

Part numbers come from distributor listings; verify them against the Molex drawings before ordering. A module with a socket that plugs straight onto the card is not allowed: it would fix the module position and rule out cabled modules such as the D-SUB bundle.
