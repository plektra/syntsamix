# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Power board start-up into the rail capacitance: behavioural (averaged) ngspice model.

Checks whether the brick's overload protection (hiccup at 105 % of rated power minimum) trips while
both converters charge about 1.1 mF per rail. Averaged model, no switching:
- Brick and soft-start FET: input ramps 0 to 24 V at 3.6 V/ms (design.py), so both converters reach
  their 21.14 V UVLO start at about 5.85 ms.
- Each TPS54560 follows its soft-start reference (0 to 20 V in 1024 cycles = 2.56 ms at 400 kHz,
  SLVSBN0C 7.3.8; or a slower external ramp), limited by the switch current limit
  (6.3 / 7.5 / 8.8 A min / typ / max, SLVSBN0C 6.5) minus half the inductor ripple; the inverter's
  output current is the inductor current times (1 - D).
- Losses: catch diode 0.5 V, switch 0.1 ohm, inductor DCR, 0.3 W fixed per converter.
- Card load: decision 96 sizing current (1.35 / 1.11 A prototype), scaled with rail voltage up to
  17 V (the LM317/LM337 drop out below that).
- Brick limits: GSM120B24 105 % of 120 W = 126 W, GSM160B24 105 % of 160 W = 168 W (Mean Well
  GSM120B / GSM160B specs: overload 105-160 % / 105-150 %, hiccup mode).
Frequency foldback at low output voltage is ignored (it only lowers the start current).
"""
import os, re, subprocess, tempfile

C_RAIL = 1.13e-3        # 0.37 mF on the prototype cards + 0.76 mF on this board (STATUS.md)
VIN, RAMP = 24.0, 3.617e3   # V, V/s (design.py soft-start FET)
T_EN = 21.14 / RAMP     # both UVLOs start here
FSW = 400e3
P_LIMITS = (("GSM120B24", 126.0), ("GSM160B24", 168.0))

NET = """* power board start-up, averaged
Vin vin 0 PWL(0 0 {tr} {vin})
* soft-start references (0 to 20 V)
Brefp refp 0 V=min(20*min(1,max(0,(time-{tenp})/{tssp})),20*(1-exp(-max(0,time-{tenp})/{tau})))
Brefn refn 0 V=min(20*min(1,max(0,(time-{tenn})/{tssn})),20*(1-exp(-max(0,time-{tenn})/{tau})))
* +20 V buck: output current limited to Ilim - ripple/2
Bdp dp 0 V=min(0.98,V(vp)/max(V(vin),1))
Bimp imp 0 V={ilim}-0.5*(V(vin)-V(vp))*V(dp)/(15e-6*{fsw})
Biop iop 0 V=min(V(imp),max(0,50*(V(refp)-V(vp))))
Bbuck 0 vp I=V(iop)
Cp vp 0 {c}
Bldp vp 0 I={ilp}*min(1,max(0,V(vp)/17))
Bpp pp 0 V=V(iop)*(V(vp)+0.5*(1-V(dp)))+V(iop)^2*(0.1*V(dp)+0.028)+0.3*(time>{tenp})
* -20 V inverter, magnitude on node vn
Bdn dn 0 V=V(vn)/(max(V(vin),1)+V(vn))
Bilm ilm 0 V={ilim}-0.5*V(vin)*V(dn)/(22e-6*{fsw})
Bion ion 0 V=min(V(ilm)*(1-V(dn)),max(0,50*(V(refn)-V(vn))))
Binv 0 vn I=V(ion)
Cn vn 0 {c}
Bldn vn 0 I={iln}*min(1,max(0,V(vn)/17))
Bpn pn 0 V=V(ion)*(V(vn)+0.5)+(V(ion)/(1-V(dn)))^2*(0.1*V(dn)+0.037)+0.3*(time>{tenn})
Bpt pt 0 V=V(pp)+V(pn)
Bo1 o1 0 V=(V(pt)>{p1})?1:0
Bo2 o2 0 V=(V(pt)>{p2})?1:0
.tran 5u 100m
.control
run
meas tran pmax max V(pt)
meas tran t1 integ V(o1)
meas tran t2 integ V(o2)
meas tran tp when V(vp)=19.0 rise=1
meas tran tn when V(vn)=19.0 rise=1
.endc
.end
"""


def run(ilim, inv_delay=0.0, tss=2.56e-3, tau=1e-9, ilp=1.35, iln=1.11):
    p = dict(tr=VIN / RAMP, vin=VIN, tenp=T_EN, tenn=T_EN + inv_delay, tssp=tss, tssn=tss,
             ilim=ilim, tau=tau, fsw=FSW, c=C_RAIL, ilp=ilp, iln=iln,
             p1=P_LIMITS[0][1], p2=P_LIMITS[1][1])
    with tempfile.NamedTemporaryFile("w", suffix=".cir", delete=False) as f:
        f.write(NET.format(**p))
        path = f.name
    out = subprocess.run(["ngspice", "-b", path], capture_output=True, text=True).stdout
    os.unlink(path)
    m = dict(re.findall(r"^(\w+)\s*=\s*([-+0-9.eE]+)", out, re.M))
    return {k: float(v) for k, v in m.items()}


# FB ramp: Css from the output through a diode into FB; the loop holds FB at 0.8 V, so
# Css dVo/dt + (Vo - 0.8)/240k = 80 uA: an RC rise to 20 V with tau = 240k x Css
CASES = [
    ("both together, 2.6 ms soft-start", 0.0, 2.56e-3, 1e-9),
    ("inverter 10 ms after the buck", 10e-3, 2.56e-3, 1e-9),
    ("both together, linear 20 ms ramp", 0.0, 20e-3, 1e-9),
    ("FB ramp, Css 33 nF (tau 7.9 ms)", 0.0, 2.56e-3, 240e3 * 33e-9),
    ("FB ramp, Css 47 nF (tau 11.3 ms)", 0.0, 2.56e-3, 240e3 * 47e-9),
]

if __name__ == "__main__":
    print(f"rail capacitance {C_RAIL*1e3:.2f} mF each, load 1.35 / 1.11 A, UVLO start {T_EN*1e3:.2f} ms")
    print(f"{'case':36s} {'Ilim':>5s} {'Pmax W':>7s} {'>126 W ms':>9s} {'>168 W ms':>9s} {'+19 V ms':>8s} {'-19 V ms':>8s}")
    for name, dly, tss, tau in CASES:
        for ilim in (6.3, 7.5, 8.8):
            r = run(ilim, dly, tss, tau)
            print(f"{name:36s} {ilim:5.1f} {r['pmax']:7.1f} {r['t1']*1e3:9.2f} {r['t2']*1e3:9.2f}"
                  f" {r.get('tp', float('nan'))*1e3:8.2f} {r.get('tn', float('nan'))*1e3:8.2f}")
