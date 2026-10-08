# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Input sheet, drawn with real wires.

The reference netlist and part fields come from the label-connected sheet that was
verified before this redraw (make_reference.py Input input -> reference/input.json,
reference/input_parts.json); check_netlist.py input.json proves the drawing is identical.
Layout: input header and RFI filters, AD8273 receiver, trim stage with soft clip,
150 Hz low-cut, DG413 low-cut select; L above, R below; trim pot, button and supplies
along the bottom.
"""
import json,os
from schlayout import Sheet,pins_of
HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'; T=os.path.join(HERE,'build')+'/'
PARTS=json.load(open(os.path.join(HERE,'reference','input_parts.json')))
s=Sheet()
def place(ref,x,y,rot=0,unit=None,sym=None):
    p=PARTS[ref]; lib,name=p["lib"].split(':')
    return s.place(lib,name,sym or ref,p["value"],x,y,rot,unit,p["footprint"],dict(p["props"]))
def gnd(at,rot=0): s.power("GNDA",at,rot)
def up(p,d=2.54): return (p[0],p[1]-d)
def dn(p,d=2.54): return (p[0],p[1]+d)
def lt(p,d=2.54): return (p[0]-d,p[1])
def rt(p,d=2.54): return (p[0]+d,p[1])
NOCONNECT=[]

# ------------------------------------------------------------- input header (labels to the RFI filters)
j=place("J1",30.48,127.0,180)
for pin,net in (("1","AGND"),("4","AGND"),("7","AGND"),("10","AGND"),("2","IN_L+"),("3","IN_L-"),("5","IN_R+"),("6","IN_R-")):
    e=rt(j(pin),5.08)
    s.wire(j(pin),e)
    if net=="AGND": gnd(e,90)
    else: s.label(net,e,0)
NOCONNECT+=[j("8"),j("9")]

# ------------------------------------------------------------- receiver
XU,YU=101.6,127.0
u=place("U1",XU,YU)
NOCONNECT+=[u("1"),u("7")]
s.wire(u("11"),up(u("11"),5.08)); s.power("+15V",up(u("11"),5.08))
s.wire(u("4"),dn(u("4"),5.08)); s.power("-15V",dn(u("4"),5.08))
s.wire(u("14"),(116.84,u("14")[1]),(116.84,YU)); s.wire(u("8"),(116.84,u("8")[1]),(116.84,YU)); s.wire((116.84,YU),(121.92,YU)); gnd((121.92,YU))
def rfi(rref,cref,label,row,pin,xr,xn,jog,cap_up=False):
    s.label(label,(48.26,row),180)
    r=place(rref,xr,row,90); s.wire((48.26,row),r(1))
    n=(xn,row); s.wire(r(2),n)
    if cap_up: c=place(cref,xn,row-3.81,180); s.wire(n,c(1)); gnd(c(2),180)
    else: c=place(cref,xn,row+3.81,0); s.wire(n,c(1)); gnd(c(2))
    if jog: s.wire(n,(83.82,row),(83.82,u(pin)[1]),u(pin))
    else: s.wire(n,u(pin))
rfi("R1","C1","IN_L+",109.22,"2",60.96,76.2,True)
rfi("R2","C2","IN_L-",u("3")[1],"3",60.96,71.12,False,True)
rfi("R4","C4","IN_R-",u("5")[1],"5",60.96,71.12,False)
rfi("R3","C3","IN_R+",147.32,"6",60.96,76.2,True)

# ------------------------------------------------------------- trim stage, low-cut, low-cut select (one per side)
def channel(Pn,dy,rx,cpl,rin,trim_unit,c_fb,r_fb,r_z,dz1,dz2,c_a,c_b,r_a,r_b,hp_unit,dg_hp,dg_trim,r_pd):
    y=119.38+dy
    # receiver output: OUT and SENSE tied
    o,se=u(rx[0]),u(rx[1])
    xo=119.38
    if dy==0:
        s.wire(o,(xo,o[1])); s.wire(se,(xo,se[1]),(xo,o[1]))
    else:
        s.wire(se,(xo,se[1])); s.wire(o,(xo,o[1])); s.wire((xo,se[1]),(xo,o[1])); s.wire((xo,o[1]),(xo,y))
    c=place(cpl,127.0,y,90); s.wire((xo,y),c(1))
    r=place(rin,140.97,y,90); s.wire(c(2),r(1))
    SX,TX=152.4,180.34
    s.wire(r(2),(SX,y))
    a=place(trim_unit[0],167.64,y-2.54,0,trim_unit[1],trim_unit[2])
    pm,pp,po=trim_unit[3]
    s.wire((SX,y),a(pm)); s.wire(a(pp),lt(a(pp)),up(lt(a(pp)))); gnd(up(lt(a(pp))),180)
    tn=(TX,y-2.54); s.wire(a(po),tn)
    # feedback: C (row 1), R + trim pot gang (row 2), soft-clip zeners (row 3)
    yc,yr,yz=y+7.62,y+17.78,y+27.94
    for y1,y2 in ((y,yc),(yc,yr),(yr,yz)): s.wire((SX,y1),(SX,y2))
    for y1,y2 in ((tn[1],yc),(yc,yz)): s.wire((TX,y1),(TX,y2))
    cf=place(c_fb,166.37,yc,90); s.wire((SX,yc),cf(1)); s.wire(cf(2),(TX,yc))
    rf=place(r_fb,160.02,yr,90); s.wire((SX,yr),rf(1)); s.wire(rf(2),(167.64,yr)); s.label(f"{Pn}_RV",(167.64,yr),0)
    rz=place(r_z,175.26,yz,270); s.wire((TX,yz),rz(1))
    s.wire((TX,yz),(TX,yz+5.08)); s.label(f"{Pn}_TRIM",(TX,yz+5.08),270)
    d1=place(dz1,165.1,yz,180); s.wire(rz(2),d1(1))
    d2=place(dz2,156.21,yz,0); s.wire(d1(2),d2(2)); s.wire(d2(1),(SX,yz))
    # 150 Hz low-cut (Sallen-Key, unity-gain follower)
    ca=place(c_a,190.5,tn[1],90); s.wire(tn,ca(1))
    ha=(200.66,tn[1]); s.wire(ca(2),ha)
    cb=place(c_b,210.82,tn[1],90); s.wire(ha,cb(1))
    hb=(220.98,tn[1]); s.wire(cb(2),hb)
    rb=place(r_b,hb[0],tn[1]+3.81,0); s.wire(hb,rb(1)); gnd(rb(2))
    f=place(hp_unit[0],236.22,tn[1]+2.54,0,hp_unit[1],hp_unit[2])
    hpp,hpm,hpo=hp_unit[3]
    s.wire(hb,f(hpp))
    hp=(248.92,tn[1]+2.54); s.wire(f(hpo),hp)
    s.wire(hp,(hp[0],tn[1]+10.16),(226.06,tn[1]+10.16),(226.06,f(hpm)[1]),f(hpm))
    ra=place(r_a,224.79,tn[1]-10.16,90); s.wire(ha,(ha[0],tn[1]-10.16),ra(1)); s.wire(ra(2),(hp[0],tn[1]-10.16),hp)
    # low-cut select: pressed = high-passed signal
    XD=271.78; pn=(287.02,hp[1])
    for (ref,unit,rot,pin_in,pin_s,pin_d,ys,src) in ((dg_hp+(hp[1],hp)),(dg_trim+(tn[1]-17.78,None))):
        d=place("U4",XD,ys,rot,unit,ref)
        if src: s.wire(src,d(pin_s))
        else: s.wire(tn,(TX,ys)); s.wire((TX,ys),d(pin_s))
        s.wire(d(pin_d),(pn[0],ys))
        e=up(d(pin_in),2.54) if rot==180 else dn(d(pin_in),2.54)
        s.wire(d(pin_in),e); s.label("LC_CTRL",e,90 if rot==180 else 270)
    s.wire((pn[0],tn[1]-17.78),pn)
    rp=place(r_pd,pn[0],pn[1]+3.81,0); s.wire(pn,rp(1)); gnd(rp(2))
    s.wire(pn,(299.72,pn[1])); s.label(f"{Pn}_PREFILT",(299.72,pn[1]),0,"hierarchical","output")
    k=1 if Pn=="L" else 4
    s.tp(f"TP{k}",f"{Pn}_RX",(xo,y),"up" if dy==0 else "down")
    s.tp(f"TP{k+1}",f"{Pn}_TRIM",(182.88,tn[1]),"up")
    s.tp(f"TP{k+2}",f"{Pn}_PREFILT",(292.1,pn[1]),"up")

# TRIM wire to the DG413 runs up from the trim node: tn -> (TX, ys) is drawn inside channel()
channel("L",0,("13","12"),"C5","R5",("U2",1,"U2",("2","3","1")),"C7","R7","R9","D1","D2","C9","C10","R11","R12",
        ("U3",1,"U3",("3","2","1")),("U4",1,180,"1","3","2"),("U90044",4,180,"16","14","15"),"R15")
channel("R",76.2,("9","10"),"C6","R6",("U2",2,"U90022",("6","5","7")),"C8","R8","R10","D3","D4","C11","C12","R13","R14",
        ("U3",2,"U90032",("5","6","7")),("U90042",2,0,"8","6","7"),("U90043",3,180,"9","11","10"),"R16")

gnd((25.4,180.34)); s.tp("TP7","AGND",(25.4,180.34),"up")

# ------------------------------------------------------------- trim pot (both gangs), labels to the trim stages
rv=place("RV1",76.2,254.0,0)
s.wire(rv("1"),lt(rv("1"),5.08)); s.label("L_RV",lt(rv("1"),5.08),180)
s.wire(rv("2"),up(rv("2"),5.08)); s.label("L_TRIM",up(rv("2"),5.08),90)
s.wire(rv("3"),dn(rv("3"),5.08)); s.label("L_TRIM",dn(rv("3"),5.08),270)
s.wire(rv("4"),dn(rv("4"),5.08)); s.label("R_RV",dn(rv("4"),5.08),270)
s.wire(rv("5"),up(rv("5"),5.08)); s.label("R_TRIM",up(rv("5"),5.08),90)
s.wire(rv("6"),rt(rv("6"),5.08)); s.label("R_TRIM",rt(rv("6"),5.08),0)

# ------------------------------------------------------------- low-cut button
b=place("SW1",127.0,254.0)
s.wire(b("2"),lt(b("2"),5.08)); s.power("+5V",lt(b("2"),5.08))
s.wire(b("5"),lt(b("5"),5.08)); s.power("GNDPWR",lt(b("5"),5.08))
nd=rt(b("3"),5.08); s.wire(b("3"),nd)
rpd=place("R17",nd[0]+7.62,nd[1],90); s.wire(nd,rpd(1)); s.wire(rpd(2),rt(rpd(2),2.54)); s.power("GNDPWR",rt(rpd(2),2.54))   # PGND (decision 98)
s.wire(nd,up(nd,5.08)); s.label("LC_CTRL",up(nd,5.08),90)
ld=place("D5",b("6")[0]+22.86,b("6")[1],0); s.wire(b("6"),ld("1"))
rl=place("R18",ld("2")[0]+8.89,b("6")[1],270); s.wire(ld("2"),rl("2")); s.wire(rl("1"),rt(rl("1"),3.81)); s.power("+15V",rt(rl("1"),3.81),270)
NOCONNECT+=[b("1"),b("4")]

# ------------------------------------------------------------- supplies, decoupling, power flags
x=200.66; Y2=254.0
for t,ref in (("U2","U90023"),("U3","U90033")):
    p=place(t,x,Y2,0,3,ref); s.wire(p("8"),up(p("8"),5.08)); s.power("+15V",up(p("8"),5.08)); s.wire(p("4"),dn(p("4"),5.08)); s.power("-15V",dn(p("4"),5.08)); x+=17.78
p=place("U4",x+5.08,Y2,0,5,"U90045")
s.wire(p("13"),up(p("13"),5.08)); s.power("+15V",up(p("13"),5.08))
s.wire(p("12"),up(p("12"),2.54),rt(up(p("12"),2.54),5.08)); s.power("+5V",rt(up(p("12"),2.54),5.08))
s.wire(p("5"),dn(p("5"),5.08)); gnd(dn(p("5"),5.08))
s.wire(p("4"),dn(p("4"),2.54),rt(dn(p("4"),2.54),5.08)); s.power("-15V",rt(dn(p("4"),2.54),5.08))
x=264.16
for k in range(13,21,2):
    cp=place(f"C{k}",x,Y2-7.62,0); s.power("+15V",cp("1")); gnd(cp("2"))
    cn=place(f"C{k+1}",x,Y2+20.32,0); s.wire(cn("1"),up(cn("1"),2.54)); s.power("-15V",up(cn("1"),2.54),180); gnd(cn("2"))
    x+=12.7
# power flags live on the Chain and power sheet, where the rails enter the card

json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'input.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_input_wired.json','w'))
json.dump({"no_connect":NOCONNECT},open(T+'input_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols")
