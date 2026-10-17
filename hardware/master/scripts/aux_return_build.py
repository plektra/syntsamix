# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""AUX return sheets: reference netlists (build/aux_return1.json, build/aux_return2.json).

Per return (decision 51): L/MONO and R 6.3 mm jacks (R normalled to L) on the rear input row board (decision 163), RFI filters,
TL072 difference receiver at G = ½ wired inverting (decision 148, as the channel's decision 143), 1.6 Hz AC coupling,
inverting gain stage with a jumper per side (fitted -6 dB pro/Eurorack, open +6 dB pedal),
SSI2162 VCA with the channel fader law (decision 72) on a 10 kΩ linear level pot,
MUTE and DUCK switched by the buttons' spare poles (decision 177, as the channel's 142), unity inverter,
22 kΩ bus resistors switched to MAIN or COMP by a DG413 (pressed = COMP). Return n uses references n*100 + 1 ... (2xx, 3xx).
"""
import json,os,sys
def build(n):
    B=100*n+100   # return 1 -> 200, return 2 -> 300
    nets={}
    def N(net,*pins):
        for p in pins:
            r,q=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":q})
    r=lambda k:f"R{B+k}"; c=lambda k:f"C{B+k}"; u=lambda k:f"U{B+k}"; t=lambda k,unit:f"U9{B+k}{unit}"
    # jacks J1 L/MONO, J2 R (R normalled to L) sit on the rear input row board (decision 163): the four legs arrive as hierarchical labels
    N(f"RET{n}_L+",f"{r(1)}.1"); N(f"RET{n}_L-",f"{r(2)}.1"); N(f"RET{n}_R+",f"{r(3)}.1"); N(f"RET{n}_R-",f"{r(4)}.1")
    # RFI filters and receiver: TL072 difference amplifier G = 1/2, hot to the inverting leg (decision 148)
    # leg resistors 10k 0.1 %: R1-R4 (input, with the RFI caps), Ri, Rf, Rni, Rg per side
    for side,(rp,cp,rn,cn),(ri,rf,rni,rg),(ref,pp,pm,po),cpl in (("L",(1,1,2,2),(45,46,47,48),(u(1),3,2,1),5),
                                                             ("R",(3,3,4,4),(49,50,51,52),(t(1,2),5,6,7),6)):
        N(f"{side}_P",f"{r(rp)}.2",f"{c(cp)}.1",f"{r(ri)}.1"); N(f"{side}_RXN",f"{r(ri)}.2",f"{r(rf)}.1",f"{ref}.{pm}")
        N(f"{side}_RX",f"{ref}.{po}",f"{r(rf)}.2",f"{c(cpl)}.1")
        N(f"{side}_N",f"{r(rn)}.2",f"{c(cn)}.1",f"{r(rni)}.1"); N(f"{side}_RXP",f"{r(rni)}.2",f"{r(rg)}.2",f"{ref}.{pp}")
        N("AGND",f"{r(rg)}.1",f"{c(cp)}.2",f"{c(cn)}.2")
    # coupling and gain stage (U+2 TL072 since decision 173): -1 with the jumper fitted, -4 open
    for side,cc,rin,rf,rs,cf,(ref,pm,pp,po),jp in (("L",5,5,7,9,7,(u(2),2,3,1),(1,2)),("R",6,6,8,10,8,(t(2,2),6,5,7),(3,4))):
        N(f"{side}_CPL_M",f"{c(cc)}.2",f"{c(cc+29)}.2"); N(f"{side}_CPL",f"{c(cc+29)}.1",f"{r(rin)}.1")   # back to back (decision 172); N(f"{side}_SUM",f"{r(rin)}.2",f"{r(rf)}.1",f"{c(cf)}.1",f"{ref}.{pm}")
        N("AGND",f"{ref}.{pp}"); N(f"{side}_MID",f"{r(rf)}.2",f"{r(rs)}.1",f"J{B+3}.{jp[0]}")
        N(f"{side}_RET",f"{r(rs)}.2",f"J{B+3}.{jp[1]}",f"{c(cf)}.2",f"{ref}.{po}",f"{c(9 if side=='L' else 10)}.1")
    # VCA (U+3 SSI2162), I-V (U+4), inverter (U+5)
    for side,cv,rin,rr,crc,iin,iout,(iv,ivp),(inv,invp),rfb,cfb,rinv,rinvf in (
        ("L",9,11,13,11,2,4,(u(4),(2,3,1)),(u(5),(2,3,1)),15,13,17,19),
        ("R",10,12,14,12,9,7,(t(4,2),(6,5,7)),(t(5,2),(6,5,7)),16,14,18,20)):
        up=side=="L"   # L network is drawn upwards: pin order follows the drawing (electrically identical)
        N(f"{side}_VIN_M",f"{c(cv)}.2",f"{c(cv+27)}.2"); N(f"{side}_VIN",f"{c(cv+27)}.1",f"{r(rin)}.1"); N(f"{side}_IIN",f"{r(rin)}.2",f"{r(rr)}.{2 if up else 1}",f"{u(3)}.{iin}")
        N(f"{side}_RC",f"{r(rr)}.{1 if up else 2}",f"{c(crc)}.{2 if up else 1}"); N("AGND",f"{c(crc)}.{1 if up else 2}")
        N(f"{side}_IOUT",f"{u(3)}.{iout}",f"{iv}.{ivp[0]}",f"{r(rfb)}.1",f"{c(cfb)}.1"); N("AGND",f"{iv}.{ivp[1]}")
        N(f"{side}_VO",f"{iv}.{ivp[2]}",f"{r(rfb)}.2",f"{c(cfb)}.2",f"{r(rinv)}.1")
        N(f"{side}_INV",f"{r(rinv)}.2",f"{r(rinvf)}.1",f"{inv}.{invp[0]}"); N("AGND",f"{inv}.{invp[1]}")
        N(f"{side}_OUT",f"{inv}.{invp[2]}",f"{r(rinvf)}.2",f"{r(34 if side=='L' else 35)}.1")
    N("VC",f"{u(3)}.3",f"{u(3)}.8"); N("MODE",f"{u(3)}.1",f"{r(21)}.2"); N("+15V",f"{r(21)}.1",f"{u(3)}.10"); N("-15V",f"{u(3)}.6"); N("AGND",f"{u(3)}.5")
    # level law (as the channel fader, decision 72): pot, buffer, two superdiodes, summer
    # U+6 = OPA2171 (buffer A, summer B; input range includes V-), U+7 = TL072 (superdiodes), as decision 102
    RV=f"RV{B+1}"
    N("-15V",f"{RV}.1"); N("POTW",f"{RV}.2",f"{u(6)}.3"); N("AGND",f"{RV}.3"); N("VB",f"{u(6)}.2",f"{u(6)}.1",f"{r(22)}.1",f"{r(24)}.1",f"{r(27)}.1")
    N("VSUM",f"{r(42)}.2",f"{r(43)}.2",f"{r(26)}.2",f"{r(29)}.2",f"{r(30)}.1",f"{c(15)}.1",f"{r(31)}.2",f"{r(32)}.2",f"{t(6,2)}.6")
    N("+15V",f"{r(23)}.1",f"{r(25)}.1",f"{r(44)}.1")
    # E24 pairs (decision 140 values): r22+r42 = 113k, r23+r43 = 450k, r28+r44 = 124k
    N("RA_MID",f"{r(22)}.2",f"{r(42)}.1"); N("RC_MID",f"{r(23)}.2",f"{r(43)}.1"); N("RQ2_MID",f"{r(28)}.1",f"{r(44)}.2")
    N("SD1IN",f"{r(24)}.2",f"{r(25)}.2",f"{t(7,2)}.5"); N("SD1K",f"{t(7,2)}.6",f"D{B+1}.2",f"{r(26)}.1"); N("SD1O",f"{t(7,2)}.7",f"D{B+1}.1")
    N("SD2IN",f"{r(27)}.2",f"{r(28)}.2",f"{u(7)}.3"); N("SD2K",f"{u(7)}.2",f"D{B+2}.2",f"{r(29)}.1"); N("SD2O",f"{u(7)}.1",f"D{B+2}.1")
    N("VC",f"{t(6,2)}.7",f"{r(30)}.2",f"{c(15)}.2"); N("AGND",f"{t(6,2)}.5")   # summer + input on AGND (decision 97)
    N("MUTE_V",f"{r(31)}.1"); N("DUCK_V",f"{r(32)}.1")
    # bus assign: DG413 U+9, NC to MAIN, NO to COMP (pressed = COMP)
    N("L_BUS",f"{r(34)}.2",f"{t(9,4)}.15",f"{u(9)}.2"); N("MAIN_L",f"{t(9,4)}.14"); N("COMP_L",f"{u(9)}.3")
    N("R_BUS",f"{r(35)}.2",f"{t(9,3)}.10",f"{t(9,2)}.6"); N("MAIN_R",f"{t(9,3)}.11"); N("COMP_R",f"{t(9,2)}.7")
    N("COMP_CTRL",f"{u(9)}.1",f"{t(9,4)}.16",f"{t(9,3)}.9",f"{t(9,2)}.8")
    # buttons. MUTE and DUCK (decision 177, as channel 142): pole 1 switches the control voltage itself (pressed 2-3: source into
    # R31/R32); pin 1 open and the 100k holds the line at AGND when released. COMP stays a logic line to the DG413 U+9
    for name,k,src in (("MUTE",1,"-15V"),("DUCK",2,"SC_ENV"),("COMP",3,None)):
        sw,led,rl,rp=f"SW{B+k}",f"D{B+2+k}",r(35+2*k-1),r(35+2*k)
        if src: N(f"{name}_V",f"{sw}.2",f"{rp}.2"); N(src,f"{sw}.3"); N("AGND",f"{rp}.1")
        else: N(f"{name}_CTRL",f"{sw}.3",f"{rp}.2"); N("+5V",f"{sw}.2"); N("PGND",f"{rp}.1")   # pull-down to PGND (decision 98)
        N(f"{name}_LEDK",f"{sw}.6",f"{led}.1"); N("PGND",f"{sw}.5")
        N(f"{name}_LED",f"{led}.2",f"{rl}.2"); N("+15V",f"{rl}.1")
    # test pads
    N("L_RET",f"TP{B+1}.1"); N("R_RET",f"TP{B+2}.1"); N("VC",f"TP{B+3}.1")
    # supplies and decoupling
    for ref in (t(1,3),t(2,3),t(4,3),t(5,3),t(6,3),t(7,3)): N("+15V",f"{ref}.8"); N("-15V",f"{ref}.4")
    for ref in (t(9,5),): N("+15V",f"{ref}.13"); N("-15V",f"{ref}.4"); N("+5V",f"{ref}.12"); N("AGND",f"{ref}.5")
    for k in range(8):   # C232/C233 went with U+8 (decision 177)
        N("+15V",f"{c(16+2*k)}.1"); N("AGND",f"{c(16+2*k)}.2"); N("-15V",f"{c(17+2*k)}.1"); N("AGND",f"{c(17+2*k)}.2")
    return nets
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
for n in (1,2):
    nets=build(n)
    json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+f'aux_return{n}.json','w'))
    print(f"return {n}:",len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
