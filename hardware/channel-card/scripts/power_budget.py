# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Channel card supply budget and regulator dissipation (system validation 2026-10-06, finding 2).

Same method as hardware/master/scripts/power_budget.py: count the parts on the channel
sheets (scripts/build/bom.csv) and add their supply currents, typical and worst case
(every IC at datasheet maximum, every LED lit), per rail. Sources: NE5532 TI SLOS075K
(6 / 16 mA per package); TL072 TI SLOS080W (1.4 / 2.5 mA per amplifier); OPA2171 TI SBOS516H
(0.475 / 0.595 mA per amplifier); TL062 TI SLOS078N (0.2 / 0.25 mA per amplifier); SSI2144 Rev 3.0
(ICC 5.0 / 6.2 mA, IEE 5.2 / 6.4 mA); SSI2162 Rev 1.2 (Class AB 6 / 8 mA); LM13700 TI
SNOSBW2 (2.6 / 4 mA, both channels at IABC 500 uA) plus the Q current; LM339 TI SLCS006
(0.8 / 2.5 mA, as in the master script; V- on PGND, so +15 V only); uA78L05 TI SLVS010X (3.6 / 6 mA, stand-in for the
ST part). The AD8273 receiver became a TL072 (decision 143).
DG412/DG413 draw microamps and are left out.
Also prints the decision 96 sizing figure.
Usage: python3 power_budget.py [raw rail, default 20]
"""
import sys
RAW=float(sys.argv[1]) if len(sys.argv)>1 else 20.0
V15,V5=15.1,5.0
# part: (count, typ mA, max mA, rails) -- "pm" = both ±15 V, "p" = +15 V only
parts={
 "NE5532":(8,6.0,16.0,"pm"),
 "TL072 (incl. U1 receiver, decision 143)":(5,2.8,5.0,"pm"),
 "TL062 (U401, U404)":(2,0.4,0.5,"pm"),
 "OPA2171 (U204, fader buffer and control summer)":(1,0.95,1.19,"pm"),
 "SSI2144 (ICC/IEE, worse rail)":(2,5.2,6.4,"pm"),
 "SSI2162":(1,6.0,8.0,"pm"),
 "LM13700 incl. Q current":(1,3.2,4.6,"pm"),
 "LM339 (meter)":(2,0.8,2.5,"p"),
}
led_btn=(V15-2.0)/12.0                     # 7 button LEDs, 12k from +15 V
fixed_p={"LM317 divider 2k4":(6.25,6.25),"CUTOFF and offset pots, refs (+15 V)":(1.8,1.8)}
fixed_m={"LM337 divider 2k4":(6.25,6.25),"fader and pots (-15 V)":(1.5,1.5)}
btn=(3.5*led_btn,7*led_btn)                # typical: about half the buttons lit
# +5 V from the 78L05, taken from +15 V: 8 meter LEDs, 1k5 from +5 V (about 2 mA each)
led5=(8.0,16.0)                            # typical: about half the meter lit
iq78=(3.6,6.0)
# signal current into the master's virtual earths: 11 bus lines at 22k, a few mA average
sig=(2.0,6.0)
def total(i):
    p=sum(n*(t,m)[i] for n,t,m,r in parts.values())
    mneg=sum(n*(t,m)[i] for n,t,m,r in parts.values() if r=="pm")
    p+=sum(v[i] for v in fixed_p.values())+btn[i]; mneg+=sum(v[i] for v in fixed_m.values())
    i5=led5[i]+iq78[i]; p+=i5
    p+=sig[i]; mneg+=sig[i]
    return p,mneg,i5
for i,k in enumerate(("typ","max")):
    p,m,i5=total(i)
    print(f"{k}: +15 V {p:.0f} mA, -15 V {m:.0f} mA, +5 V {i5:.0f} mA | "
          f"LM317 {(RAW-V15)*p/1000:.2f} W, LM337 {(RAW-V15)*m/1000:.2f} W, "
          f"78L05 {(V15-V5)*led5[i]/1000+V15*iq78[i]/1000:.2f} W (raw {RAW:g} V)")
# Sizing for shared supply parts (decision 96): IC quiescent current at typical x 1.5,
# use-dependent loads (LEDs, signal) at their maximum. Read by tools/system_power_budget.py.
K=1.5
ic_p=sum(n*t for n,t,m,r in parts.values()); ic_m=sum(n*t for n,t,m,r in parts.values() if r=="pm")
sp=K*(ic_p+iq78[0])+sum(v[1] for v in fixed_p.values())+btn[1]+led5[1]+sig[1]
sm=K*ic_m+sum(v[1] for v in fixed_m.values())+sig[1]
print(f"sizing: +15 V {sp:.0f} mA, -15 V {sm:.0f} mA")
