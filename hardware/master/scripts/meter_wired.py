# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Master meter sheet, drawn with real wires.

Reference netlist: meter_build.py (check_netlist.py meter.json).
Left: per side the inverter, two superdiode peak detectors, hold capacitor, decay
resistor and follower (MV_L, MV_R). Middle: the shared threshold ladder and the left
comparator/LED column (clip on top); right: the right column, its thresholds by label.
Supplies along the bottom.
"""
import json,os
from schlayout import Sheet
R0805="Resistor_SMD:R_0805_2012Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"
SO8="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"; SO14="Package_SO:SOIC-14_3.9x8.7mm_P1.27mm"
TI={"Manufacturer":"Texas Instruments"}
s=Sheet()
P=lambda pn,**k: {"ProjectPN":pn,**k}
def R(ref,val,pn,x,y,rot=90,**k): return s.place("Device","R",ref,val,x,y,rot,fp=R0805,props=P(pn,**k))
def C(ref,val,pn,x,y,rot=0): return s.place("Device","C",ref,val,x,y,rot,fp=C0805,props=P(pn))
LOWP={"U802","U98022","U98023","U804","U98042","U98043"}   # TL062 (decision 126): light DC and meter loads
def OA(ref,unit,x,y):
    v="TL062" if ref in LOWP else "TL072"
    return s.place("Amplifier_Operational",v,ref,v,x,y,0,unit,SO8,P("SX-IC-024" if ref in LOWP else "SX-IC-007",**TI,**({"MPN":"TL062CDR","Supplier":"LCSC","SupplierPN":"C67471"} if ref in LOWP else {})))
gnd=lambda at,rot=0: s.power("GNDA",at,rot); pgnd=lambda at,rot=0: s.power("GNDPWR",at,rot)
up=lambda p,d=2.54:(p[0],p[1]-d); dn=lambda p,d=2.54:(p[0],p[1]+d); lt=lambda p,d=2.54:(p[0]-d,p[1]); rt=lambda p,d=2.54:(p[0]+d,p[1])

# ------------------------------------------------------------- detectors
XS,HX=101.6,142.24
def superdiode(ref,unit,pins,ys,d,r):
    a=OA(ref,unit,XS,ys); pp,pm,po=pins
    dd=s.place("Device","D",d,"1N4148W",115.57,ys,180,fp="Diode_SMD:D_SOD-123",props=P("SX-D-003"))
    s.wire(a(po),dd(2)); x=(121.92,ys); s.wire(dd(1),x)
    rr=R(r,"1k","SX-R-035",130.81,ys); s.wire(x,rr(1)); s.wire(rr(2),(HX,ys))
    s.wire(x,(x[0],ys+7.62),(91.44,ys+7.62),(91.44,a(pm)[1]),a(pm))
    return a(pp)
for side,base,sdp,sdn,inv,fol,rin,rfb,rd,ch,tp in (
        ("L",45.72,("U801",1,(3,2,1),"D801","R803"),("U98012",2,(5,6,7),"D802","R804"),("U802",1,(3,2,1)),("U98022",2,(5,6,7)),"R801","R802","R805","C801","TP801"),
        ("R",137.16,("U803",1,(3,2,1),"D803","R808"),("U98032",2,(5,6,7),"D804","R809"),("U804",1,(3,2,1)),("U98042",2,(5,6,7)),"R806","R807","R810","C802","TP802")):
    p1=superdiode(*sdp[:3],base,*sdp[3:])
    p2=superdiode(*sdn[:3],base+25.4,*sdn[3:])
    yin=p1[1]
    s.label(f"MAIN_{side}_OUT",(25.4,yin),180,"hierarchical","input"); s.wire((25.4,yin),(40.64,yin)); s.wire((40.64,yin),p1)
    yv=p2[1]
    ri=R(rin,"10k","SX-R-002",50.8,yv); s.wire((40.64,yin),(40.64,yv),ri(1))
    a=OA(inv[0],inv[1],76.2,yv-2.54); pp,pm,po=inv[2]
    n=(60.96,yv); s.wire(ri(2),n,a(pm))
    s.wire(a(pp),lt(a(pp)),up(lt(a(pp)))); gnd(up(lt(a(pp))),180)
    s.wire(a(po),(86.36,a(po)[1]),(86.36,yv),p2)
    rf=R(rfb,"10k","SX-R-002",72.39,yv+7.62); s.wire(n,(n[0],yv+7.62),rf(1)); s.wire(rf(2),(86.36,yv+7.62),(86.36,yv))
    s.wire((HX,base),(HX,base+25.4))
    yh=base+12.7; s.wire((HX,yh),(152.4,yh)); s.wire((152.4,yh),(160.02,yh)); s.wire((160.02,yh),(167.64,yh))
    c=C(ch,"1u","SX-C-010",152.4,yh+3.81); s.wire((152.4,yh),c(1)); gnd(c(2))
    r=R(rd,"680k","SX-R-036",160.02,yh+3.81,0); s.wire((160.02,yh),r(1)); gnd(r(2))
    b=OA(fol[0],fol[1],175.26,yh+2.54); pp,pm,po=fol[2]; s.wire((167.64,yh),b(pp))
    mv=(185.42,b(po)[1]); s.wire(b(po),mv)
    s.wire(mv,(mv[0],yh+10.16),(165.1,yh+10.16),(165.1,b(pm)[1]),b(pm))
    s.wire(mv,(193.04,mv[1])); s.label(f"MV_{side}",(193.04,mv[1]),0)
    s.tp(tp,f"MV_{side}",mv,"up")

# ------------------------------------------------------------- ladder and comparator/LED columns (clip on top)
UNIT={1:(5,4,2),2:(7,6,1),3:(11,10,13),4:(9,8,14)}
vals=["115k","13k3","31k6","22k6","16k2","11k3","8k06","5k62","5k11","3k83","2k15","1k87","866"]   # R811 (top) ... R823 (bottom)
pns=[f"SX-R-{n:03d}" for n in range(68,81)]
names={1:"-30",2:"-20",3:"-15",4:"-10",5:"-6",6:"-3",7:"0",8:"+3",9:"+6",10:"+9",11:"+12",12:"CLIP"}
colour={k:("green" if k<=7 else "yellow" if k<=10 else "red") for k in range(1,13)}
ledpn={"green":"SX-D-004","yellow":"SX-D-005","red":"SX-D-006"}
LX=231.14
taps={}
for side,XC,chips,d0,r0 in (("L",256.54,("805","806","807"),804,823),("R",360.68,("808","809","810"),816,835)):
    for k in range(12,0,-1):
        yc=40.64+(12-k)*20.32
        chip=chips[(k-1)//4]; unit=(k-1)%4+1; ref=f"U{chip}" if unit==1 else f"U9{chip}{unit}"; pp,pm,po=UNIT[unit]
        c=s.place("Comparator","LM339",ref,"LM339",XC,yc,0,unit,SO14,P("SX-IC-009",**TI))
        if side=="L": tap=(LX,c(pp)[1]); taps[k]=tap; s.wire(tap,c(pp))
        else: s.wire(c(pp),lt(c(pp),7.62)); s.label(f"T{k}",lt(c(pp),7.62),180)
        s.wire(c(pm),lt(c(pm),5.08)); s.label(f"MV_{side}",lt(c(pm),5.08),180)
        led=s.place("Device","LED",f"D{d0+k}",f"{side} {names[k]} {colour[k]}",XC+17.78,yc,0,fp="LED_THT:LED_D3.0mm",props=P(ledpn[colour[k]]))
        s.wire(c(po),led(1))
        rl=R(f"R{r0+k}","1k5","SX-R-044",XC+30.48,yc,270); s.wire(led(2),rl(2)); s.wire(rl(1),rt(rl(1),2.54)); s.power("+5V",rt(rl(1),2.54),270)
for k in range(12,0,-1): s.wire(taps[k],lt(taps[k],5.08)); s.label(f"T{k}",lt(taps[k],5.08),180)
top=R("R811",vals[0],pns[0],LX,taps[12][1]-10.16,0); s.wire(top(2),taps[12]); s.wire(top(1),up(top(1),2.54)); s.power("+15V",up(top(1),2.54))
for i,k in enumerate(range(12,1,-1),start=1):
    a,bb=taps[k],taps[k-1]
    r=R(f"R{811+i}",vals[i],pns[i],LX,(a[1]+bb[1])/2,0); s.wire(a,r(1)); s.wire(r(2),bb)
bot=R("R823",vals[12],pns[12],LX,taps[1][1]+10.16,0); s.wire(taps[1],bot(1)); gnd(bot(2))

# ------------------------------------------------------------- supplies and decoupling
Y2=330.2; x=40.64
for t in ("U98013","U98023","U98033","U98043"):
    u=OA(t,3,x,Y2); s.wire(u(8),up(u(8),5.08)); s.power("+15V",up(u(8),5.08)); s.wire(u(4),dn(u(4),5.08)); s.power("-15V",dn(u(4),5.08)); x+=17.78
for chip in ("805","806","807","808","809","810"):
    u=s.place("Comparator","LM339",f"U9{chip}5","LM339",x,Y2,0,5,SO14,P("SX-IC-009",**TI))
    s.wire(u(3),up(u(3),5.08)); s.power("+15V",up(u(3),5.08)); s.wire(u(12),dn(u(12),5.08)); pgnd(dn(u(12),5.08)); x+=17.78
x+=7.62
for k in (803,805,807,809):
    cp=C(f"C{k}","100n","SX-C-002",x,Y2-7.62); s.power("+15V",cp(1)); gnd(cp(2))
    cn=C(f"C{k+1}","100n","SX-C-002",x,Y2+20.32); s.wire(cn(1),up(cn(1),2.54)); s.power("-15V",up(cn(1),2.54),180); gnd(cn(2))
    x+=12.7
for k in range(811,817):
    cp=C(f"C{k}","100n","SX-C-002",x,Y2-7.62); s.power("+15V",cp(1)); pgnd(cp(2)); x+=12.7

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'meter.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_meter_wired.json','w'))
json.dump({"no_connect":[]},open(T+'meter_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols")
