# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Power board +20 V buck sheet, drawn with real wires.

Reference netlist: buck_build.py (check_netlist.py buck.json). Left side shared with the
inverter (convlib.py); right side: bootstrap, catch diode, 15 uH, output capacitors, feedback
divider, then the second-stage LC filter to +20V_RAW.
"""
import json,os
from convlib import Conv,YU
c=Conv(); s=c.s
c.rcomp,c.rcomp_key,c.cpole,c.cpole_key="16k","16k","560p C0G","560p"
pg=c.pgnd
u=c.left(200,pg,[("4u7 100V","4u7 100V",pg)]*3+[("100n 100V","100n 100V",pg)],"CLK_A")
# bootstrap, switch node, catch diode, inductor
cb=c.C("C208","100n","100n",175.26,u(1)[1],90); s.wire(u(1),cb(1)); s.wire(cb(2),(179.07,YU))
d=c.pl("Device","D_Schottky","D201","SS54","SS54",184.15,132.08,270); pg(d(2))
l=c.pl("Device","L","L201","15u","15u",196.85,YU,90)
c.chain(YU,(u(8)[0],179.07,184.15,l(1)[0])); s.wire((184.15,YU),d(1))
# converter output and feedback (taken before the LC filter)
co=c.CP("C209","330u 35V","330u 35V",208.28,130.81); pg(co(2))
cc=c.C("C210","4u7 100V","4u7 100V",220.98,130.81); pg(cc(2))
rf1=c.R("R205","240k","240k",233.68,135.89); rf2=c.R("R206","10k","10k",233.68,151.13); pg(rf2(2))
lf=c.pl("Device","L","L202","2u2","2u2",248.92,YU,90)
c.chain(YU,(l(2)[0],208.28,220.98,233.68,243.84,lf(1)[0]))
for x,p in ((208.28,co(1)),(220.98,cc(1)),(233.68,rf1(1))): s.wire((x,YU),p)
s.wire(rf1(2),(233.68,144.78),rf2(1)); s.wire((233.68,144.78),(218.44,144.78),(170.18,144.78),(170.18,u(5)[1]),u(5))
# start-up ramp: 47 nF from the output, D202 into FB; R207 and clamp D203 reset the node (startup_sim.py)
YS=187.96
css=c.C("C214","47n C0G","47n",243.84,177.8); s.wire((243.84,YU),css(1))
dfb=c.pl("Device","D","D202","1N4148W","1N4148W",224.79,YS,0); s.wire((218.44,144.78),(218.44,YS),dfb(1))
dcl=c.pl("Device","D","D203","1N4148W","1N4148W",237.49,196.85,0); s.wire((233.68,YS),dcl(1)); s.wire(dcl(2),(246.38,196.85),(246.38,199.39)); pg((246.38,199.39))
rbl=c.R("R207","1M","1M",256.54,191.77); pg(rbl(2))
s.wire(css(2),(243.84,YS)); c.chain(YS,(dfb(2)[0],233.68,243.84,256.54))
# second-stage LC filter output
f1=c.CP("C211","330u 35V","330u 35V",260.35,130.81); f2=c.CP("C212","100u 35V","100u 35V",273.05,130.81)
f3=c.C("C213","4u7 100V","4u7 100V",285.75,130.81)
for p in (f1,f2,f3): pg(p(2))
c.chain(YU,(lf(2)[0],260.35,273.05,285.75,293.37,300.99))
for x,p in ((260.35,f1(1)),(273.05,f2(1)),(285.75,f3(1))): s.wire((x,YU),p)
s.tp("TP201","+20V_RAW",(293.37,YU),"up")
s.label("+20V_RAW",(300.99,YU),0,"hierarchical","output")

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'buck.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_buck_wired.json','w'))
json.dump({"no_connect":[]},open(T+'buck_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols","left fields",c.left_fields)
