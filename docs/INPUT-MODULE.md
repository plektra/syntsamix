# Input module interface

Status: **[confirmed]** by the user (decision 62). Pinout **[proposed]** until the first schematic review.

The channel card carries no input jacks. Its input sockets connect to a small **input module** that holds the connectors. The module options are interchangeable:

| Module | Connectors | Mono handling | Status |
|---|---|---|---|
| `input-module-6p3` | 2x 6.3 mm TRS (L/MONO, R) and a 6.3 mm CV jack | R jack switch contacts normal L to R | Prototype |
| `input-module-3p5` | 2x 3.5 mm stereo switched jacks and a 3.5 mm CV jack | Same as 6.3 mm | Backlog |
| `input-module-dsub` | One DB-25 carrying several channels (common 8-channel analog pinout), cables to each card's header | Jumper or switch per channel | Backlog |

The module is passive: connectors, normalling and nothing that needs power. The input receiver (AD8273), its protection, the AC coupling and the trim stay on the channel card, so every module gets the same hot-level handling (up to ±12 V peak, decision 25).

## Input header: 8 pins, 2.54 mm, single row, polarised

| Pin | Signal | Notes |
|---|---|---|
| 1 | AGND | |
| 2 | L+ | Hot, left (or mono) |
| 3 | L− | Cold, left. Tied to AGND at the jack sleeve for unbalanced sources |
| 4 | AGND | |
| 5 | R+ | Hot, right. Carries L+ when the module normals mono |
| 6 | R− | Cold, right. Carries L− when the module normals mono |
| 7 | AGND | |
| 8 | CV | Cutoff CV, single-ended, referenced to AGND |

- Ground between the two channels and between audio and CV.
- Connector: a keyed, polarised single-row header (for example a KK 254-style friction-lock header). Exact part chosen during the schematic. Its size must not match the chain connectors (`CHAIN.md`).
- The jack sleeves and the D-SUB shell connect to AGND through the module's AGND pins, matching the grounding rules in `CHAIN.md`.
