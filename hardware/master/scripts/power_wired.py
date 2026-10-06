# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Master card power sheet, drawn with real wires.

Reference netlist: power_build.py (check_netlist.py power.json).
Regulator blocks follow the channel card (chain_wired.py); +5 V uses an L7805 for the
heavier LED load. AGND/PGND star point (net tie) and the frame ground lift.
"""
import json,os
from schlayout import Sheet,pins_of
R0805="Resistor_SMD:R_0805_2012Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"
CP47="Capacitor_THT:CP_Radial_D6.3mm_P2.50mm"; CP10="Capacitor_THT:CP_Radial_D5.0mm_P2.00mm"
TO220="Package_TO_SOT_THT:TO-220-3_Vertical"
s=Sheet()
P=lambda pn,**k: {"ProjectPN":pn,**k}
def R(ref,val,pn,x,y,rot=0): return s.place("Device","R",ref,val,x,y,rot,fp=R0805,props=P(pn))
def C(ref,val,pn,x,y,rot=0): return s.place("Device","C",ref,val,x,y,rot,fp=C0805,props=P(pn))
def CP(ref,val,pn,fp,x,y,rot=0): return s.place("Device","C_Polarized",ref,val,x,y,rot,fp=fp,props=P(pn))
def D(ref,val,pn,fp,x,y,rot): return s.place("Device","D",ref,val,x,y,rot,fp=fp,props=P(pn))
def gnd(at,rot=0): s.power("GNDA",at,rot)
def pgnd(at,rot=0): s.power("GNDPWR",at,rot)
def up(p,d=2.54): return (p[0],p[1]-d)
def dn(p,d=2.54): return (p[0],p[1]+d)
def lt(p,d=2.54): return (p[0]-d,p[1])
def rt(p,d=2.54): return (p[0]+d,p[1])

# ------------------------------------------------------------- power ribbon in (from the power board)
j=s.place("Connector_Generic","Conn_02x04_Odd_Even","J901","POWER IN",60.96,180.34,0,fp="Connector_IDC:IDC-Header_2x04_P2.54mm_Vertical",
          props=P("SX-CONN-008",Note="8-pin shrouded keyed box header: 1-2 V-, 3-6 PGND, 7-8 V+ (docs/CHAIN.md)"))
for side,pins,x in (("L",(1,3,5,7),j(1)[0]-5.08),("R",(2,4,6,8),j(2)[0]+5.08)):
    a,b,c,d=pins
    for p in pins: s.wire(j(p),(x,j(p)[1]))
    s.wire((x,j(b)[1]),(x,j(c)[1])); pg=(x+(-10.16 if side=="L" else 10.16),j(b)[1])
    s.wire((x,j(b)[1]),pg); pgnd(pg,90 if side=="L" else 270)
    e1=(x+(-7.62 if side=="L" else 7.62),j(a)[1]); s.wire((x,j(a)[1]),e1); s.label("-20V_RAW",e1,180 if side=="L" else 0)
    e2=(x+(-7.62 if side=="L" else 7.62),j(d)[1]); s.wire((x,j(d)[1]),e2); s.label("+20V_RAW",e2,180 if side=="L" else 0)
s.power("PWR_FLAG",(40.64,200.66)); s.wire((40.64,200.66),(40.64,205.74)); pgnd((40.64,205.74))

# ------------------------------------------------------------- +15 V (LM317) and -15 V (LM337)
XU=165.1   # regulator centre; VI at XU-7.62, VO at XU+7.62, ADJ below (LM317) / above (LM337)
def rail_in(y,label,tpref,flag_dir,cap47,cap100,neg):
    s.label(label,(119.38,y),180)
    x=(119.38,y)
    for xx in (124.46,132.08,137.16,142.24,152.4): s.wire(x,(xx,y)); x=(xx,y)
    s.power("PWR_FLAG",(124.46,y-5.08) if flag_dir=="up" else (124.46,y+5.08)); s.wire((124.46,y),(124.46,y-5.08) if flag_dir=="up" else (124.46,y+5.08))
    if neg: c=CP(cap47,"47u 35V","SX-C-011",CP47,132.08,y-3.81); pgnd(c(1),180)
    else:   c=CP(cap47,"47u 35V","SX-C-011",CP47,132.08,y+3.81); pgnd(c(2))
    c=C(cap100,"100n","SX-C-002",142.24,y+3.81); pgnd(c(2))
    s.tp(tpref,label,(137.16,y),flag_dir)
    return (152.4,y)
def rail_out(y,vo,stops):
    x=vo
    for xx in stops: s.wire(x,(xx,y)); x=(xx,y)

Y1=180.34
u=s.place("Regulator_Linear","LM317_TO-220","U901","LM317",XU,Y1,0,fp=TO220,props=P("SX-IC-010",Manufacturer="Texas Instruments",MPN="LM317"))
vin=rail_in(Y1,"+20V_RAW","TP901","up","C901","C902",False); s.wire(vin,u(3))
s.wire((119.38,Y1),(119.38,Y1+12.7)); s.label("+20V_RAW",(119.38,Y1+12.7),270,"hierarchical","output")   # to the relay drop-out comparator (Master out sheet)
d=D("D901","1N4148W","SX-D-003","Diode_SMD:D_SOD-123",XU,Y1-7.62,0)
s.wire(vin,(vin[0],Y1-7.62),d(1)); s.wire(d(2),(177.8,Y1-7.62),(177.8,Y1))
s.wire(u(2),(177.8,Y1)); rail_out(Y1,(177.8,Y1),(185.42,195.58,208.28,218.44,228.6,233.68,238.76))
adj=u(1)
r2=R("R902","2k2","SX-R-049",XU,adj[1]+3.81); gnd(r2(2))
ca=CP("C903","10u 25V","SX-C-012",CP10,175.26,adj[1]+3.81); gnd(ca(2))
r1=R("R901","200","SX-R-010",185.42,Y1+3.81)
d2=D("D902","1N4148W","SX-D-003","Diode_SMD:D_SOD-123",195.58,Y1+3.81,270)
x=adj
for xx in (175.26,185.42,195.58): s.wire(x,(xx,adj[1])); x=(xx,adj[1])
co=CP("C904","10u 25V","SX-C-012",CP10,208.28,Y1+3.81); gnd(co(2))
cc=C("C905","100n","SX-C-002",218.44,Y1+3.81); gnd(cc(2))
ds=D("D905","SS14","SX-D-007","Diode_SMD:D_SMA",228.6,Y1+3.81,270); gnd(ds(2))
s.tp("TP903","+15V",(233.68,Y1),"up"); s.power("+15V",(238.76,Y1))

Y2=236.22
u=s.place("Regulator_Linear","LM337_TO220","U902","LM337",XU,Y2,0,fp=TO220,props=P("SX-IC-011",Manufacturer="Texas Instruments",MPN="LM337"))
vin=rail_in(Y2,"-20V_RAW","TP902","down","C906","C907",True); s.wire(vin,u(2))
d=D("D903","1N4148W","SX-D-003","Diode_SMD:D_SOD-123",XU,Y2+7.62,180)
s.wire(vin,(vin[0],Y2+7.62),d(2)); s.wire(d(1),(177.8,Y2+7.62),(177.8,Y2))
s.wire(u(3),(177.8,Y2)); rail_out(Y2,(177.8,Y2),(185.42,195.58,208.28,218.44,228.6,233.68,238.76))
adj=u(1)
r4=R("R904","2k2","SX-R-049",XU,adj[1]-3.81); gnd(r4(1),180)
ca=CP("C908","10u 25V","SX-C-012",CP10,175.26,adj[1]-3.81); gnd(ca(1),180)
r3=R("R903","200","SX-R-010",185.42,Y2-3.81)
d4=D("D904","1N4148W","SX-D-003","Diode_SMD:D_SOD-123",195.58,Y2-3.81,270)
x=adj
for xx in (175.26,185.42,195.58): s.wire(x,(xx,adj[1])); x=(xx,adj[1])
co=CP("C909","10u 25V","SX-C-012",CP10,208.28,Y2-3.81); gnd(co(1),180)
cc=C("C910","100n","SX-C-002",218.44,Y2+3.81); gnd(cc(2))
ds=D("D906","SS14","SX-D-007","Diode_SMD:D_SMA",228.6,Y2-3.81,270); gnd(ds(1),180)
s.tp("TP904","-15V",(233.68,Y2),"down"); s.power("-15V",(238.76,Y2))

# ------------------------------------------------------------- +5 V (L7805, TO-220) for logic and LEDs
Y3=279.4
u=s.place("Regulator_Linear","L7805","U903","L7805",160.02,Y3,0,fp=TO220,props=P("SX-IC-016",Manufacturer="STMicroelectronics",MPN="L7805CV"))
s.power("+15V",(142.24,Y3)); s.wire((142.24,Y3),(147.32,Y3)); s.wire((147.32,Y3),u(1))
c=C("C911","100n","SX-C-002",147.32,Y3+3.81); pgnd(c(2))
s.wire(u(2),dn(u(2),2.54)); pgnd(dn(u(2),2.54))
x=u(3)
for xx in (175.26,180.34,185.42): s.wire(x,(xx,Y3)); x=(xx,Y3)
c=CP("C912","10u 25V","SX-C-012",CP10,175.26,Y3+3.81); pgnd(c(2))
s.tp("TP905","+5V",(180.34,Y3),"up"); s.power("+5V",(185.42,Y3))
pgnd((200.66,Y3+7.62)); s.tp("TP906","PGND",(200.66,Y3+7.62),"up")

# ------------------------------------------------------------- system star point: AGND meets PGND here only
nt=s.place("Device","NetTie_2","NT901","STAR POINT",76.2,264.16,0,fp="NetTie:NetTie-2_SMD_Pad2.0mm",props=P("none (PCB net tie)",Note="The only AGND-PGND connection in the system (docs/CHAIN.md); place where the power ribbon enters"))
s.wire(nt(1),lt(nt(1),5.08)); gnd(lt(nt(1),5.08)); s.wire(nt(2),rt(nt(2),5.08)); pgnd(rt(nt(2),5.08))
s.power("PWR_FLAG",(55.88,256.54)); s.wire((55.88,256.54),(55.88,261.62)); gnd((55.88,261.62))
# frame bond with ground lift: closed = frame on the star point, open = through 100R || 100n
fr=s.place("Connector_Generic","Conn_01x01","J902","FRAME",40.64,304.8,0,fp="MountingHole:MountingHole_3.2mm_M3_Pad",props=P("none (PCB mounting hole)",Note="Frame bond screw to the metal frame rail"))
ch=rt(fr(1),7.62); s.wire(fr(1),ch)
for xx in (58.42,73.66,88.9): s.wire(ch,(xx,ch[1])); ch=(xx,ch[1])
sw=s.place("Switch","SW_SPST","SW901","GROUND LIFT",58.42,314.96,270,props=P("SX-SW-002",Note="Panel switch on the master rear panel; part to choose"))
rl=s.place("Device","R","R905","100",73.66,314.96,0,fp=R0805,props=P("SX-R-001"))
cl=s.place("Device","C","C913","100n 100V",88.9,314.96,0,fp=C0805,props=P("SX-C-013"))
for p1,p2 in ((sw(1),sw(2)),(rl(1),rl(2)),(cl(1),cl(2))):
    s.wire((p1[0],304.8),p1); s.wire(p2,dn(p2,2.54)); gnd(dn(p2,2.54))

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'power.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_power_wired.json','w'))
json.dump({"no_connect":[]},open(T+'power_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols")
