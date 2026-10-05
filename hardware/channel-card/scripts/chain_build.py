# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Chain and power sheet reference netlist (build/chain.json), written independently of the drawing.

Audio ribbon 34-pin and power ribbon 8-pin, each as an IN/OUT pair wired straight
through (docs/CHAIN.md). LM317/LM337 make ±15.2 V from the raw ±20 V rails
(120 Ω / 1.33 kΩ, 10 µF on ADJ, protection diodes per the TI datasheets), a 78L05
makes +5 V for logic and LEDs. Input capacitors return to PGND; dividers, output
capacitors and the rail clamp Schottkys return to AGND (grounding rules in CHAIN.md).
"""
import json,os
nets={}
def N(net,*pins):
    for p in pins:
        r,n=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":n})
AUDIO={2:"MAIN_L",4:"MAIN_R",6:"COMP_L",8:"COMP_R",10:"AUX1_L",12:"AUX1_R",14:"AUX2_L",16:"AUX2_R",
       18:"CUE_L",20:"CUE_R",22:"SC",24:"SC_ENV",26:"SPARE2",28:"SPARE3",30:"SPARE4",32:"SPARE5",34:"PFL_ACT"}
for j in ("J501","J502"):
    for p in range(1,35,2): N("AGND",f"{j}.{p}")
    for p,net in AUDIO.items(): N(net,f"{j}.{p}")
for j in ("J503","J504"):
    N("-20V_RAW",f"{j}.1",f"{j}.2"); N("PGND",f"{j}.3",f"{j}.4",f"{j}.5",f"{j}.6"); N("+20V_RAW",f"{j}.7",f"{j}.8")
# +15 V: LM317 (1 ADJ, 2 VO, 3 VI)
N("+20V_RAW","U501.3","C501.1","C502.1","D501.1"); N("PGND","C501.2","C502.2")
N("+15V","U501.2","D501.2","R501.1","D502.1","C504.1","C505.1","D505.1")
N("ADJ_P","U501.1","R501.2","R502.1","C503.1","D502.2"); N("AGND","R502.2","C503.2","C504.2","C505.2","D505.2")
# -15 V: LM337 (1 ADJ, 2 VI, 3 VO)
N("-20V_RAW","U502.2","C506.2","C507.1","D503.2"); N("PGND","C506.1","C507.2")
N("-15V","U502.3","D503.1","R503.2","D504.2","C509.2","C510.1","D506.2")
N("ADJ_N","U502.1","R503.1","R504.2","C508.2","D504.1"); N("AGND","R504.1","C508.1","C509.1","C510.2","D506.1")
# +5 V: 78L05 (1 OUT, 2 GND, 3 IN)
N("+15V","U503.3","C511.1"); N("PGND","U503.2","C511.2","C512.2"); N("+5V","U503.1","C512.1")
# test pads
for tp,net in (("TP501","+20V_RAW"),("TP502","-20V_RAW"),("TP503","+15V"),("TP504","-15V"),("TP505","+5V"),("TP506","PGND")): N(net,f"{tp}.1")
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'chain.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
