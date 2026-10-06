# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Compressor sheet reference netlist (build/compressor.json), written independently of the drawing.

Decisions 57, 82 and 89; detector values simulated in simulation/compressor/run.py.
Audio: COMP_L/R_SUM (inverted by the summing amps) into a stereo-linked SSI2162 with I-V
stages (wet, non-inverted), unity inverters for the dry path, a dual linear MIX pot
(CCW dry, CW wet) with followers, and 22 kΩ into the MAIN bus nodes.
Side chain on SC_DET: precision full-wave rectifier into a log converter on the AS3046D
matched pair (Q1 signal, Q2 diode-connected reference), gain -11 with the ERA-V33,
peak hold (470 Ω / 1 µF attack, Q3/Q4 current-mirror release set by RELEASE),
threshold and 4:1 ratio, makeup 0.735 x Amount (DNP R439 halves it), VC summer.
ON/OFF ramps the Amount voltage through one DG413 (pressed = on) and lifts the threshold
when off. Five gain-reduction LEDs on two LM339s.
DG413 sections: unit 1 (pins 1-3, NO), unit 2 (6-8, NO), unit 3 (9-11, NC), unit 4 (14-16, NC).
"""
import json,os
nets={}
def N(net,*pins):
    for p in pins:
        r,q=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":q})
# ---------------------------------------------------------------- audio: VCA (U401), I-V (U403), dry inverters (U404)
N("COMP_L_SUM","C401.1","R408.1"); N("COMP_R_SUM","C402.1","R410.1")
N("L_VIN","C401.2","R401.1"); N("R_VIN","C402.2","R402.1")
N("L_IIN","R401.2","R403.1","U401.2"); N("L_RC","R403.2","C403.1"); N("AGND","C403.2")
N("R_IIN","R402.2","R404.2","U401.9"); N("R_RC","R404.1","C404.2"); N("AGND","C404.1")   # R network drawn upwards
N("VC","U401.3","U401.8"); N("MODE","U401.1","R405.2"); N("+15V","R405.1","U401.10"); N("-15V","U401.6"); N("AGND","U401.5")
N("L_IOUT","U401.4","U403.2","R406.1","C405.1"); N("AGND","U403.3"); N("WET_L","U403.1","R406.2","C405.2","RV401.3")
N("R_IOUT","U401.7","U94032.6","R407.1","C406.1"); N("AGND","U94032.5"); N("WET_R","U94032.7","R407.2","C406.2","RV401.6")
N("L_DINV","R408.2","R409.1","U404.2"); N("AGND","U404.3"); N("DRY_L","U404.1","R409.2","RV401.1")
N("R_DINV","R410.2","R411.1","U94042.6"); N("AGND","U94042.5"); N("DRY_R","U94042.7","R411.2","RV401.4")
# mix pot and followers (U405), bus resistors
N("L_MIXW","RV401.2","U405.3"); N("MIX_L","U405.1","U405.2","R412.1"); N("MAIN_L","R412.2")
N("R_MIXW","RV401.5","U94052.5"); N("MIX_R","U94052.7","U94052.6","R413.1"); N("MAIN_R","R413.2")
# ---------------------------------------------------------------- side chain: rectifier (U406A), log converter (U406B, U402)
N("SC_DET","R414.1","R416.1")
N("FW_N","R414.2","R415.1","U406.2","D402.2"); N("AGND","U406.3"); N("FW_O","U406.1","D401.2","D402.1")
N("FW_HW","D401.1","R415.2","R417.1")
N("LN","R416.2","R417.2","R418.2","U402.1","U94062.6","C407.1"); N("+15V","R418.1"); N("AGND","U402.2","U94062.5")
N("LOG_O","U94062.7","R419.2","C407.2"); N("EMIT","R419.1","U402.3","D403.2"); N("AGND","D403.1")
N("REF","R420.2","U402.4","U402.5","U407.3"); N("+15V","R420.1")
# reference buffer (U407A), gain -11 with the ERA-V33 (U407B)
N("VL","U407.1","U407.2","R421.1"); N("GAIN_N","R421.2","R422.1","U94072.6"); N("AGND","U94072.5"); N("VA","U94072.7","R422.2","U408.3")
# peak hold (U408), release mirror (U402 units 2-4), RELEASE pot
N("PK_K","U408.2","D404.1","R423.1"); N("PK_O","U408.1","D404.2"); N("HOLD","R423.2","C408.1","U94082.5","U94022.8"); N("AGND","C408.2")
N("VD","U94082.6","U94082.7","R429.1")
N("MIR","U94022.6","U94023.9","U94023.11","R424.2"); N("-15V","U94022.7","U94023.10","U94024.12","U94024.13")
N("REL_W","RV402.2","R424.1"); N("AGND","RV402.1"); N("REL_B","RV402.3","R425.1"); N("-15V","R425.2")
# ---------------------------------------------------------------- Amount pot, on/off ramp (U413), buffer (U410B)
N("AMT_TOP","R426.1","RV403.3"); N("+15V","R426.2"); N("AGND","RV403.1"); N("AMT_W","RV403.2","U413.2")
N("AMT_S","U413.3","R427.1"); N("AMT_R","R427.2","C409.1","R428.1","U94102.5"); N("AGND","C409.2")
N("AMT_D","R428.2","U94133.10"); N("AGND","U94133.11")
N("VAMT","U94102.6","U94102.7","R430.1","R437.1")
# gain computer (U409A): threshold, 4:1 ratio, off-state threshold lift (U413 units 4 and 2)
N("GC","R429.2","R430.2","R431.2","R433.2","R435.1","U409.2","D406.1"); N("-15V","R431.1"); N("AGND","U409.3")
N("GC_O","U409.1","D405.1","D406.2"); N("GRN","D405.2","R435.2","R436.1","R441.1")
N("-15V","U94134.15"); N("KILL_S","U94134.14","R432.1"); N("KILL","R432.2","C410.1","R433.1","R434.2"); N("AGND","C410.2")
N("KILL_R","R434.1","U94132.7"); N("AGND","U94132.6")
N("ON_CTRL","U413.1","U94132.8","U94133.9","U94134.16")
# VC summer (U409B): VC = gain reduction - makeup
N("VSUM","R436.2","R438.2","R440.1","C411.1","U94092.6"); N("AGND","U94092.5"); N("VC","U94092.7","R440.2","C411.2")
N("MK","R437.2","R438.1","R439.1"); N("AGND","R439.2")
# ---------------------------------------------------------------- gain-reduction LEDs: inverter (U410A), ladder, LM339 (U411, U412)
N("GR_INV","R441.2","R442.1","U410.2"); N("AGND","U410.3"); N("GRP","U410.1","R442.2")
N("+15V","R443.1"); N("T5","R443.2","R444.1"); N("T4","R444.2","R445.1"); N("T3","R445.2","R446.1"); N("T2","R446.2","R447.1"); N("T1","R447.2","R448.1"); N("AGND","R448.2")
units=[("U411",5,4,2),("U94112",7,6,1),("U94113",11,10,13),("U94114",9,8,14),("U412",5,4,2)]
for k,(ref,pp,pm,po) in enumerate(units,start=1):     # k = 1 (1 dB) ... 5 (15 dB); LED on when GRP > Tk
    N(f"T{k}",f"{ref}.{pp}"); N("GRP",f"{ref}.{pm}"); N(f"GR{k}",f"{ref}.{po}",f"D{406+k}.1")
    N(f"GRA{k}",f"D{406+k}.2",f"R{448+k}.2"); N("+5V",f"R{448+k}.1")
for ref,pp,pm in (("U94122",7,6),("U94123",11,10),("U94124",9,8)):   # spare comparators: output held low, outputs open
    N("AGND",f"{ref}.{pp}"); N("+5V",f"{ref}.{pm}")
# ---------------------------------------------------------------- ON/OFF button
N("ON_CTRL","SW401.3","R455.2"); N("+5V","SW401.2"); N("ON_LEDK","SW401.6","D412.1"); N("PGND","SW401.5")
N("ON_LED","D412.2","R454.2"); N("+15V","R454.1"); N("AGND","R455.1")
# ---------------------------------------------------------------- test pads
for tp,net in (("TP401","VD"),("TP402","VC"),("TP403","VAMT"),("TP404","WET_L")): N(net,f"{tp}.1")
# ---------------------------------------------------------------- supplies and decoupling
for ref in ("U94033","U94043","U94053","U94063","U94073","U94083","U94093","U94103"): N("+15V",f"{ref}.8"); N("-15V",f"{ref}.4")
for ref in ("U94115","U94125"): N("+15V",f"{ref}.3"); N("PGND",f"{ref}.12")
N("+15V","U94135.13"); N("-15V","U94135.4"); N("+5V","U94135.12"); N("AGND","U94135.5")
for k in range(9):
    N("+15V",f"C{412+2*k}.1"); N("AGND",f"C{412+2*k}.2"); N("-15V",f"C{413+2*k}.1"); N("AGND",f"C{413+2*k}.2")
for c in ("C430","C431"): N("+15V",f"{c}.1"); N("PGND",f"{c}.2")
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'compressor.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
