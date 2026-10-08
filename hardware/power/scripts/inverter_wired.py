# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Power board -20 V inverter sheet, drawn with real wires.

Reference netlist: inverter_build.py (check_netlist.py inverter.json). Left side shared with the
buck (convlib.py), with the IC ground as -20V_CONV label stubs. Right side: bootstrap, catch diode
to -20V_CONV, 22 uH to PGND, output capacitors from the -20 V rail up to a PGND bar, feedback
divider below the rail, then the second-stage LC filter to -20V_RAW.
"""
import json,os
from convlib import Conv,YU
c=Conv(); s=c.s
c.rcomp,c.rcomp_key,c.cpole,c.cpole_key="27k","27k","100p C0G","100p"
pg,ng=c.pgnd,c.neg
u=c.left(300,ng,[("4u7 100V","4u7 100V",ng)]*2+[("4u7 100V","4u7 100V",pg),("100n 100V","100n 100V",ng)],"CLK_B")
# bootstrap, switch node, catch diode to -20V_CONV, inductor to PGND
cb=c.C("C308","100n","100n",175.26,u(1)[1],90); s.wire(u(1),cb(1)); s.wire(cb(2),(179.07,YU))
d=c.pl("Device","D_Schottky","D301","SS510C","SS510C",184.15,132.08,270); ng(d(2),"R",5.08)
l=c.pl("Device","L","L301","22u","22u",199.39,130.81,0); pg(l(2))
c.chain(YU,(u(8)[0],179.07,184.15,l(1)[0])); s.wire((184.15,YU),d(1))
# -20 V node: output capacitors up to a PGND bar, feedback divider below the rail
YN,YB=157.48,142.24
s.label("-20V_CONV",(203.2,YN),180)
rf2=c.R("R306","10k","10k",210.82,161.29); rf1=c.R("R305","240k","240k",210.82,171.45); pg(rf1(2))
s.wire(rf2(2),(210.82,167.64),rf1(1)); s.wire((210.82,167.64),(170.18,167.64),(170.18,u(5)[1]),u(5))
co=c.CP("C309","330u 35V","330u 35V",223.52,YN-3.81); cc=c.C("C310","4u7 100V","4u7 100V",236.22,YN-3.81)
lf=c.pl("Device","L","L302","2u2","2u2",264.16,YN,90)
c.chain(YN,(203.2,210.82,223.52,236.22,246.38,251.46,lf(1)[0]))
s.tp("TP302","-20V_CONV",(246.38,YN),"down")
s.power("PWR_FLAG",(251.46,YN-5.08)); s.wire((251.46,YN),(251.46,YN-5.08))
# second-stage LC filter output
f1=c.CP("C311","330u 35V","330u 35V",276.86,YN-3.81); f2=c.CP("C312","100u 35V","100u 35V",289.56,YN-3.81)
f3=c.C("C313","4u7 100V","4u7 100V",302.26,YN-3.81)
c.chain(YN,(lf(2)[0],276.86,289.56,302.26,309.88,317.5))
s.tp("TP301","-20V_RAW",(309.88,YN),"down")
s.label("-20V_RAW",(317.5,YN),0,"hierarchical","output")
# PGND bar over the capacitors
xs=(223.52,236.22,276.86,289.56,302.26,312.42)
for x,p in zip(xs,(co,cc,f1,f2,f3)): s.wire(p(1),(x,YB))
c.chain(YB,xs); s.wire((312.42,YB),(312.42,YB+2.54)); pg((312.42,YB+2.54))

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'inverter.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_inverter_wired.json','w'))
json.dump({"no_connect":[]},open(T+'inverter_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols","left fields",c.left_fields)
