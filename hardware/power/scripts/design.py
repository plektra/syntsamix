# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Power board component values: TPS54560 buck (+20 V) and inverting buck-boost (-20 V), 400 kHz.

Equations from TI SLVSBN0C (TPS54560 datasheet, rev. March 2017) and TI SLVA317B (inverting power
supply from a step-down regulator). Run to print the calculated and chosen values.
Usage: python3 design.py
"""
import math
pi=math.pi
VREF,GMEA,GMPS=0.8,350e-6,17.0          # SLVSBN0C: reference, error amp gm, COMP-to-SW gm
IHYS,I1,VENA=3.4e-6,1.2e-6,1.2         # EN hysteresis current, pull-up, threshold
FSW=400e3
VIN_NOM,VIN_MIN,VIN_MAX=24.0,22.5,24.7  # brick 24 V +-3 %, minus fuse and FET drops at the IC
VO,IO=20.0,2.0                          # each rail, prototype design current
COUT,ESR=330e-6,0.020                   # Panasonic EEHZK1V331P at the converter output
def e(x,unit): return f"{x:.4g} {unit}"
print("== shared")
rt=101756*(FSW/1e3)**-1.008*1e3
print("RT (eq. 8):",e(rt/1e3,"kohm"),"-> 243 kohm;  free-run f =",e(92417/(243**0.991),"kHz"))
# feedback: Vout = 0.8 * (1 + Rhs/Rls)
print("FB 240k/10k ->",e(VREF*(1+240/10),"V"))
# UVLO: start 21 V, stop 18.5 V (converters stay off until the soft-start FET has nearly finished its ramp)
vstart,vstop=21.0,18.5
r1=(vstart-vstop)/IHYS; r2=VENA/((vstart-VENA)/r1+I1)
print("UVLO R1 (eq. 4):",e(r1/1e3,"kohm"),"R2 (eq. 5):",e(r2/1e3,"kohm"),"-> 732k / 42.2k")
R1,R2=732e3,42.2e3
st=VENA+R1*(VENA/R2-I1); sp=st-IHYS*R1   # I1 flows out of EN into R2
print("   chosen: start",e(st,"V"),"stop",e(sp,"V"),"(inverter: stop moot, input sees Vin+|Vo| once running)")
print("   inverter EN at Vin+|Vo| = 44.7 V:",e(44.7*R2/(R1+R2),"V"),"(internal clamp 5.8 V, abs max 8.4 V)")

print("== buck +20 V")
d=VO/VIN_NOM; L=15e-6
print("duty",e(d,""),"ripple",e((VIN_NOM-VO)*d/(L*FSW),"A pp"),"(15 uH)")
vmin=(VO+0.5+IO*0.02)/0.98+IO*0.19   # eq. 43 style: Vf 0.5 V, DCR 20 mohm, Rds(on) max 190 mohm, near-100 % duty with BOOT refresh
print("minimum VIN estimate",e(vmin,"V"),"vs",VIN_MIN)
fp=IO/(2*pi*VO*COUT); fz=1/(2*pi*ESR*COUT)
fco=math.sqrt(math.sqrt(fp*fz)*math.sqrt(fp*FSW/2))
r4=(2*pi*fco*COUT/GMPS)*(VO/(VREF*GMEA))
print("fp(mod)",e(fp,"Hz"),"fz(esr)",e(fz,"Hz"),"fco",e(fco,"Hz"))
print("Rcomp (eq. 48):",e(r4/1e3,"kohm"),"-> 15.8k;  Czero (eq. 49):",e(1/(2*pi*15.8e3*fp)*1e9,"nF"),"-> 220n")
print("Cpole (eq. 50/51):",e(max(1/(pi*15.8e3*FSW),COUT*ESR/15.8e3)*1e12,"pF"),"-> 560p (pole",e(1/(2*pi*15.8e3*560e-12),"Hz)"))

print("== inverter -20 V")
for vin in (VIN_MIN,VIN_NOM):
    d=VO/(vin+VO); il=IO/(1-d); L=22e-6; rip=vin*d/(L*FSW)
    print(f"Vin {vin}: duty {d:.3f}, inductor avg {il:.2f} A, ripple {rip:.2f} App, peak {il+rip/2:.2f} A (limit min 6.3 A)")
R=VO/IO; d=VO/(VIN_MIN+VO)
fz2=R*(1-d)**2/(2*pi*22e-6*d)
dn=VO/(VIN_NOM+VO)
fp1=(1+dn)/(2*pi*R*COUT); kbb=GMPS*R*(1-dn)/(1+dn)
fco=math.sqrt(fp1*fz2)
rc=(fco/(kbb*fp1))*(VO/(VREF*GMEA))
print("fz2 (RHP, min)",e(fz2,"Hz"),"fp1",e(fp1,"Hz"),"Kbb",e(kbb,""),"fco",e(fco,"Hz"))
print("Rcomp (SLVA317 eq. 23):",e(rc/1e3,"kohm"),"-> 27k")
print("Czero (eq. 24, zero at fp1/2):",e(1/(2*pi*27e3*fp1/2)*1e9,"nF"),"-> 220n")
print("Cpole (eq. 25, pole at fz2):",e(1/(2*pi*27e3*fz2)*1e12,"pF"),"-> 100p (pole",e(1/(2*pi*27e3*100e-12),"Hz)"))
print("output cap ripple current",e(IO*math.sqrt(d/(1-d)),"A rms"),"(EEHZK1V331P 2.8 A)")
print("IC VIN-GND max",e(VIN_MAX+VO,"V"),"; with TVS clamp 38.9 V:",e(38.9+VO,"V"),"(abs max 65, operating 60)")

print("== input soft-start (Q102 Miller ramp)")
vplat=3.5; ig=(VIN_NOM-vplat)/100e3-vplat/100e3; c=47e-9
print("gate current",e(ig*1e6,"uA"),"ramp",e(ig/c/1e3,"V/ms"),"->",e(VIN_NOM/(ig/c)*1e3,"ms to 24 V"),"(plateau 3.5 V assumed)")
print("inrush into ~120 uF:",e(120e-6*ig/c,"A"))

print("== clock (74HC14 RC oscillator, 4.7k / 560p)")
for vtp,vtn in ((2.7,1.6),(3.15,1.5),(1.7,0.9)):
    t=4.7e3*560e-12*(math.log((5-vtn)/(5-vtp))+math.log(vtp/vtn))
    print(f"VT+ {vtp} VT- {vtn}: f = {1/t/1e3:.0f} kHz")
