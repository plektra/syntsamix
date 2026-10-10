# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""AUX return sheets, drawn with real wires (one script, two identical sheets).

Reference netlists: aux_return_build.py (check_netlist.py aux_return1.json / aux_return2.json).
Top: jacks, RFI filters, TL072 difference receiver (decision 148), gain stage with the PRO/PEDAL jumper,
SSI2162 VCA with I-V stage and inverter, bus resistors and the MAIN/COMP switch.
Bottom: level law (as the channel fader), mute/duck switch, buttons, supplies.
"""
SMD={"SX-C-023":dict(Manufacturer="Panasonic",MPN="EEE-1VA100NP",Supplier="Mouser",SupplierPN="667-EEE-1VA100NP"),
     "SX-C-024":dict(Manufacturer="ROQANG",MPN="RVT1V100M0505",Supplier="LCSC",SupplierPN="C72486"),
     "SX-C-025":dict(Manufacturer="ROQANG",MPN="RVT1V470M0605",Supplier="LCSC",SupplierPN="C72522")}   # decision 111 parts, 5.4 mm tall
import json,os,sys
from schlayout import Sheet,pins_of
R0805="Resistor_SMD:R_0805_2012Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"
CBIP="Capacitor_SMD:C_Elec_6.3x5.4"; SO8="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"; SO16="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm"
TI={"Manufacturer":"Texas Instruments"}; VI={"Manufacturer":"Vishay"}
ST072={"Manufacturer":"STMicroelectronics","MPN":"TL072CDT","Supplier":"LCSC","SupplierPN":"C6961"}   # SX-IC-007 fee-free (decision 137)
SWFP="syntsamix:SW_Latching_8.5x8.5mm_CW_GPBS850N"
def draw(n):
    B=100*n+100
    s=Sheet(); NC=[]
    P=lambda pn,**k: {"ProjectPN":pn,**k}
    rr=lambda k:f"R{B+k}"; cc=lambda k:f"C{B+k}"; uu=lambda k:f"U{B+k}"; tt=lambda k,unit:f"U9{B+k}{unit}"
    def R(k,val,pn,x,y,rot=90,**kw): return s.place("Device","R",rr(k),val,x,y,rot,fp=R0805,props=P(pn,**kw))
    def C(k,val,pn,x,y,rot=90,fp=C0805): return s.place("Device","C",cc(k),val,x,y,rot,fp=fp,props=P(pn,**SMD.get(pn,{})))
    SYM={"OPA2171":"Opamp_Dual"}; MPN={"OPA2171":{"MPN":"OPA2171AIDR"}}   # no OPA2171 symbol in the KiCad library; same pinout
    def OA(part,ref,unit,x,y,pn): return s.place("Amplifier_Operational",SYM.get(part,part),ref,part,x,y,0,unit,SO8,P(pn,**(ST072 if part=="TL072" else {**TI,**MPN.get(part,{})})))
    def DG(ref,unit,x,y): return s.place("Analog_Switch","DG413xY",ref,"DG413DY",x,y,0,unit,SO16,P("SX-IC-005",**VI,Assembly="hand (decision 150)",))
    gnd=lambda at,rot=0: s.power("GNDA",at,rot)
    up=lambda p,d=2.54:(p[0],p[1]-d); dn=lambda p,d=2.54:(p[0],p[1]+d); lt=lambda p,d=2.54:(p[0]-d,p[1]); rt=lambda p,d=2.54:(p[0]+d,p[1])
    # ------------------------------------------------ jacks (labels to the RFI filters)
    JK=dict(fp="syntsamix:Jack_6.35mm_Rean_NYS216_Horizontal")
    j1=s.place("Connector_Audio","AudioJack3_Switch",f"J{B+1}",f"RETURN {n} L/MONO",30.48,50.8,0,props=P("SX-CONN-015",Manufacturer="Rean",MPN="NYS216"),**JK)
    j2=s.place("Connector_Audio","AudioJack3_Switch",f"J{B+2}",f"RETURN {n} R",30.48,76.2,0,props=P("SX-CONN-015",Manufacturer="Rean",MPN="NYS216"),**JK)
    for jj,pins in ((j1,(("T","IN_L+"),("R","IN_L-"),("S",None))),(j2,(("T","IN_R+"),("R","IN_R-"),("S",None),("TN","IN_L+"),("RN","IN_L-")))):
        for pin,net in pins:
            e=rt(jj(pin),5.08); s.wire(jj(pin),e)
            if net: s.label(net,e,0)
            else: gnd(e,90)
    NC+=[j1("TN"),j1("RN"),j1("SN"),j2("SN")]
    # ------------------------------------------------ receiver
    # receiver: TL072 difference amplifier, G = 1/2, as the channel (decision 148, after decision 143).
    # R1-R4 (10k 0.1 %, with the 220p RFI caps) are the first half of each 20k input leg; IN+ drives the
    # inverting leg as the AD8273 was wired (-INA, +INA), so the receiver still inverts.
    RX=dict(Manufacturer="YAGEO",MPN="RT0805BRD0710KL",Supplier="LCSC",SupplierPN="C110775",Note="0.1 %: receiver resistor match sets the CMRR (decision 148)")
    def receiver(ych,legs,ref,unit,pins):
        (rp_,cp_,lp,ri,rf),(rn_,cn_,ln,rni,rg)=legs
        a=OA("TL072",ref,unit,109.22,ych,"SX-IC-007"); pp,pm,po=pins
        A,Bv,F=ych-12.7,ych+10.16,ych+20.32
        # non-inverting leg on row A, R to ground above the + node column
        s.label(ln,(48.26,A),180); r=R(rn_,"10k","SX-R-107",60.96,A,**RX); s.wire((48.26,A),r(1)); nd=(71.12,A); s.wire(r(2),nd)
        c=C(cn_,"220p C0G","SX-C-001",nd[0],A+3.81,0); s.wire(nd,c(1)); gnd(c(2))
        r2=R(rni,"10k","SX-R-107",83.82,A,**RX); s.wire(nd,r2(1)); s.wire(r2(2),(93.98,A),(93.98,a(pp)[1]),a(pp))
        g=R(rg,"10k","SX-R-107",93.98,A-3.81,0,**RX); s.wire((93.98,A),g(2)); t=up(g(1),2.54); s.wire(g(1),t,rt(t,5.08)); gnd(rt(t,5.08))
        # inverting leg on row B, feedback on row F
        s.label(lp,(48.26,Bv),180); r=R(rp_,"10k","SX-R-107",60.96,Bv,**RX); s.wire((48.26,Bv),r(1)); nd=(71.12,Bv); s.wire(r(2),nd)
        c=C(cp_,"220p C0G","SX-C-001",nd[0],Bv+3.81,0); s.wire(nd,c(1)); gnd(c(2))
        r2=R(ri,"10k","SX-R-107",83.82,Bv,**RX); s.wire(nd,r2(1)); s.wire(r2(2),(91.44,Bv))
        s.wire((91.44,Bv),(91.44,a(pm)[1]),a(pm)); s.wire((91.44,Bv),(91.44,F))
        f=R(rf,"10k","SX-R-107",104.14,F,**RX); s.wire((91.44,F),f(1)); s.wire(f(2),(a(po)[0],F),a(po))
        return a(po)
    RXO={"L":receiver(119.38,((1,1,"IN_L+",45,46),(2,2,"IN_L-",47,48)),uu(1),1,(3,2,1)),
         "R":receiver(195.58,((3,3,"IN_R+",49,50),(4,4,"IN_R-",51,52)),tt(1,2),2,(5,6,7))}
    # ------------------------------------------------ per side: gain stage, VCA input, I-V, inverter, bus switch
    XV,YV=325.12,121.92
    v=s.place("syntsamix","SSI2162",uu(3),"SSI2162",XV,YV,0,fp="Package_SO:SSOP-10_3.9x4.9mm_P1.00mm",props=P("SX-IC-002",Assembly="hand (decision 150)",Manufacturer="Sound Semiconductor",MPN="SSI2162SS-TU",Supplier="Electrokit",SupplierPN="41019302"))
    s.wire(v("10"),up(v("10"),5.08)); s.power("+15V",up(v("10"),5.08)); s.wire(v("6"),dn(v("6"),5.08)); s.power("-15V",dn(v("6"),5.08))
    s.wire(v("5"),dn(v("5"),5.08),rt(dn(v("5"),5.08),5.08)); gnd(rt(dn(v("5"),5.08),5.08))
    vcp=dn(v("3"),7.62); s.wire(v("3"),vcp); s.wire(v("8"),dn(v("8"),7.62)); s.wire(vcp,dn(v("8"),7.62)); s.wire(vcp,lt(vcp,5.08)); s.label("VC",lt(vcp,5.08),180)
    m=up(v("1"),7.62); s.wire(v("1"),m,lt(m,7.62)); r21=R(21,"14k3","SX-R-030",m[0]-7.62,m[1]-3.81,0,Note="DNP = Class AB (default); fit for Class A")
    s.wire(r21(1),up(r21(1),2.54)); s.power("+15V",up(r21(1),2.54))
    s.tp(f"TP{B+3}","VC",lt(vcp,2.54),"down")
    sides=(("L",0,(5,5,7,9,7,9,11,13,11,15,13,17,19,34),(uu(2),1,(2,3,1)),(uu(4),1,(2,3,1)),(uu(5),1,(2,3,1)),v("2"),v("4"),True,
            ((tt(9,4),4,15,14,16,"MAIN_L"),(uu(9),1,2,3,1,"COMP_L"))),
           ("R",76.2,(6,6,8,10,8,10,12,14,12,16,14,18,20,35),(tt(2,2),2,(6,5,7)),(tt(4,2),2,(6,5,7)),(tt(5,2),2,(6,5,7)),v("9"),v("7"),False,
            ((tt(9,3),3,10,11,9,"MAIN_R"),(tt(9,2),2,6,7,8,"COMP_R"))))
    for side,dy,(ccpl,rin,rf,rs,cf,cvin,rvin,rrc,crc,rfb,cfb,rinv,rinvf,rbus),gain,iv,inv,iin,iout,rc_up,dgs in sides:
        y=119.38+dy
        o=RXO[side]; xo=119.38
        s.wire(o,(xo,o[1]))
        if abs(o[1]-y)>0.01: s.wire((xo,o[1]),(xo,y))
        c=C(ccpl,"10u bipolar","SX-C-023",127.0,y,fp=CBIP); s.wire((xo,y),c(1))
        r=R(rin,"10k","SX-R-002",140.97,y); s.wire(c(2),r(1))
        SX,TX=152.4,180.34
        s.wire(r(2),(SX,y))
        a=OA("NE5532",gain[0],gain[1],167.64,y-2.54,"SX-IC-004"); pm,pp,po=gain[2]
        s.wire((SX,y),a(pm)); s.wire(a(pp),lt(a(pp)),up(lt(a(pp)))); gnd(up(lt(a(pp))),180)
        tn=(TX,y-2.54); s.wire(a(po),tn)
        yc,yr=y+7.62,y+17.78
        for y1,y2 in ((y,yc),(yc,yr)): s.wire((SX,y1),(SX,y2))
        for y1,y2 in ((tn[1],yc),(yc,yr),(yr,yr+7.62)): s.wire((TX,y1),(TX,y2))
        cfx=C(cf,"22p C0G","SX-C-004",166.37,yc); s.wire((SX,yc),cfx(1)); s.wire(cfx(2),(TX,yc))
        r1=R(rf,"10k","SX-R-002",157.48,yr); s.wire((SX,yr),r1(1))
        mid=(165.1,yr); s.wire(r1(2),mid)
        r2=R(rs,"30k","SX-R-050",172.72,yr); s.wire(mid,r2(1)); s.wire(r2(2),(TX,yr))
        if side=="L":
            jp=s.place("Connector_Generic","Conn_02x02_Odd_Even",f"J{B+3}","GAIN: fitted -6 dB (PRO), open +6 dB (PEDAL)",170.18,yr+7.62,0,
                       fp="Connector_PinHeader_2.54mm:PinHeader_2x02_P2.54mm_Vertical",props=P("SX-CONN-004",Note="Default: both fitted (-6 dB)"))
            s.wire(mid,jp(1)); s.wire(jp(2),(TX,yr+7.62))
            s.wire(jp(3),(160.02,jp(3)[1])); s.label("R_MID",(160.02,jp(3)[1]),180)
            s.wire(jp(4),(185.42,jp(4)[1])); s.label("R_RET",(185.42,jp(4)[1]),0)
        else:
            s.wire(mid,dn(mid,7.62)); s.label("R_MID",dn(mid,7.62),270)
            s.wire((TX,yr+7.62),(TX,yr+10.16)); s.label("R_RET",(TX,yr+10.16),270)
        s.tp(f"TP{B+1 if side=='L' else B+2}",f"{side}_RET",(185.42,tn[1]),"up")
        # VCA input
        cv=C(cvin,"10u bipolar","SX-C-023",195.58,tn[1],fp=CBIP); s.wire(tn,(185.42,tn[1])); s.wire((185.42,tn[1]),cv(1))
        rv=R(rvin,"10k","SX-R-002",213.36,tn[1]); s.wire(cv(2),rv(1))
        node=(228.6,tn[1]); s.wire(rv(2),node)
        sgn=-1 if rc_up else 1
        rn=R(rrc,"100","SX-R-001",node[0],tn[1]+sgn*11.43,0); cn=C(crc,"2n2 C0G","SX-C-009",node[0],tn[1]+sgn*26.67,0)
        if rc_up: s.wire(node,rn(2)); s.wire(rn(1),cn(2)); gnd(cn(1),180)
        else: s.wire(node,rn(1)); s.wire(rn(2),cn(1)); gnd(cn(2))
        if abs(iin[1]-tn[1])<0.01: s.wire(node,iin)
        else: s.wire(node,(iin[0]-5.08,tn[1]),(iin[0]-5.08,iin[1]),iin)
        # I-V converter
        yv=tn[1]; X1=355.6
        b=OA("NE5532",iv[0],iv[1],X1,yv-2.54,"SX-IC-004"); pm,pp,po=iv[2]
        if abs(iout[1]-yv)<0.01: s.wire(iout,b(pm))
        else: s.wire(iout,(iout[0]+2.54,iout[1]),(iout[0]+2.54,yv),b(pm))
        s.wire(b(pp),lt(b(pp)),up(lt(b(pp)))); gnd(up(lt(b(pp))),180)
        nf=(X1-10.16,yv); out=(X1+10.16,yv-2.54); s.wire(b(po),out)
        f1=R(rfb,"10k","SX-R-002",X1,yv+10.16); f2=C(cfb,"100p C0G","SX-C-008",X1,yv+20.32)
        s.wire(nf,(nf[0],yv+10.16)); s.wire((nf[0],yv+10.16),(nf[0],yv+20.32)); s.wire((nf[0],yv+10.16),f1(1)); s.wire((nf[0],yv+20.32),f2(1))
        s.wire(f1(2),(out[0],yv+10.16)); s.wire(f2(2),(out[0],yv+20.32)); s.wire((out[0],yv+20.32),(out[0],yv+10.16)); s.wire((out[0],yv+10.16),out)
        # inverter
        X2=396.24; yi=yv-2.54
        ri=R(rinv,"10k","SX-R-002",378.46,yi); s.wire(out,ri(1))
        c2=OA("NE5532",inv[0],inv[1],X2,yi-2.54,"SX-IC-004"); pm,pp,po=inv[2]
        n2=(X2-10.16,yi); s.wire(ri(2),n2,c2(pm)); s.wire(c2(pp),lt(c2(pp)),up(lt(c2(pp)))); gnd(up(lt(c2(pp))),180)
        o2=(X2+10.16,yi-2.54); s.wire(c2(po),o2)
        rf2=R(rinvf,"10k","SX-R-002",X2,yi+10.16); s.wire(n2,(n2[0],yi+10.16),rf2(1)); s.wire(rf2(2),(o2[0],yi+10.16),o2)
        # bus resistor and MAIN/COMP switch
        rb=R(rbus,"22k","SX-R-047",419.1,o2[1]); s.wire(o2,rb(1))
        bn=(429.26,o2[1]); s.wire(rb(2),bn)
        for k,(ref,unit,pl,pr,pc,bus) in enumerate(dgs):
            yy=o2[1]+k*20.32
            d=DG(ref,unit,444.5,yy)
            if k: s.wire(bn,(bn[0],yy))
            s.wire((bn[0],yy),d(pl)); s.wire(d(pr),(462.28,yy)); s.label(bus,(462.28,yy),0,"hierarchical","bidirectional")
            s.wire(d(pc),dn(d(pc),2.54)); s.label("COMP_CTRL",dn(d(pc),2.54),270)
    # ------------------------------------------------ level law (as the channel fader, decision 72)
    Y=300.0; VBX=96.52; SUMX=241.3
    fv=s.place("Device","R_Potentiometer",f"RV{B+1}",f"RETURN {n} LEVEL 10k lin",45.72,Y,0,fp="Potentiometer_THT:Potentiometer_Alpha_RD901F-40-00D_Single_Vertical",
               props=P("SX-POT-006",Note="Pin 1 = fully counter-clockwise (off)"))
    s.wire(fv(1),up(fv(1),5.08)); s.power("-15V",up(fv(1),5.08),180); s.wire(fv(3),dn(fv(3),5.08)); gnd(dn(fv(3),5.08))
    # U+6 = OPA2171: input range includes V- (the wiper reaches -15 V), no phase reversal (TI SBOS516H).
    # Its inputs have back-to-back diodes, so the superdiodes (open loop when off) stay on the TL072 U+7 (decision 102)
    bu=OA("OPA2171",uu(6),1,68.58,Y+2.54,"SX-IC-021"); s.wire(fv(2),bu(3))
    bo=(78.74,Y+2.54); s.wire(bu(1),bo,(VBX,Y+2.54)); s.wire(bo,(78.74,Y+10.16),(58.42,Y+10.16),(58.42,bu(2)[1]),bu(2))
    # E24 pairs as the channel's level law (decision 140): 113k = 100k + 13k, 450k = 300k + 150k
    ra=R(22,"100k","SX-R-007",165.1,Y-20.32); ra2=R(42,"13k","SX-R-011",180.34,Y-20.32)
    s.wire((VBX,Y-20.32),ra(1)); s.wire(ra(2),ra2(1)); s.wire(ra2(2),(SUMX,Y-20.32))
    rc=R(23,"300k","SX-R-096",165.1,Y-10.16); rc2=R(43,"150k","SX-R-098",180.34,Y-10.16)
    s.wire((152.4,Y-10.16),rc(1)); s.power("+15V",(152.4,Y-10.16)); s.wire(rc(2),rc2(1)); s.wire(rc2(2),(SUMX,Y-10.16))
    def superdiode(y,rp,rq,rqval,rqpn,opa,unit,pins,d,rs,rsval,rspn,rq2=None):
        a=R(rp,"100k","SX-R-007",106.68,y); s.wire((VBX,y),a(1)); nd=(114.3,y); s.wire(a(2),nd)
        q=R(rq,rqval,rqpn,114.3,y-10.16,0); s.wire(nd,q(2))
        if rq2:   # second part of an E24 pair above the first
            q2=R(rq2[0],rq2[1],rq2[2],114.3,y-20.32,0); s.wire(q(1),q2(2)); q=q2
        s.wire(q(1),up(q(1),1.27)); s.power("+15V",up(q(1),1.27))
        o=OA("TL072",opa,unit,129.54,y+2.54,"SX-IC-007"); s.wire(nd,o(pins[0]))
        dd=s.place("Device","D",d,"1N4148W",144.78,y+2.54,0,fp="Diode_SMD:D_SOD-123",props=P("SX-D-003"))
        s.wire(o(pins[2]),dd(1)); k=(152.4,y+2.54); s.wire(dd(2),k)
        s.wire(k,(k[0],y+10.16),(119.38,y+10.16),(119.38,o(pins[1])[1]),o(pins[1]))
        r=R(rs,rsval,rspn,200.66,y+2.54); s.wire(k,r(1)); s.wire(r(2),(SUMX,y+2.54))
    superdiode(Y+17.78,24,25,"220k","SX-R-103",tt(7,2),2,(5,6,7),f"D{B+1}",26,"62k","SX-R-102")
    superdiode(Y+50.8,27,28,"100k","SX-R-007",uu(7),1,(3,2,1),f"D{B+2}",29,"9k1","SX-R-095",(44,"24k","SX-R-031"))   # 124k = 100k + 24k
    for y1,y2 in ((Y-20.32,Y+2.54),(Y+2.54,Y+17.78),(Y+17.78,Y+50.8)): s.wire((VBX,y1),(VBX,y2))
    rd=R(32,"30k","SX-R-050",220.98,Y+30.48,Note="SC_ENV into the virtual earth: 0.333 V/V, 10 dB of ducking per -1 V (decisions 97, 153)")
    s.wire((208.28,Y+30.48),rd(1)); s.label("DUCK_V",(208.28,Y+30.48),180); s.wire(rd(2),(SUMX,Y+30.48))
    rm=R(31,"33k","SX-R-006",220.98,Y+40.64); s.wire((208.28,Y+40.64),rm(1)); s.label("MUTE_V",(208.28,Y+40.64),180); s.wire(rm(2),(SUMX,Y+40.64))
    taps=sorted({Y-38.1,Y-30.48,Y-20.32,Y-10.16,Y+5.08,Y+20.32,Y+30.48,Y+40.64,Y+53.34})
    for y1,y2 in zip(taps,taps[1:]): s.wire((SUMX,y1),(SUMX,y2))
    su=OA("OPA2171",tt(6,2),2,256.54,Y+2.54,"SX-IC-021"); s.wire((SUMX,Y+5.08),su(6))
    s.wire(su(5),lt(su(5),2.54),up(lt(su(5),2.54),2.54)); gnd(up(lt(su(5),2.54),2.54),180)   # + input on AGND (decision 97)
    so=(266.7,Y+2.54); s.wire(su(7),so,(279.4,so[1])); s.label("VC",(279.4,so[1]),0)
    f1=R(30,"10k","SX-R-002",254.0,Y-30.48); f2=C(15,"1u","SX-C-010",254.0,Y-38.1)
    s.wire((SUMX,Y-30.48),f1(1)); s.wire((SUMX,Y-38.1),f2(1)); s.wire(f1(2),(so[0],Y-30.48)); s.wire(f2(2),(so[0],Y-38.1))
    s.wire((so[0],Y-38.1),(so[0],Y-30.48)); s.wire((so[0],Y-30.48),so)
    # ------------------------------------------------ mute and duck (DG413)
    DGX=330.2
    d1=DG(uu(8),1,DGX,Y-20.32)
    s.wire(d1(2),lt(d1(2),7.62)); s.label("DUCK_V",lt(d1(2),7.62),180)
    s.wire(d1(3),(350.52,d1(3)[1])); s.label("SC_ENV",(350.52,d1(3)[1]),0,"hierarchical","input")
    s.wire(d1(1),dn(d1(1),5.08)); s.label("DUCK_CTRL",dn(d1(1),5.08),270)
    d4=DG(tt(8,2),2,DGX,Y+15.24)
    s.wire(d4(6),lt(d4(6),5.08)); s.power("-15V",lt(d4(6),5.08)); s.wire(d4(7),(345.44,d4(7)[1])); s.label("MUTE_V",(345.44,d4(7)[1]),0)
    s.wire(d4(8),dn(d4(8),5.08)); s.label("MUTE_CTRL",dn(d4(8),5.08),270)
    for ref,unit,yy in ((tt(8,3),3,Y+40.64),(tt(8,4),4,Y+66.04)):
        dx=DG(ref,unit,DGX,yy)
        for q,(px,py,ang) in pins_of("Analog_Switch","DG413xY",unit).items():
            p=dx(q); e={0:lt(p,5.08),180:rt(p,5.08),90:dn(p,5.08)}[int(ang)]; s.wire(p,e); gnd(e)
    # ------------------------------------------------ buttons
    # button LED colours as the channel (decision 117): MUTE red, DUCK and COMP BUS green
    LEDPN={"MUTE":P("SX-D-015",Manufacturer="Foshan NationStar",MPN="NCD0805R1",Supplier="LCSC",SupplierPN="C84256"),"DUCK":P("SX-D-011",Manufacturer="Hubei KENTO",MPN="KT-0805G",Supplier="LCSC",SupplierPN="C2297"),"COMP":P("SX-D-011",Manufacturer="Hubei KENTO",MPN="KT-0805G",Supplier="LCSC",SupplierPN="C2297")}
    def button(name,k,x,y):
        sw,led,rl,rp=f"SW{B+k}",f"D{B+2+k}",35+2*k-1,35+2*k
        b=s.place("Switch","SW_Push_DPDT",sw,f"RETURN {n} {name} (latching)",x,y,0,fp=SWFP,props=P("SX-SW-001",Manufacturer="CW Industries",MPN="GPBS850N",Supplier="Electrokit",SupplierPN="41012905"))
        s.wire(b(2),lt(b(2),5.08)); s.power("+5V",lt(b(2),5.08)); s.wire(b(5),lt(b(5),5.08)); s.power("GNDPWR",lt(b(5),5.08))
        nd=(b(3)[0]+10.16,b(3)[1]); s.wire(b(3),nd,rt(nd,10.16)); s.label(f"{name}_CTRL",rt(nd,10.16),0)
        r=R(rp,"100k","SX-R-007",nd[0],nd[1]-7.62,0); s.wire(nd,r(2))
        g=lt(up(r(1),2.54),5.08); s.wire(r(1),up(r(1),2.54),g); s.power("GNDPWR",g)   # PGND (decision 98); symbol points down beside the resistor
        ld=s.place("Device","LED",led,f"{name} LED",b(6)[0]+22.86,b(6)[1],0,fp="LED_SMD:LED_0805_2012Metric",props=LEDPN[name])
        s.wire(b(6),ld(1)); r2=R(rl,"12k","SX-R-008",ld(2)[0]+8.89,b(6)[1],270); s.wire(ld(2),r2(2)); s.wire(r2(1),rt(r2(1),3.81)); s.power("+15V",rt(r2(1),3.81),270)
        NC.extend([b(1),b(4)])
    button("MUTE",1,421.64,289.56); button("DUCK",2,421.64,320.04); button("COMP",3,421.64,350.52)
    # ------------------------------------------------ supplies and decoupling
    Y2=396.24; x=40.64
    for ref in (tt(2,3),tt(4,3),tt(5,3)):
        p=OA("NE5532",ref,3,x,Y2,"SX-IC-004"); s.wire(p(8),up(p(8),5.08)); s.power("+15V",up(p(8),5.08)); s.wire(p(4),dn(p(4),5.08)); s.power("-15V",dn(p(4),5.08)); x+=15.24
    for ref,part,pn in ((tt(1,3),"TL072","SX-IC-007"),(tt(6,3),"OPA2171","SX-IC-021"),(tt(7,3),"TL072","SX-IC-007")):
        p=OA(part,ref,3,x,Y2,pn); s.wire(p(8),up(p(8),5.08)); s.power("+15V",up(p(8),5.08)); s.wire(p(4),dn(p(4),5.08)); s.power("-15V",dn(p(4),5.08)); x+=15.24
    for ref in (tt(8,5),tt(9,5)):
        p=DG(ref,5,x+5.08,Y2-7.62)
        s.wire(p(13),up(p(13),5.08)); s.power("+15V",up(p(13),5.08)); s.wire(p(12),up(p(12),2.54),rt(up(p(12),2.54),5.08)); s.power("+5V",rt(up(p(12),2.54),5.08))
        s.wire(p(5),dn(p(5),5.08)); gnd(dn(p(5),5.08)); s.wire(p(4),dn(p(4),2.54),rt(dn(p(4),2.54),5.08)); s.power("-15V",rt(dn(p(4),2.54),5.08)); x+=20.32
    x=170.18
    for k in range(9):
        cp=C(16+2*k,"100n","SX-C-002",x,Y2-17.78,0); s.power("+15V",cp(1)); gnd(cp(2))
        cn=C(17+2*k,"100n","SX-C-002",x,Y2+2.54,0); s.wire(cn(1),up(cn(1),2.54)); s.power("-15V",up(cn(1),2.54),180); gnd(cn(2))
        x+=12.7
    return s,NC
HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
for n in (1,2):
    s,NC=draw(n)
    json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+f'aux_return{n}.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+f'calls_aux_return{n}_wired.json','w'))
    json.dump({"no_connect":NC},open(T+f'aux_return{n}_wired_extra.json','w'))
    print(f"return {n}:",len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels")
