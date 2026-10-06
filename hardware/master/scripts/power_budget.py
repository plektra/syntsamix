# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Master card supply budget and regulator dissipation (decision 95).

Counts the parts on the ten master sheets and adds their supply currents, typical and
worst case, per rail. Sources: NE5532 TI SLOS075K (6 / 16 mA per package); SSI2162
Rev 1.2 (Class AB 6 / 8 mA); THAT1646 doc 600078 (4.9 / 5.75 mA); TPA6120A2 TI SLOS431B
(about 13 / 15 mA per channel at ±15 V); AD8273 (2.5 mA max per amplifier);
G6K-2F-Y DC12 coil 1315 Ω with 330 Ω in series. TL072 (1.4 / 2.5 mA per amplifier),
LM339 (0.8 / 2.5 mA) and L7805 quiescent (5 / 8 mA) are standard values not re-checked
against the datasheets here.
Also prints the decision 96 sizing figure.
Usage: python3 power_budget.py [raw rail, default 20]
"""
import sys
RAW=float(sys.argv[1]) if len(sys.argv)>1 else 20.0
V15,V5=15.1,5.0
# part: (count, typ mA, max mA, rails) -- rails "pm" = both ±15 V, "p" = +15 V only
parts={
 "NE5532 (bus 6, returns 6, compressor 3, sends 2, master out 1)":(18,6.0,16.0,"pm"),
 "TL072 (returns 4, compressor 5, sidechain 5, master out 2, meter 4)":(20,2.8,5.0,"pm"),
 "SSI2162 (returns 2, compressor 1, master out 1)":(4,6.0,8.0,"pm"),
 "AD8273 (returns)":(2,5.0,5.0,"pm"),
 "THAT1646 (main outputs)":(2,4.9,5.75,"pm"),
 "TPA6120A2 quiescent (two channels)":(1,26.0,30.0,"pm"),
 "LM339 (compressor 2, master out 1, meter 6)":(9,0.8,2.5,"p"),
}
coil=(15.0-0.2)/(1315+330)*1000
fixed_p={"relay coils (3)":(3*coil,3*coil),"button LEDs from +15 V via 12k (10)":(11.0,11.0),
         "dividers, pots, ladders (+15 V)":(2.5,2.5)}
fixed_m={"pots and dividers (-15 V)":(6.0,6.0)}
# +5 V from the L7805, taken from +15 V: meter LEDs 24 x 2 mA, GR LEDs 5 x 2 mA, PFL LED 2 mA
led5_typ,led5_max=24.0,60.0          # typical: about half the meter lit
l7805_iq=(5.0,8.0)
# signal load currents (average per rail): THAT1646 into 600 ohm, headphones
sig_typ={"THAT1646 into 600 ohm (2 x 5 mA)":10.0,"headphones loud, 2 Vrms into 32 ohm":25.0}
sig_max={"THAT1646 into 600 ohm at full level (2 x 10 mA)":20.0,"headphones at full output into 32 ohm":108.0}
def total(k):
    i=1 if k=="max" else 0
    p=sum(n*(t if i==0 else m) for n,t,m,r in parts.values())
    mneg=sum(n*(t if i==0 else m) for n,t,m,r in parts.values() if r=="pm")
    p+=sum(v[i] for v in fixed_p.values()); mneg+=sum(v[i] for v in fixed_m.values())
    i5=(led5_typ if i==0 else led5_max)+l7805_iq[i]
    p+=i5
    s=sum((sig_typ if i==0 else sig_max).values()); p+=s; mneg+=s
    return p,mneg,i5
for k in ("typ","max"):
    p,m,i5=total(k)
    pl317=(RAW-V15)*p/1000; pl337=(RAW-V15)*m/1000; p7805=(V15-V5)*(i5-l7805_iq[k=="max"])/1000+V15*l7805_iq[k=="max"]/1000
    print(f"{k}: +15 V {p:.0f} mA, -15 V {m:.0f} mA, +5 V {i5:.0f} mA | LM317 {pl317:.2f} W, LM337 {pl337:.2f} W, L7805 {p7805:.2f} W (raw {RAW:g} V)")
# heatsink needed for TJ <= 100 C at 40 C ambient (TO-220 junction-to-case about 5 C/W, pad about 1 C/W)
p,m,_=total("max"); pw=(RAW-V15)*max(p,m)/1000
print(f"worst regulator {pw:.2f} W: heatsink at most {(100-40)/pw-6:.1f} C/W for TJ <= 100 C at 40 C ambient")
p,m,_=total("typ"); pw=(RAW-V15)*max(p,m)/1000
print(f"typical regulator {pw:.2f} W: free-air TO-220 (about 50 C/W) would reach TJ {40+pw*50:.0f} C")
# Sizing for shared supply parts (decision 96): IC quiescent current at typical x 1.5,
# use-dependent loads (relays, LEDs, signal, headphones) at their maximum.
K=1.5
ic_p=sum(n*t for n,t,m,r in parts.values()); ic_m=sum(n*t for n,t,m,r in parts.values() if r=="pm")
sp=K*(ic_p+l7805_iq[0])+sum(v[1] for v in fixed_p.values())+led5_max+sum(sig_max.values())
sm=K*ic_m+sum(v[1] for v in fixed_m.values())+sum(sig_max.values())
print(f"sizing: +15 V {sp:.0f} mA, -15 V {sm:.0f} mA")
