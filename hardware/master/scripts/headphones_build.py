# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Headphones sheet reference netlist (build/headphones.json), written independently of the drawing.

Decisions 56, 84 and 94. A DG413 picks the source: MAIN_L/R_OUT while PFL_ACT is high,
the cue bus sums while any PFL (or SC listen) pulls PFL_ACT low. A dual 10 kΩ log volume
pot feeds the TPA6120A2 (TI SLOS431B) as non-inverting gain-2 stages: 51 Ω series input,
1 kΩ / 1 kΩ feedback, 39.2 Ω output resistors (2512 for the power). The third G6K relay
(coil on RLY_N from the Master out sheet) connects the amplifier to the 6.3 mm stereo jack;
released, both conductors go to AGND through 1 kΩ. The PFL-active LED sinks into PFL_ACT.
References 751 onwards (the 7xx block is shared with the Master out sheet, which ends at 731).
"""
import json,os
nets={}
def N(net,*pins):
    for p in pins:
        r,q=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":q})
# ---------------------------------------------------------------- source switch (U751 DG413): NO = main (PFL_ACT high), NC = cue
N("MAIN_L_OUT","U751.2"); N("HP_L_SEL","U751.3","U97513.11","RV751.3"); N("CUE_L_SUM","U97513.10")
N("MAIN_R_OUT","U97512.6"); N("HP_R_SEL","U97512.7","U97514.14","RV751.6"); N("CUE_R_SUM","U97514.15")
N("PFL_ACT","U751.1","U97512.8","U97513.9","U97514.16","D752.1")
# ---------------------------------------------------------------- volume and TPA6120A2 (U752)
N("AGND","RV751.1","RV751.4"); N("HP_L_W","RV751.2","R751.1"); N("HP_R_W","RV751.5","R755.1")
N("L_INP","R751.2","U752.4"); N("L_INN","U752.5","R752.1","R753.1"); N("AGND","R752.2"); N("L_AMP","U752.2","R753.2","R754.1")
N("R_INP","R755.2","U752.17"); N("R_INN","U752.16","R756.1","R757.1"); N("AGND","R756.2"); N("R_AMP","U752.19","R757.2","R758.1")
N("+15V","U752.3","U752.18","C751.1","C752.1","C755.1"); N("-15V","U752.1","U752.20","C753.1","C754.1","C756.2"); N("AGND","U752.21")
N("AGND","C751.2","C752.2","C753.2","C754.2","C755.2","C756.1")
# ---------------------------------------------------------------- relay K751 (pole 2 left/tip, pole 1 right/ring), jack J751
N("HP_LO","R754.2","K751.5"); N("HP_RO","R758.2","K751.4")
N("HP_L","K751.6","J751.T"); N("HP_R","K751.3","J751.R"); N("AGND","J751.S")
N("HP_GL","K751.7","R759.1"); N("HP_GR","K751.2","R760.1"); N("AGND","R759.2","R760.2")
N("K3P","K751.1","R761.1","D751.1"); N("+15V","R761.2"); N("RLY_N","K751.8","D751.2")
# ---------------------------------------------------------------- PFL-active LED
N("PFL_LEDA","D752.2","R762.2"); N("+5V","R762.1")
# ---------------------------------------------------------------- supplies
N("+15V","U97515.13","C757.1"); N("-15V","U97515.4","C758.1"); N("+5V","U97515.12"); N("AGND","U97515.5","C757.2","C758.2")
N("HP_L_SEL","TP751.1"); N("HP_R_SEL","TP752.1")
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'headphones.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
