# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Drawing helpers shared by the buck (+20 V) and inverter (-20 V) sheets.

Both sheets draw the TPS54560 with the same left side: input capacitors, EN (UVLO) divider,
COMP network, RT resistor and the 10 pF sync capacitor. On the buck, the IC ground is PGND;
on the inverter it is the -20 V node, so the caller passes the ground function.
"""
from schlayout import Sheet
from parts import part
YV=101.6                 # input rail
XU,YU=152.4,127.0        # TPS54560 centre: VIN (139.7,121.92), EN (139.7,127), COMP (139.7,129.54), RT (139.7,132.08)
class Conv:
    def __init__(c): c.s=Sheet()
    def pl(c,lib,sym,ref,val,key,x,y,rot=0,**extra):
        fp,props=part(key,**extra); return c.s.place(lib,sym,ref,val,x,y,rot,fp=fp,props=props)
    def R(c,ref,val,key,x,y,rot=0): return c.pl("Device","R",ref,val,key,x,y,rot)
    def C(c,ref,val,key,x,y,rot=0): return c.pl("Device","C",ref,val,key,x,y,rot)
    def CP(c,ref,val,key,x,y,rot=0): return c.pl("Device","C_Polarized",ref,val,key,x,y,rot)
    def pgnd(c,at,side="L"): c.s.power("GNDPWR",at,0)
    def chain(c,y,xs):
        for a,b in zip(xs,xs[1:]): c.s.wire((a,y),(b,y))
    def neg(c,at,side="L",d=2.54):
        """IC ground on the inverter: short stub down to a -20V_CONV label, text to the left (L) or right (R)."""
        e=(at[0],at[1]+d); c.s.wire(at,e); c.s.label("-20V_CONV",e,180 if side=="L" else 0)
    def left(c,n,gnd,caps,clk):
        """n: reference number base (200 / 300). gnd(at, side): IC ground. caps: [(value key, value text, ground fn)] on VIN.
        clk: CLK_A / CLK_B. Returns the TPS54560 pin function."""
        s=c.s
        u=c.pl("Regulator_Switching","TPS54560BDDA",f"U{n+1}","TPS54560","TPS54560",XU,YU,0)
        s.label("VIN_SW",(25.4,YV),180,"hierarchical","input")
        xs=[25.4]; k=1
        for i,(key,val,g) in enumerate(caps):
            x=38.1+15.24*i; xs.append(x)
            cc=c.C(f"C{n+k}",val,key,x,YV+7.62); s.wire((x,YV),cc(1)); g(cc(2)); k+=1
        xs+=[101.6,134.62]; c.chain(YV,xs)
        s.wire((134.62,YV),(134.62,u(2)[1]),u(2))
        # EN divider: start 21.1 V, stop 18.7 V (design.py)
        r1=c.R(f"R{n+1}","680k","680k",101.6,107.95); s.wire((101.6,YV),r1(1))
        r2=c.R(f"R{n+2}","39k","39k",101.6,120.65); gnd(r2(2))
        s.wire(r1(2),(101.6,114.3),r2(1)); s.wire((101.6,114.3),(132.08,114.3),(132.08,u(3)[1]),u(3))
        # COMP: series R + C to ground, small C in parallel
        y=u(6)[1]; c.chain(y,(u(6)[0],114.3,106.68))
        rc=c.R(f"R{n+3}",c.rcomp,c.rcomp_key,114.3,134.62); s.wire((114.3,y),rc(1))
        cz=c.C(f"C{n+k}","220n","220n",114.3,146.05); s.wire(rc(2),cz(1)); gnd(cz(2)); k+=1
        cp=c.C(f"C{n+k}",c.cpole,c.cpole_key,106.68,134.62); s.wire((106.68,y),cp(1)); gnd(cp(2)); k+=1
        c.left_fields=[f"C{n+k-1}"]
        # RT to ground, sync clock through 10 pF (SLVSBN0C 7.3.11)
        s.wire(u(4),(137.16,u(4)[1]),(137.16,135.89))
        rt=c.R(f"R{n+4}","240k","240k",137.16,143.51); s.wire((137.16,135.89),rt(1)); gnd(rt(2),"R")
        cs=c.C(f"C{n+k}","10p C0G","10p",130.81,135.89,90); s.wire(cs(2),(137.16,135.89)); k+=1
        s.wire(cs(1),(127.0,135.89),(127.0,154.94)); s.label(clk,(127.0,154.94),270,"hierarchical","input")
        gnd(u(7),"R")
        c.k=k
        return u
