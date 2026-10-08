# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Sidechain and ducking sheet reference netlist (build/sidechain.json), written independently of the drawing.

Decision 90; values simulated in simulation/sidechain/run.py.
Sources: INT = -(COMP_L_SUM + COMP_R_SUM)/2, BUS = -SC_SUM, EXT = DC-coupled inverting buffer
(100 kΩ) on a switched 6.3 mm jack whose ring switch contact (RN) detects a plug.
Selector (U506 DG413): SC BUS button picks BUS (pressed) or INT; a plugged EXT jack overrides.
LPF: unity-gain Sallen-Key 22 nF / 47 nF with 10 kΩ + a 100 kΩ dual reverse-log pot (about
45-510 Hz), bypass button (U507). A follower drives SC_DET (compressor detector, ducker, SC listen).
SC listen sums SC_DET into CUE_L/R through 22 kΩ and pulls PFL_ACT low (MMBT3904).
Ducker: window comparator against ±THRESHOLD (0.1-5 V peak), two DG413 NO sections charge
2.2 µF from the buffered DEPTH voltage (0 to -4 V) through 470 Ω; DECAY (500 kΩ log + 22 kΩ)
discharges it; a follower drives SC_ENV through 100 Ω with its feedback taken after the 100 Ω,
and a BAT54 clamps SC_ENV below about +0.3 V (decision 97).
DG413 sections: unit 1 (pins 1-3, NO), unit 2 (6-8, NO), unit 3 (9-11, NC), unit 4 (14-16, NC).
"""
import json,os
nets={}
def N(net,*pins):
    for p in pins:
        r,q=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":q})
# ---------------------------------------------------------------- sources (U501, U502A), EXT jack
N("COMP_L_SUM","R501.1"); N("COMP_R_SUM","R502.1"); N("NI","R501.2","R502.2","R503.1","U501.2"); N("AGND","U501.3"); N("INT","U501.1","R503.2")
N("SC_SUM","R504.1"); N("NB","R504.2","R505.1","U95012.6"); N("AGND","U95012.5"); N("BUSS","U95012.7","R505.2","U506.2")
N("AGND","J501.S","J501.R","J501.TN"); N("EXT_T","J501.T","R506.1"); N("EXT_SEL","J501.RN","R508.2","C501.1","U95062.8","U95064.16")
N("+5V","R508.1"); N("AGND","C501.2")
N("NE","R506.2","R507.1","U502.2"); N("AGND","U502.3"); N("EXTS","U502.1","R507.2","U95062.6")
# ---------------------------------------------------------------- selector (U506)
N("BUS_CTRL","U506.1","U95063.9"); N("SEL1","U506.3","U95063.11","U95064.15")
N("INT","U95063.10"); N("SEL2","U95064.14","U95062.7","R509.1","U507.2")
# ---------------------------------------------------------------- LPF (RV501, U502B)
N("LPF_P1","R509.2","RV501.3"); N("LPF_A","RV501.1","RV501.2","R510.1","C502.1")
N("LPF_P2","R510.2","RV501.6"); N("LPF_B","RV501.4","RV501.5","C503.1","U95022.5"); N("AGND","C503.2")
N("LPF_OUT","U95022.6","U95022.7","C502.2","U95073.10")
# ---------------------------------------------------------------- bypass, SC_DET buffer, SC listen (U507, U503A)
N("BYP_CTRL","U507.1","U95073.9"); N("FILT_IN","U507.3","U95073.11","U503.3")
N("SC_DET","U503.1","U503.2","U95072.6","U504.3","U95042.6","TP501.1")
N("LISTEN_CTRL","U95072.8","R513.1"); N("LST","U95072.7","R511.1","R512.1"); N("CUE_L","R511.2"); N("CUE_R","R512.2")
N("AGND","U95074.14","U95074.15","U95074.16")
N("Q_B","R513.2","Q501.1"); N("PGND","Q501.2"); N("PFL_ACT","Q501.3")
# ---------------------------------------------------------------- ducker: THRESHOLD, comparators (U504), inverter (U503B)
N("THR_LO","RV502.1","R515.2"); N("AGND","R515.1"); N("THR","RV502.2","U504.2","R516.1"); N("THR_HI","RV502.3","R514.1"); N("+15V","R514.2")
N("THR_INV","R516.2","R517.1","U95032.6"); N("AGND","U95032.5"); N("THRN","U95032.7","R517.2","U95042.5")
N("TRIG1","U504.1","U508.1"); N("TRIG2","U95042.7","U95082.8")
# DEPTH (U505A), charge switches (U508), hold, DECAY, SC_ENV buffer (U505B)
N("AGND","RV503.1"); N("DEPTH_W","RV503.2","U505.3"); N("DEP_TOP","RV503.3","R518.1"); N("-15V","R518.2")   # DEPTH 0 to -4 V (decision 97)
N("DEP","U505.1","U505.2","U508.2","U95082.6"); N("CHG","U508.3","U95082.7","R519.1")
N("AGND","U95083.9","U95083.10","U95083.11","U95084.14","U95084.15","U95084.16")
N("HOLD","R519.2","C504.1","R520.1","U95052.5"); N("AGND","C504.2")
N("DK","R520.2","RV504.3","RV504.2"); N("AGND","RV504.1")
N("ENV_O","U95052.7","R521.1"); N("SC_ENV","R521.2","TP502.1","U95052.6","D504.2"); N("AGND","D504.1")   # feedback after R521, Schottky clamp (decision 97)
# ---------------------------------------------------------------- buttons
for name,sw,led,rl,rp in (("BUS","SW501","D501","R522","R523"),("BYP","SW502","D502","R524","R525"),("LISTEN","SW503","D503","R526","R527")):
    N(f"{name}_CTRL",f"{sw}.3",f"{rp}.2"); N("+5V",f"{sw}.2"); N(f"{name}_LEDK",f"{sw}.6",f"{led}.1"); N("PGND",f"{sw}.5")
    N(f"{name}_LED",f"{led}.2",f"{rl}.2"); N("+15V",f"{rl}.1"); N("PGND",f"{rp}.1")   # pull-downs to PGND (decision 98)
# ---------------------------------------------------------------- supplies and decoupling
for ref in ("U95013","U95023","U95033","U95043","U95053"): N("+15V",f"{ref}.8"); N("-15V",f"{ref}.4")
for ref in ("U95065","U95075","U95085"): N("+15V",f"{ref}.13"); N("-15V",f"{ref}.4"); N("+5V",f"{ref}.12"); N("AGND",f"{ref}.5")
for k in range(8):
    N("+15V",f"C{505+2*k}.1"); N("AGND",f"C{505+2*k}.2"); N("-15V",f"C{506+2*k}.1"); N("AGND",f"C{506+2*k}.2")
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'sidechain.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
