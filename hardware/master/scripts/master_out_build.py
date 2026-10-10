# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Master out sheet reference netlist (build/master_out.json), written independently of the drawing.

Decisions 46, 64, 83, 85 and 92. MAIN_L/R_SUM (inverted by the summing amps) into an
SSI2162 (one VC for both sides) with I-V stages (NE5532, 10 kΩ ∥ 100 pF) that carry the
soft clip (back-to-back 6V2 zeners with 4.7 kΩ, onset about +14 dBu as on the channels);
their outputs are MAIN_L/R_OUT (meter, headphones). DRV135 balanced drivers (THAT1646 pinout, decision 125; +6 dB) with
10 µF common-mode offset capacitors and rail clamp diodes (THAT doc 600078 Figures 5 and 8),
then G6K-2F-Y relays: energised = driver to the jack, released = each conductor to AGND
through 1 kΩ (pole 2 hot, pole 1 cold). Master level: the channel fader law on a 10 kΩ linear pot.
Relay control (LM339, +15 V / PGND): comparator A drops the relays at once when the raw
+20 V falls below about 17.9 V, comparator C when the raw -20 V rises above about -17.9 V (decision 128); comparator B closes them about 2 s after power-up;
an MMBT3904 sinks the coils (RLY_N also drives the headphone relay on its own sheet).
G6K-2 pins (KiCad Relay library): 1 coil +, 8 coil -, pole 1 COM 3 / NC 2 / NO 4, pole 2 COM 6 / NC 7 / NO 5.
"""
import json,os
nets={}
def N(net,*pins):
    for p in pins:
        r,q=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":q})
# ---------------------------------------------------------------- VCA and I-V with soft clip
for side,(cin,rin,rrc,crc,riv,civ,rz,dza,dzb,iin,iout,(iv,pm,pp,po)) in (
        ("L",("C701","R701","R703","C703","R706","C705","R708","D701","D702","2","4",("U702",2,3,1))),
        ("R",("C702","R702","R704","C704","R707","C706","R709","D703","D704","9","7",("U97022",6,5,7)))):
    N(f"MAIN_{side}_SUM",f"{cin}.1"); N(f"{side}_VIN",f"{cin}.2",f"{rin}.1")
    up=side=="R"   # R network drawn upwards
    N(f"{side}_IIN",f"{rin}.2",f"{rrc}.{2 if up else 1}",f"U701.{iin}"); N(f"{side}_RC",f"{rrc}.{1 if up else 2}",f"{crc}.{2 if up else 1}"); N("AGND",f"{crc}.{1 if up else 2}")
    N(f"{side}_IOUT",f"U701.{iout}",f"{iv}.{pm}",f"{riv}.1",f"{civ}.1",f"{dzb}.1"); N("AGND",f"{iv}.{pp}")
    N(f"{side}_ZK",f"{dzb}.2",f"{dza}.2"); N(f"{side}_ZR",f"{dza}.1",f"{rz}.1")
    N(f"MAIN_{side}_OUT",f"{iv}.{po}",f"{riv}.2",f"{civ}.2",f"{rz}.2")
N("VC","U701.3","U701.8","TP703.1"); N("MODE","U701.1","R705.2"); N("+15V","R705.1","U701.10"); N("-15V","U701.6"); N("AGND","U701.5")
N("MAIN_L_OUT","TP701.1"); N("MAIN_R_OUT","TP702.1")
# ---------------------------------------------------------------- THAT1646 drivers, clamps, relays, jacks
for side,(u,ccp,ccn,dpp,dpn,dnp,dnn,k,rgh,rgc,j) in (
        ("L",("U703","C707","C708","D705","D706","D707","D708","K701","R710","R711","J701")),
        ("R",("U704","C709","C710","D709","D710","D711","D712","K702","R712","R713","J702"))):
    N(f"MAIN_{side}_OUT",f"{u}.4"); N("AGND",f"{u}.3"); N("+15V",f"{u}.6"); N("-15V",f"{u}.5")
    # pole 2 (COM 6, NC 7, NO 5) carries the hot leg, pole 1 (COM 3, NC 2, NO 4) the cold leg
    N(f"{side}_OP",f"{u}.8",f"{ccp}.1",f"{dpp}.2",f"{dnp}.1",f"{k}.5"); N(f"{side}_SP",f"{u}.7",f"{ccp}.2")
    N(f"{side}_ON",f"{u}.1",f"{ccn}.2",f"{dpn}.2",f"{dnn}.1",f"{k}.4"); N(f"{side}_SN",f"{u}.2",f"{ccn}.1")
    N("+15V",f"{dpp}.1",f"{dpn}.1"); N("-15V",f"{dnp}.2",f"{dnn}.2")      # D pin 1 = K: clamps to the rails
    N(f"{side}_HOT",f"{k}.6",f"{j}.T"); N(f"{side}_GH",f"{k}.7",f"{rgh}.1"); N("AGND",f"{rgh}.2")
    N(f"{side}_COLD",f"{k}.3",f"{j}.R"); N(f"{side}_GC",f"{k}.2",f"{rgc}.1"); N("AGND",f"{rgc}.2")
    N("AGND",f"{j}.S")
# ---------------------------------------------------------------- master level law (as the channel fader, decision 72)
# U705 = OPA2171 (buffer A, summer B), U706 = TL072 (superdiodes), as decision 102
N("-15V","RV701.1"); N("POTW","RV701.2","U705.3"); N("AGND","RV701.3"); N("VB","U705.2","U705.1","R714.1","R716.1","R719.1")
N("VSUM","R734.2","R735.2","R718.2","R721.2","R722.1","C711.1","U97052.6"); N("AGND","U97052.5"); N("VC","U97052.7","R722.2","C711.2")
N("+15V","R715.1","R717.1","R736.1")
# E24 pairs (decision 140 values): R714+R734 = 113k, R715+R735 = 450k, R720+R736 = 124k
N("RA_MID","R714.2","R734.1"); N("RC_MID","R715.2","R735.1"); N("RQ2_MID","R720.1","R736.2")
N("SD1IN","R716.2","R717.2","U97062.5"); N("SD1K","U97062.6","D713.2","R718.1"); N("SD1O","U97062.7","D713.1")
N("SD2IN","R719.2","R720.2","U706.3"); N("SD2K","U706.2","D714.2","R721.1"); N("SD2O","U706.1","D714.1")
# ---------------------------------------------------------------- relay control
N("+20V_RAW","R723.1"); N("RAW_DIV","R723.2","R724.1","U707.5"); N("PGND","R724.2")
N("+15V","R725.1"); N("REF","R725.2","R726.1","U707.4","U97072.6"); N("PGND","R726.2")
N("UV_O","U707.2","R727.1"); N("TIMER","R727.2","R728.2","C712.1","U97072.7","TP704.1"); N("+15V","R728.1"); N("PGND","C712.2")
N("RLY_B","U97072.1","R729.2","Q701.1"); N("+15V","R729.1"); N("PGND","Q701.2"); N("RLY_N","Q701.3","K701.8","K702.8","D715.2","D716.2")
# C: raw -20 V through 22k6 / 100k from +15 V against REF (decision 128): NEG_DIV rises above REF when the
# raw -20 V is weaker than about -17.9 V; its output joins UV_O (open collector, wired OR with A)
N("+15V","R737.1"); N("NDIV_TOP","R737.2","R732.1"); N("NEG_DIV","R732.2","R733.1","U97073.10"); N("-20V_RAW","R733.2"); N("REF","U97073.11"); N("UV_O","U97073.13")
N("+15V","R730.2","R731.2"); N("K1P","R730.1","K701.1","D715.1"); N("K2P","R731.1","K702.1","D716.1")
for ref,pp,pm in (("U97074",9,8),):   # spare comparators: output held low, outputs open
    N("PGND",f"{ref}.{pp}"); N("+5V",f"{ref}.{pm}")
# ---------------------------------------------------------------- supplies and decoupling
for ref in ("U97023","U97053","U97063"): N("+15V",f"{ref}.8"); N("-15V",f"{ref}.4")
N("+15V","U97075.3"); N("PGND","U97075.12")
for k in range(6):
    N("+15V",f"C{713+2*k}.1"); N("AGND",f"C{713+2*k}.2"); N("-15V",f"C{714+2*k}.1"); N("AGND",f"C{714+2*k}.2")
N("+15V","C725.1"); N("PGND","C725.2")
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'master_out.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
