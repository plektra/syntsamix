# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Power board input sheet, drawn with real wires.

Reference netlist: input_build.py (check_netlist.py input.json).
Top: brick jack, PTC, TVS, back-to-back P-MOSFETs with the gate network below and the Miller
ramp above, power switch and LED. Bottom: +5 V and the 400 kHz two-phase clock.
"""
import json,os
from schlayout import Sheet
from parts import part
s=Sheet()
def pl(lib,sym,ref,val,key,x,y,rot=0,unit=None,**extra):
    fp,props=part(key,**extra); return s.place(lib,sym,ref,val,x,y,rot,unit=unit,fp=fp,props=props)
def R(ref,val,key,x,y,rot=0): return pl("Device","R",ref,val,key,x,y,rot)
def C(ref,val,key,x,y,rot=0): return pl("Device","C",ref,val,key,x,y,rot)
def pgnd(at,rot=0): s.power("GNDPWR",at,rot)
def chain(y,xs):
    for a,b in zip(xs,xs[1:]): s.wire((a,y),(b,y))

Y=101.6
# ------------------------------------------------------------- brick jack: pins 1, 4 = +24 V, 2, 3 = 0 V (diagonal pairs)
j=pl("Connector_Generic","Conn_01x04","J101","24V IN","KPJX-4S",40.64,Y,180,
     Note="Locking 4-pin power DIN, PCB right angle at the rear edge; mates Mean Well R7B (KPPX-4P). Check polarity on the first brick")
s.wire(j(4),(j(4)[0]+10.16,j(4)[1])); s.label("VBRICK",(j(4)[0]+10.16,j(4)[1]))
s.wire(j(1),(j(1)[0]+2.54,j(1)[1]),(j(1)[0]+2.54,Y+7.62),(j(1)[0]+10.16,Y+7.62)); s.label("VBRICK",(j(1)[0]+10.16,Y+7.62))
for p in (2,3): s.wire(j(p),(j(p)[0]+5.08,j(p)[1]))
x=j(2)[0]+5.08; s.wire((x,j(3)[1]),(x,j(2)[1])); s.wire((x,Y-1.27),(x+7.62,Y-1.27)); pgnd((x+7.62,Y-1.27),270)
s.power("PWR_FLAG",(40.64,Y+17.78)); s.wire((40.64,Y+17.78),(40.64,Y+22.86)); pgnd((40.64,Y+22.86))

# ------------------------------------------------------------- PTC, TVS, reverse block (Q101), soft start (Q102)
s.label("VBRICK",(63.5,Y),180)
f=pl("Device","Polyfuse","F101","4A 30V","PTC 4A",73.66,Y,90); s.wire((63.5,Y),f(1))
tv=pl("Device","D_Zener","D101","SMBJ24A","SMBJ24A",86.36,Y+7.62,270,Note="TVS 24 V standoff, clamps 38.9 V: keeps the inverter IC (VIN + 20 V) under 60 V")
pgnd(tv(2))
c=C("C101","100n 100V","100n 100V",96.52,Y+7.62); pgnd(c(2))
q1=pl("Transistor_FET","SQJ409EP","Q101","SQJ457EP","SQJ457EP",111.76,Y+2.54,90,Note="Reverse-polarity block: drain to the input")
chain(Y,(f(2)[0],86.36,96.52,q1(5)[0])); s.wire((86.36,Y),tv(1)); s.wire((96.52,Y),c(1))
q2=pl("Transistor_FET","SQJ409EP","Q102","SQJ457EP","SQJ457EP",144.78,Y-2.54,270,Note="Soft start: source to the input, Miller ramp about 7 ms; copper pad for heat")
chain(Y,(q1(1)[0],124.46,132.08,q2(1)[0]))
# gate network below the rail
YG=Y+20.32
s.wire(q1(4),(q1(4)[0],YG)); s.label("GATE",(q1(4)[0],YG),180)
r=R("R101","100k","100k",124.46,Y+10.16); s.wire((124.46,Y),r(1)); s.wire(r(2),(124.46,YG))
z=pl("Device","D_Zener","D102","BZT52C12","BZT52C12",132.08,Y+10.16,270); s.wire((132.08,Y),z(1)); s.wire(z(2),(132.08,YG))
r=R("R102","100k","100k",152.4,YG,90)
chain(YG,(q1(4)[0],124.46,132.08,r(1)[0]))
sw=pl("Switch","SW_SPST","SW101","POWER","POWER",167.64,YG,0,Note="Power switch: carries only gate current (about 0.1 mA); part to choose")
s.wire(r(2),sw(1)); s.wire(sw(2),(177.8,YG),(177.8,YG+5.08)); pgnd((177.8,YG+5.08))
# Miller ramp above the rail: gate - 1k - 47n - drain (VIN_SW)
YM=Y-12.7
s.wire(q2(4),(q2(4)[0],YM)); s.wire((q2(4)[0],YM),(q2(4)[0]-5.08,YM)); s.label("GATE",(q2(4)[0]-5.08,YM),180)
r=R("R103","1k","1k",149.86,YM,90); s.wire((q2(4)[0],YM),r(1))
c=C("C102","47n C0G","47n",162.56,YM,90); s.wire(r(2),c(1)); s.wire(c(2),(c(2)[0],Y))
# switched rail: VIN_SW
chain(Y,(q2(5)[0],c(2)[0],180.34,187.96,198.12,210.82,238.76))
s.power("PWR_FLAG",(180.34,Y-5.08)); s.wire((180.34,Y),(180.34,Y-5.08))
s.tp("TP101","VIN_SW",(187.96,Y),"up")
cb=pl("Device","C_Polarized","C103","100u 50V","100u 50V",198.12,Y+7.62); s.wire((198.12,Y),cb(1)); pgnd(cb(2))
r=R("R104","10k","10k",210.82,Y+7.62); s.wire((210.82,Y),r(1))
led=pl("Device","LED","D103","POWER","LED green",218.44,Y+15.24,180,Note="Power LED at the rear edge, about 2 mA")
s.wire(r(2),(210.82,Y+15.24),led(2)); pgnd(led(1))
s.label("VIN_SW",(238.76,Y),0,"hierarchical","output")
s.tp("TP102","PGND",(233.68,Y+25.4),"up"); pgnd((233.68,Y+25.4))

# ------------------------------------------------------------- +5 V for the clock
Y5=170.18
s.label("VIN_SW",(40.64,Y5),180)
u=pl("Regulator_Linear","LM78M05_TO252","U101","L78M05","L78M05",66.04,Y5,0)
c=C("C104","1u","1u",50.8,Y5+5.08); s.wire((40.64,Y5),(50.8,Y5),u(1)); s.wire((50.8,Y5),c(1)); pgnd(c(2))
pgnd(u(2))
c5=C("C105","1u","1u",81.28,Y5+5.08); c6=C("C106","100n","100n",91.44,Y5+5.08)
chain(Y5,(u(3)[0],81.28,91.44,101.6)); s.wire((81.28,Y5),c5(1)); s.wire((91.44,Y5),c6(1)); pgnd(c5(2)); pgnd(c6(2))
up=pl("74xx","74HC14","U91027","74HC14","74HC14",101.6,Y5+20.32,0,unit=7)
s.wire((101.6,Y5),up(14)); pgnd(up(7))

# ------------------------------------------------------------- 400 kHz RC oscillator and two phases
YO=Y5+5.08
u1=pl("74xx","74HC14","U91021","74HC14","74HC14",139.7,YO,0,unit=1)
r=R("R105","4k7","4k7",139.7,YO-7.62,90)
s.wire(u1(1),(u1(1)[0],YO-7.62),r(1)); s.wire(r(2),(u1(2)[0],YO-7.62),u1(2))
c=C("C107","560p C0G","560p",127.0,YO+5.08); s.wire(u1(1),(127.0,YO),c(1)); pgnd(c(2))
u2=pl("74xx","74HC14","U91022","74HC14","74HC14",165.1,YO,0,unit=2); s.wire(u1(2),u2(3))
u3=pl("74xx","74HC14","U91023","74HC14","74HC14",190.5,YO,0,unit=3)
s.wire(u2(4),(177.8,YO),u3(5)); s.wire((177.8,YO),(177.8,YO+12.7),(185.42,YO+12.7),(193.04,YO+12.7))
s.tp("TP104","CLK_B",(185.42,YO+12.7),"down")
s.label("CLK_B",(193.04,YO+12.7),0,"hierarchical","output")
s.wire(u3(6),(205.74,YO),(213.36,YO)); s.tp("TP103","CLK_A",(205.74,YO),"up")
s.label("CLK_A",(213.36,YO),0,"hierarchical","output")
# unused gates: inputs to PGND, outputs open
nc=[]
for k,(unit,pi,po) in enumerate(((4,9,8),(5,11,10),(6,13,12))):
    yy=YO+30.48+k*12.7
    g=pl("74xx","74HC14",f"U9102{unit}","74HC14","74HC14",139.7,yy,0,unit=unit)
    s.wire(g(pi),(g(pi)[0]-5.08,yy),(g(pi)[0]-5.08,yy+2.54)); pgnd((g(pi)[0]-5.08,yy+2.54)); nc.append(list(g(po)))

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'input.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_input_wired.json','w'))
json.dump({"no_connect":nc},open(T+'input_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols")
