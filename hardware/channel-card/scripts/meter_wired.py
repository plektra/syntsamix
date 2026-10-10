# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Meter sheet, drawn with real wires.

Reference netlist: meter_build.py (check_netlist.py meter.json).
Layout: inputs and inverters (left), four superdiode peak detectors into the
hold bus, hold capacitor, decay resistor and buffer (middle), threshold ladder
and the comparator/LED column with the clip segment on top (right), supplies
along the bottom.
"""
import json,os
from schlayout import Sheet
R0805="Resistor_SMD:R_0805_2012Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"
SO8="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"; SO14="Package_SO:SOIC-14_3.9x8.7mm_P1.27mm"
TI={"Manufacturer":"Texas Instruments"}
ST={"Manufacturer":"STMicroelectronics","MPN":"TL072CDT","Supplier":"LCSC","SupplierPN":"C6961"}   # SX-IC-007, JLCPCB basic (decision 137)
s=Sheet()
P=lambda pn,**k: {"ProjectPN":pn,**k}
def R(ref,val,pn,x,y,rot=90,**k): return s.place("Device","R",ref,val,x,y,rot,fp=R0805,props=P(pn,**k))
def C(ref,val,pn,x,y,rot=0): return s.place("Device","C",ref,val,x,y,rot,fp=C0805,props=P(pn))
# U401 (inverters) and U404 (hold follower) are TL062s (power lever 2, 2026-10-09); the superdiodes U402/U403 stay TL072
LOWP=("U401","U94012","U94013","U404","U94042","U94043")
def OA(ref,unit,x,y):
    part,pn=("TL062","SX-IC-024") if ref in LOWP else ("TL072","SX-IC-007")
    return s.place("Amplifier_Operational",part,ref,part,x,y,0,unit,SO8,P(pn,**(ST if pn=="SX-IC-007" else TI)))
def gnd(at,rot=0): s.power("GNDA",at,rot)
def pgnd(at,rot=0): s.power("GNDPWR",at,rot)
def up(p,d=2.54): return (p[0],p[1]-d)
def dn(p,d=2.54): return (p[0],p[1]+d)
def lt(p,d=2.54): return (p[0]-d,p[1])
def rt(p,d=2.54): return (p[0]+d,p[1])

# ------------------------------------------------------------- detectors
XS,HX=101.6,142.24
rows=[]   # (ys of superdiode)
def superdiode(ref,unit,pins,ys,d,r):
    a=OA(ref,unit,XS,ys); pp,pm,po=pins
    dd=s.place("Device","D",d,"1N4148W",115.57,ys,180,fp="Diode_SMD:D_SOD-123",props=P("SX-D-003"))
    s.wire(a(po),dd(2)); x=(121.92,ys); s.wire(dd(1),x)
    rr=R(r,"1k","SX-R-035",130.81,ys); s.wire(x,rr(1)); s.wire(rr(2),(HX,ys))
    s.wire(x,(x[0],ys+7.62),(91.44,ys+7.62),(91.44,a(pm)[1]),a(pm))
    rows.append(ys); return a(pp)
for Pn,base,inv,rin,rfb,sd1,sd2 in (("L",45.72,("U401",1,(3,2,1)),"R401","R402",("U402",1,(3,2,1),"D401","R405"),("U94022",2,(5,6,7),"D402","R406")),
                                    ("R",96.52,("U94012",2,(5,6,7)),"R403","R404",("U403",1,(3,2,1),"D403","R407"),("U94032",2,(5,6,7),"D404","R408"))):
    p1=superdiode(sd1[0],sd1[1],sd1[2],base,sd1[3],sd1[4])
    p2=superdiode(sd2[0],sd2[1],sd2[2],base+25.4,sd2[3],sd2[4])
    yin=p1[1]
    s.label(f"{Pn}_PRE",(25.4,yin),180,"hierarchical","input"); s.wire((25.4,yin),(40.64,yin)); s.wire((40.64,yin),p1)
    # inverter for the negative half-waves
    yv=p2[1]
    ri=R(rin,"10k","SX-R-002",50.8,yv); s.wire((40.64,yin),(40.64,yv),ri(1))
    a=OA(inv[0],inv[1],76.2,yv-2.54); pp,pm,po=inv[2]
    n=(60.96,yv); s.wire(ri(2),n,a(pm))
    s.wire(a(pp),lt(a(pp)),up(lt(a(pp)))); gnd(up(lt(a(pp))),180)
    s.wire(a(po),(86.36,a(po)[1]),(86.36,yv),p2)
    rf=R(rfb,"10k","SX-R-002",72.39,yv+7.62); s.wire(n,(n[0],yv+7.62),rf(1)); s.wire(rf(2),(86.36,yv+7.62),(86.36,yv))
for y1,y2 in zip(sorted(rows),sorted(rows)[1:]): s.wire((HX,y1),(HX,y2))
# hold capacitor, decay resistor, buffer
yh=83.82; s.wire((HX,yh),(152.4,yh)); s.wire((152.4,yh),(160.02,yh)); s.wire((160.02,yh),(167.64,yh))
ch=C("C401","1u","SX-C-010",152.4,yh+3.81); s.wire((152.4,yh),ch(1)); gnd(ch(2))
rd=R("R409","680k","SX-R-036",160.02,yh+3.81,0); s.wire((160.02,yh),rd(1)); gnd(rd(2))
b=OA("U404",1,175.26,yh+2.54); mv=(185.42,b(1)[1]); s.wire(b(1),mv)
s.wire(mv,(mv[0],yh+10.16),(165.1,yh+10.16),(165.1,b(2)[1]),b(2))
s.wire(mv,(187.96,mv[1])); s.label("MV",(187.96,mv[1]),0)
s.tp("TP401","MV",mv,"up")
sp=OA("U94042",2,175.26,yh+30.48)
s.wire(sp(5),lt(sp(5)),up(lt(sp(5)))); gnd(up(lt(sp(5))),180)
s.wire(sp(7),rt(sp(7),2.54),dn(rt(sp(7),2.54),5.08),(sp(6)[0]-2.54,sp(7)[1]+5.08),(sp(6)[0]-2.54,sp(6)[1]),sp(6))

# ------------------------------------------------------------- threshold ladder and comparator/LED column (clip on top)
LX,XC=198.12,223.52
units=[("U405",1,5,4,2),("U94052",2,7,6,1),("U94053",3,11,10,13),("U94054",4,9,8,14),
       ("U406",1,5,4,2),("U94062",2,7,6,1),("U94063",3,11,10,13),("U94064",4,9,8,14)]
vals=["19k1","4k02","2k","1k43","1k54","845","750","237","110"]
pns=["SX-R-037","SX-R-038","SX-R-003","SX-R-039","SX-R-040","SX-R-041","SX-R-042","SX-R-043","SX-R-022"]
names={1:"-30",2:"-20",3:"-10",4:"-5",5:"0",6:"+3",7:"+6",8:"CLIP"}
colour={k:"green" for k in range(1,6)}; colour.update({6:"yellow",7:"yellow",8:"red"})
# 0805 LEDs under the printed bezel (decision 119)
ledpn={"green":P("SX-D-011",Manufacturer="Hubei KENTO",MPN="KT-0805G",Supplier="LCSC",SupplierPN="C2297"),
       "yellow":P("SX-D-016",Manufacturer="Hubei KENTO",MPN="KT-0805Y",Supplier="LCSC",SupplierPN="C2296"),
       "red":P("SX-D-015",Manufacturer="Foshan NationStar",MPN="NCD0805R1",Supplier="LCSC",SupplierPN="C84256")}
taps={}
for k in range(8,0,-1):
    yc=50.8+(8-k)*20.32
    ref,unit,pp,pm,po=units[k-1]
    c=s.place("Comparator","LM339",ref,"LM339",XC,yc,0,unit,SO14,P("SX-IC-009",**TI))
    tap=(LX,c(pp)[1]); taps[k]=tap; s.wire(tap,c(pp))
    s.wire(c(pm),lt(c(pm),5.08)); s.label("MV",lt(c(pm),5.08),180)
    led=s.place("Device","LED",f"D{410+k}",f"{names[k]} {colour[k]}",XC+17.78,yc,0,fp="LED_SMD:LED_0805_2012Metric",props=ledpn[colour[k]])
    s.wire(c(po),led(1))
    rl=R(f"R{418+k}","1k5","SX-R-044",XC+30.48,yc,270); s.wire(led(2),rl(2)); s.wire(rl(1),rt(rl(1),2.54)); s.power("+5V",rt(rl(1),2.54),270)
# ladder resistors between the taps
top=R("R410",vals[0],pns[0],LX,taps[8][1]-10.16,0); s.wire(top(2),taps[8]); s.wire(top(1),up(top(1),2.54)); s.power("+15V",up(top(1),2.54))
for i,k in enumerate(range(8,1,-1),start=1):
    a,bb=taps[k],taps[k-1]
    r=R(f"R{410+i}",vals[i],pns[i],LX,(a[1]+bb[1])/2,0); s.wire(a,r(1)); s.wire(r(2),bb)
bot=R("R418",vals[8],pns[8],LX,taps[1][1]+10.16,0); s.wire(taps[1],bot(1)); gnd(bot(2))

# ------------------------------------------------------------- supplies and decoupling
Y2=246.38; x=50.8
for t in ("U94013","U94023","U94033","U94043"):
    u=OA(t,3,x,Y2); s.wire(u(8),up(u(8),5.08)); s.power("+15V",up(u(8),5.08)); s.wire(u(4),dn(u(4),5.08)); s.power("-15V",dn(u(4),5.08)); x+=17.78
for t in ("U94055","U94065"):
    u=s.place("Comparator","LM339",t,"LM339",x,Y2,0,5,SO14,P("SX-IC-009",**TI))
    s.wire(u(3),up(u(3),5.08)); s.power("+15V",up(u(3),5.08)); s.wire(u(12),dn(u(12),5.08)); pgnd(dn(u(12),5.08)); x+=17.78
x=177.8
for k in (402,404,406,408):
    cp=C(f"C{k}","100n","SX-C-002",x,Y2-7.62); s.power("+15V",cp(1)); gnd(cp(2))
    cn=C(f"C{k+1}","100n","SX-C-002",x,Y2+20.32); s.wire(cn(1),up(cn(1),2.54)); s.power("-15V",up(cn(1),2.54),180); gnd(cn(2))
    x+=12.7
for k in (410,411):
    cp=C(f"C{k}","100n","SX-C-002",x,Y2-7.62); s.power("+15V",cp(1)); pgnd(cp(2)); x+=12.7

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'meter.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_meter_wired.json','w'))
json.dump({"no_connect":[]},open(T+'meter_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols")
