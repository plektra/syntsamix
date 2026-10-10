# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Level sheet, drawn with real wires (pilot for readable sheets).

Same parts, references and connections as level_build.py, which stays the
reference netlist: check_netlist.py level.json compares this drawing with it.
Layout: L and R audio rows across the top (input network, SSI2162, I-V stage,
polarity inverter), the fader-law control circuit below, then the DG413
mute/duck switches, the buttons and the supply decoupling.
"""
import json,os
from schlayout import Sheet,pins_of
R0805="Resistor_SMD:R_0805_2012Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"
CBIP="Capacitor_SMD:C_Elec_6.3x5.4"; SO8="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"; SO16="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm"   # decision 111: SMD bipolar, 5.4 mm tall
TI={"Manufacturer":"Texas Instruments"}; VI={"Manufacturer":"Vishay"}
ST={"Manufacturer":"STMicroelectronics","MPN":"TL072CDT","Supplier":"LCSC","SupplierPN":"C6961"}   # SX-IC-007, JLCPCB basic (decision 137)
s=Sheet()
P=lambda pn,**k: {"ProjectPN":pn,**k}
def R(ref,val,pn,x,y,rot=90,fp=R0805,**k): return s.place("Device","R",ref,val,x,y,rot,fp=fp,props=P(pn,**k))
def C(ref,val,pn,x,y,rot=90,fp=C0805,**k): return s.place("Device","C",ref,val,x,y,rot,fp=fp,props=P(pn,**k))
SYM={"OPA2171":"Opamp_Dual"}; MPN={"OPA2171":{"MPN":"OPA2171AIDR"},"TL072":ST}   # no OPA2171 symbol in the KiCad library; same pinout
def OA(part,ref,unit,x,y,pn): return s.place("Amplifier_Operational",SYM.get(part,part),ref,part,x,y,0,unit,SO8,P(pn,**{**TI,**MPN.get(part,{})}))
def gnd(at,rot=0): s.power("GNDA",at,rot)       # renamed to AGND in post-processing
def pgnd(at,rot=0): s.power("GNDPWR",at,rot)    # renamed to PGND in post-processing
def up(p,d=2.54): return (p[0],p[1]-d)
def dn(p,d=2.54): return (p[0],p[1]+d)
def lt(p,d=2.54): return (p[0]-d,p[1])
def rt(p,d=2.54): return (p[0]+d,p[1])

# ------------------------------------------------------------- VCA chip
XV,YV=175.26,101.6
v=s.place("syntsamix","SSI2162","U201","SSI2162",XV,YV,0,fp="Package_SO:SSOP-10_3.9x4.9mm_P1.00mm",
          props=P("SX-IC-002",Manufacturer="Sound Semiconductor",MPN="SSI2162SS-TU",Supplier="Electrokit",SupplierPN="41019302"))
s.wire(v(10),up(v(10),5.08)); s.power("+15V",up(v(10),5.08))
s.wire(v(6),dn(v(6),5.08)); s.power("-15V",dn(v(6),5.08))
s.wire(v(5),dn(v(5),5.08),rt(dn(v(5),5.08),5.08)); gnd(rt(dn(v(5),5.08),5.08))
# control inputs VC1, VC2 joined, labelled VC
vc=dn(v(3),7.62); s.wire(v(3),vc); s.wire(v(8),dn(v(8),7.62)); s.wire(vc,dn(v(8),7.62))
s.wire(vc,lt(vc,5.08)); s.label("VC",lt(vc,5.08),180)
# mode resistor (DNP = Class AB)
m=up(v(1),7.62); s.wire(v(1),m,lt(m,7.62))
r=R("R206","14k3","SX-R-030",m[0]-7.62,m[1]-3.81,0,Note="DNP = Class AB (default); fit for Class A, mode current about 1 mA (datasheet Rev 1.2)")
s.wire(r(1),up(r(1),2.54)); s.power("+15V",up(r(1),2.54))

# ------------------------------------------------------------- audio rows
def audio(Pn,o,y,iin,iout,iv,inv,rc_up):
    c=lambda n:f"C{n+o+20}"; rr=lambda n:f"R{n+o}"
    x0=30.48
    s.wire((x0,y),(41.91,y)); s.label(f"{Pn}_POSTFILT",(x0,y),180,"hierarchical","input")
    ci=C(c(201),"10u bipolar","SX-C-023",45.72,y,fp=CBIP,Manufacturer="Panasonic",MPN="EEE-1VA100NP",Supplier="Mouser",SupplierPN="667-EEE-1VA100NP")
    ri=R(rr(201),"10k","SX-R-002",63.5,y)
    s.wire(ci(2),ri(1))
    node=(78.74,y); s.wire(ri(2),node)
    # input stability network 110R + 2n2 (up for L, down for R)
    sgn=-1 if rc_up else 1
    rot=0
    rn=R(rr(202),"100","SX-R-001",node[0],y+sgn*11.43,rot)
    cn=C(c(202),"2n2 C0G","SX-C-009",node[0],y+sgn*26.67,rot)
    if rc_up:
        s.wire(node,rn(2)); s.wire(rn(1),cn(2)); gnd(cn(1),180)
    else:
        s.wire(node,rn(1)); s.wire(rn(2),cn(1)); gnd(cn(2))
    # to the VCA input
    if abs(iin[1]-y)<0.01: s.wire(node,iin)
    else: s.wire(node,(iin[0]-5.08,y),(iin[0]-5.08,iin[1]),iin)
    # I-V converter (inverting), feedback below
    yv=y; X1=205.74
    a=OA("NE5532",iv[0],iv[1],X1,yv-2.54,"SX-IC-004")
    if abs(iout[1]-yv)<0.01: s.wire(iout,a(iv[2][0]))
    else: s.wire(iout,(iout[0]+2.54,iout[1]),(iout[0]+2.54,yv),a(iv[2][0]))
    s.wire(a(iv[2][1]),lt(a(iv[2][1]),2.54),up(lt(a(iv[2][1]),2.54),2.54)); gnd(up(lt(a(iv[2][1]),2.54),2.54),180)
    nfb=(X1-10.16,yv); out=(X1+10.16,yv-2.54)
    s.wire(a(iv[2][2]),out)
    rf=R(rr(203),"10k","SX-R-002",X1,yv+10.16); cf=C(c(203),"100p C0G","SX-C-008",X1,yv+20.32)
    s.wire(nfb,(nfb[0],yv+20.32)); s.wire(nfb,(nfb[0],yv+10.16))   # split for junction
    s.wire((nfb[0],yv+10.16),rf(1)); s.wire((nfb[0],yv+20.32),cf(1))
    s.wire(rf(2),(out[0],yv+10.16)); s.wire(cf(2),(out[0],yv+20.32))
    s.wire((out[0],yv+20.32),(out[0],yv+10.16)); s.wire((out[0],yv+10.16),out)
    # polarity inverter
    X2=246.38; yi=yv-2.54
    ri2=R(rr(204),"10k","SX-R-002",228.6,yi)
    s.wire(out,ri2(1))
    b=OA("NE5532",inv[0],inv[1],X2,yi-2.54,"SX-IC-004")
    n2=(X2-10.16,yi); s.wire(ri2(2),n2,b(inv[2][0]))
    s.wire(b(inv[2][1]),lt(b(inv[2][1]),2.54),up(lt(b(inv[2][1]),2.54),2.54)); gnd(up(lt(b(inv[2][1]),2.54),2.54),180)
    o2=(X2+10.16,yi-2.54); s.wire(b(inv[2][2]),o2)
    rf2=R(rr(205),"10k","SX-R-002",X2,yi+10.16)
    s.wire(n2,(n2[0],yi+10.16),rf2(1)); s.wire(rf2(2),(o2[0],yi+10.16),o2)
    s.wire(o2,(279.4,o2[1])); s.label(f"{Pn}_POSTFADE",(279.4,o2[1]),0,"hierarchical","output")
    s.tp("TP203" if Pn=="L" else "TP204",f"{Pn}_POSTFADE",(271.78,o2[1]),"down")
audio("L",0,v(2)[1],v(2),v(4),("U202",1,(2,3,1)),("U203",1,(2,3,1)),True)
audio("R",50,147.32,v(9),v(7),("U92022",2,(6,5,7)),("U92032",2,(6,5,7)),False)

# ------------------------------------------------------------- fader law
fv=s.place("Device","R_Potentiometer","RV201","10k lin FADER",45.72,210.82,0,fp="Potentiometer_THT:Potentiometer_Bourns_PTA6043_Single_Slide",
           props=P("SX-POT-001",Manufacturer="Bourns",MPN="PTA6043-2015DPB103",Note="Pin 1 = bottom of travel (datasheet: output rises from terminal 1)"))
s.wire(fv(1),up(fv(1),5.08)); s.power("-15V",up(fv(1),5.08),180)
s.wire(fv(3),dn(fv(3),5.08)); gnd(dn(fv(3),5.08))
bu=OA("OPA2171","U204",1,68.58,213.36,"SX-IC-021")
s.wire(fv(2),bu(3))
VBX=96.52; bo=(78.74,213.36)
s.wire(bu(1),bo,(VBX,213.36))
s.wire(bo,(78.74,220.98),(58.42,220.98),(58.42,bu(2)[1]),bu(2))
SUMX=241.3
# row 1: Ra from VB, row 2: Rc from +15 V
ra=R("R207","113k","SX-R-023",170.18,190.5); s.wire((VBX,190.5),ra(1)); s.wire(ra(2),(SUMX,190.5))
rc=R("R208","453k","SX-R-024",170.18,200.66); s.wire((152.4,200.66),rc(1)); s.power("+15V",(152.4,200.66)); s.wire(rc(2),(SUMX,200.66))
# superdiode breakpoints
def superdiode(y,rp,rq,rqval,rqpn,opa,unit,pins,d,rs,rsval,rspn):
    a=R(rp,"100k","SX-R-007",106.68,y); s.wire((VBX,y),a(1))
    nd=(114.3,y); s.wire(a(2),nd)
    q=R(rq,rqval,rqpn,114.3,y-10.16,0); s.wire(nd,q(2)); s.wire(q(1),up(q(1),1.27)); s.power("+15V",up(q(1),1.27))
    o=OA("TL072",opa,unit,129.54,y+2.54,"SX-IC-007")
    s.wire(nd,o(pins[0]))
    dd=s.place("Device","D",d,"1N4148W",144.78,y+2.54,0,fp="Diode_SMD:D_SOD-123",props=P("SX-D-003"))
    s.wire(o(pins[2]),dd(1)); k=(152.4,y+2.54); s.wire(dd(2),k)
    s.wire(k,(k[0],y+10.16),(119.38,y+10.16),(119.38,o(pins[1])[1]),o(pins[1]))
    r=R(rs,rsval,rspn,200.66,y+2.54); s.wire(k,r(1)); s.wire(r(2),(SUMX,y+2.54))
    return y+2.54
superdiode(231.14,"R209","R210","221k","SX-R-025","U92052",2,(5,6,7),"D201","R211","63k4","SX-R-026")
superdiode(264.16,"R212","R213","124k","SX-R-027","U205",1,(3,2,1),"D202","R214","8k66","SX-R-014")
s.wire((VBX,190.5),(VBX,213.36)); s.wire((VBX,213.36),(VBX,231.14)); s.wire((VBX,231.14),(VBX,264.16))
# duck and mute inputs
rd=R("R217","30k1","SX-R-087",220.98,279.4,Note="SC_ENV into the virtual earth: 0.332 V/V, 10 dB of ducking per -1 V (decision 97)")
s.wire((208.28,279.4),rd(1)); s.label("DUCK_V",(208.28,279.4),180); s.wire(rd(2),(SUMX,279.4))
rm=R("R216","33k2","SX-R-028",220.98,289.56); s.wire((208.28,289.56),rm(1)); s.label("MUTE_V",(208.28,289.56),180); s.wire(rm(2),(SUMX,289.56))
# summing junction bus (split at every tap so each joint gets a junction)
taps=sorted({172.72,182.88,190.5,200.66,218.44,233.68,266.7,279.4,289.56})
for y1,y2 in zip(taps,taps[1:]): s.wire((SUMX,y1),(SUMX,y2))
su=OA("OPA2171","U92042",2,256.54,215.9,"SX-IC-021")
s.wire((SUMX,218.44),su(6))
s.wire(su(5),lt(su(5),2.54),up(lt(su(5),2.54),2.54)); gnd(up(lt(su(5),2.54),2.54),180)
so=(266.7,215.9); s.wire(su(7),so,(279.4,215.9)); s.label("VC",(279.4,215.9),0)
s.tp("TP201","VC",(274.32,215.9),"down")
s.tp("TP202","VB",(88.9,213.36),"up")
rf=R("R215","10k","SX-R-002",254.0,182.88); cf=C("C224","1u","SX-C-010",254.0,172.72,Note="10 ms control smoothing: fader wiper noise and click-free mute ramp")
s.wire((SUMX,182.88),rf(1)); s.wire((SUMX,172.72),cf(1)); s.wire(rf(2),(so[0],182.88)); s.wire(cf(2),(so[0],172.72))
s.wire((so[0],172.72),(so[0],182.88)); s.wire((so[0],182.88),so)

# ------------------------------------------------------------- DG413: duck and mute
DGX=330.2
d1=s.place("Analog_Switch","DG413xY","U206","DG413DY",DGX,203.2,0,1,SO16,P("SX-IC-005",**VI))
s.wire(d1(2),lt(d1(2),7.62)); s.label("DUCK_V",lt(d1(2),7.62),180)
s.wire(d1(3),(350.52,203.2)); s.label("SC_ENV",(350.52,203.2),0,"hierarchical","input")
s.tp("TP205","SC_ENV",(345.44,203.2),"up")
s.wire(d1(1),dn(d1(1),5.08)); s.label("DUCK_CTRL",dn(d1(1),5.08),270)
d4=s.place("Analog_Switch","DG413xY","U92062","DG413DY",DGX,238.76,0,2,SO16,P("SX-IC-005",**VI))
s.wire(d4(6),lt(d4(6),5.08)); s.power("-15V",lt(d4(6),5.08))
s.wire(d4(7),(345.44,238.76)); s.label("MUTE_V",(345.44,238.76),0)
s.wire(d4(8),dn(d4(8),5.08)); s.label("MUTE_CTRL",dn(d4(8),5.08),270)
for ref,unit,y in (("U92063",3,264.16),("U92064",4,289.56)):
    u=s.place("Analog_Switch","DG413xY",ref,"DG413DY",DGX,y,0,unit,SO16,P("SX-IC-005",**VI))
    for n,(px,py,ang) in pins_of("Analog_Switch","DG413xY",unit).items():
        p=u(n)
        e={0:lt(p,5.08),180:rt(p,5.08),90:dn(p,5.08)}[int(ang)]
        s.wire(p,e); gnd(e)

# ------------------------------------------------------------- buttons
def button(name,sw,led,rl,rp,x,y):
    b=s.place("Switch","SW_Push_DPDT",sw,f"{name} (latching)",x,y,0,fp="syntsamix:SW_Latching_8.5x8.5mm_CW_GPBS850N",props=P("SX-SW-001",Manufacturer="CW Industries",MPN="GPBS850N",Supplier="Electrokit",SupplierPN="41012905"))
    s.wire(b(2),lt(b(2),5.08)); s.power("+5V",lt(b(2),5.08))
    s.wire(b(5),lt(b(5),5.08)); pgnd(lt(b(5),5.08))
    nd=(b(3)[0]+10.16,b(3)[1]); s.wire(b(3),nd,rt(nd,10.16)); s.label(f"{name}_CTRL",rt(nd,10.16),0)
    rpd=R(rp,"100k","SX-R-007",nd[0],nd[1]-7.62,0); s.wire(nd,rpd(2))
    g=lt(up(rpd(1),2.54),5.08); s.wire(rpd(1),up(rpd(1),2.54),g); pgnd(g)   # PGND (decision 98); symbol points down beside the resistor
    ld=s.place("Device","LED",led,f"{name} LED",b(6)[0]+22.86,b(6)[1],0,fp="LED_SMD:LED_0805_2012Metric",props=LEDPN[name])
    s.wire(b(6),ld(1))
    r=R(rl,"12k","SX-R-008",ld(2)[0]+8.89,b(6)[1],270); s.wire(ld(2),r(2)); s.wire(r(1),rt(r(1),3.81)); s.power("+15V",rt(r(1),3.81),270)
    return b
LEDPN={"MUTE":P("SX-D-015",Manufacturer="Foshan NationStar",MPN="NCD0805R1",Supplier="LCSC",SupplierPN="C84256"),"DUCK":P("SX-D-011",Manufacturer="Hubei KENTO",MPN="KT-0805G",Supplier="LCSC",SupplierPN="C2297")}   # button LED colours (user, 2026-10-09)
b1=button("MUTE","SW201","D203","R219","R220",60.96,358.14)
b2=button("DUCK","SW202","D204","R221","R222",157.48,358.14)
NOCONNECT=[b1(1),b1(4),b2(1),b2(4)]

# ------------------------------------------------------------- supplies and decoupling
x=210.82
for t,part in (("U92023","NE5532"),("U92033","NE5532"),("U92043","OPA2171"),("U92053","TL072")):
    u=s.place("Amplifier_Operational",SYM.get(part,part),t,part,x,358.14,0,3,SO8,P({"NE5532":"SX-IC-004","TL072":"SX-IC-007","OPA2171":"SX-IC-021"}[part],**{**TI,**MPN.get(part,{})}))
    s.wire(u(8),up(u(8),5.08)); s.power("+15V",up(u(8),5.08))
    s.wire(u(4),dn(u(4),5.08)); s.power("-15V",dn(u(4),5.08))
    x+=15.24
u=s.place("Analog_Switch","DG413xY","U92065","DG413DY",x+5.08,358.14,0,5,SO16,P("SX-IC-005",**VI))
s.wire(u(13),up(u(13),5.08)); s.power("+15V",up(u(13),5.08))
s.wire(u(12),up(u(12),2.54),rt(up(u(12),2.54),5.08)); s.power("+5V",rt(up(u(12),2.54),5.08))
s.wire(u(5),dn(u(5),5.08)); gnd(dn(u(5),5.08))
s.wire(u(4),dn(u(4),2.54),rt(dn(u(4),2.54),5.08)); s.power("-15V",rt(dn(u(4),2.54),5.08),0)
k=225; x=320.04
for i in range(6):
    cp=C(f"C{k}","100n","SX-C-002",x,345.44,0); s.power("+15V",cp(1)); gnd(cp(2)); k+=1
    cn=C(f"C{k}","100n","SX-C-002",x,373.38,0); s.wire(cn(1),up(cn(1),2.54)); s.power("-15V",up(cn(1),2.54),180); gnd(cn(2)); k+=1
    x+=12.7

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'level.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_level_wired.json','w'))
json.dump({"no_connect":NOCONNECT},open(T+'level_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols")
