# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
import json,os
CARD=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
R0805="Resistor_SMD:R_0805_2012Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"
CBIP="Capacitor_THT:C_Radial_D5.0mm_H11.0mm_P2.00mm"; SO8="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"; SO16="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm"
syms=[];nets={}
def S(lib,name,ref,val,x,y,fp,pn,unit=None,props=None):
    d={"library":lib,"symbol_name":name,"reference":ref,"value":val,"x_mm":x,"y_mm":y,"footprint":fp,"properties":{"ProjectPN":pn,**(props or {})}}
    if unit: d["unit"]=unit
    syms.append(d)
def N(net,*pins):
    for p in pins:
        r,n=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":n})
def R(ref,val,pn,a,b,x,y,fp=R0805,props=None):
    S("Device","R",ref,val,x,y,fp,pn,props=props); N(a,ref+".1"); N(b,ref+".2")
def C(ref,val,pn,a,b,x,y,fp=C0805,props=None):
    S("Device","C",ref,val,x,y,fp,pn,props=props); N(a,ref+".1"); N(b,ref+".2")
def OA(part,ref,unit,x,y,pins,pn):
    S("Amplifier_Operational",part,ref,part,x,y,SO8,pn,unit,{"Manufacturer":"Texas Instruments"})
    for net,p in pins: N(net,f"{ref}.{p}")
# ---- audio, one row per side
def side(P,o,y,iv,inv):
    r=lambda n:f"R{n+o}"; c=lambda n:f"C{n+o+20}"
    C(c(201),"10u bipolar","SX-C-003",f"{P}_POSTFILT",f"{P}_VIN",40,y,CBIP)
    R(r(201),"10k","SX-R-002",f"{P}_VIN",f"{P}_IIN",65,y)
    a,b=(f"{P}_RC",f"{P}_IIN") if P=="L" else (f"{P}_IIN",f"{P}_RC")   # pin order matches the wired drawing
    R(r(202),"110","SX-R-022",a,b,90,y+20)
    C(c(202),"2n2 C0G","SX-C-009",*(("AGND",f"{P}_RC") if P=="L" else (f"{P}_RC","AGND")),115,y+20)
    OA("NE5532",iv[0],iv[1],185,y,((f"{P}_IOUT",iv[2][0]),("AGND",iv[2][1]),(f"{P}_VO",iv[2][2])),"SX-IC-004")
    R(r(203),"10k","SX-R-002",f"{P}_IOUT",f"{P}_VO",175,y-25)
    C(c(203),"100p C0G","SX-C-008",f"{P}_IOUT",f"{P}_VO",205,y-25)
    R(r(204),"10k","SX-R-002",f"{P}_VO",f"{P}_INV",225,y)
    OA("NE5532",inv[0],inv[1],260,y,((f"{P}_INV",inv[2][0]),("AGND",inv[2][1]),(f"{P}_POSTFADE",inv[2][2])),"SX-IC-004")
    R(r(205),"10k","SX-R-002",f"{P}_INV",f"{P}_POSTFADE",255,y-25)
side("L",0,70,("U202",1,(2,3,1)),("U203",1,(2,3,1)))
side("R",50,160,("U92022",2,(6,5,7)),("U92032",2,(6,5,7)))
S("syntsamix","SSI2162","U201","SSI2162",145,115,"Package_SO:SSOP-10_3.9x4.9mm_P1.00mm","SX-IC-002",props={"Manufacturer":"Sound Semiconductor","MPN":"SSI2162SS-TU","Supplier":"Electrokit"})
for pn,net in ((2,"L_IIN"),(3,"VC"),(4,"L_IOUT"),(1,"MODE"),(9,"R_IIN"),(8,"VC"),(7,"R_IOUT")): N(net,f"U201.{pn}")
N("+15V","U201.10"); N("-15V","U201.6"); N("AGND","U201.5")
R("R206","14k3","SX-R-030","+15V","MODE",120,125,props={"Note":"DNP = Class AB (default); fit for Class A, mode current about 1 mA (datasheet Rev 1.2)"})
# ---- fader law (shared)
Y=250
S("Device","R_Potentiometer","RV201","10k lin FADER",40,Y,"Potentiometer_THT:Potentiometer_Bourns_PTA6043_Single_Slide","SX-POT-001",props={"Manufacturer":"Bourns","MPN":"PTA6043-2015DPB103","Note":"Pin 1 = bottom of travel (datasheet: output rises from terminal 1)"})
N("-15V","RV201.1"); N("FADW","RV201.2"); N("AGND","RV201.3")
OA("TL072","U204",1,70,Y,(("FADW",3),("VB",2),("VB",1)),"SX-IC-007")
R("R207","113k","SX-R-023","VB","VSUM",215,Y-30)
R("R208","453k","SX-R-024","+15V","VSUM",240,Y-30)
R("R209","100k","SX-R-007","VB","SD1IN",100,Y+5)
R("R210","221k","SX-R-025","+15V","SD1IN",100,Y+35)
OA("TL072","U92042",2,135,Y+15,(("SD1IN",5),("SD1K",6),("SD1O",7)),"SX-IC-007")
S("Device","D","D201","1N4148W",160,Y+40,"Diode_SMD:D_SOD-123","SX-D-003"); N("SD1O","D201.1"); N("SD1K","D201.2")
R("R211","63k4","SX-R-026","SD1K","VSUM",185,Y+15)
R("R212","100k","SX-R-007","VB","SD2IN",100,Y+65)
R("R213","124k","SX-R-027","+15V","SD2IN",100,Y+95)
OA("TL072","U205",1,135,Y+75,(("SD2IN",3),("SD2K",2),("SD2O",1)),"SX-IC-007")
S("Device","D","D202","1N4148W",160,Y+100,"Diode_SMD:D_SOD-123","SX-D-003"); N("SD2O","D202.1"); N("SD2K","D202.2")
R("R214","8k66","SX-R-014","SD2K","VSUM",185,Y+75)
OA("TL072","U92052",2,250,Y+20,(("VPLUS",5),("VSUM",6),("VC",7)),"SX-IC-007")
R("R215","10k","SX-R-002","VSUM","VC",265,Y-30)
C("C224","1u","SX-C-010","VSUM","VC",290,Y-30,props={"Note":"10 ms control smoothing: fader wiper noise and click-free mute ramp"})
R("R216","33k2","SX-R-028","MUTE_V","VSUM",215,Y+60)
R("R217","100k","SX-R-007","DUCK_V","VPLUS",240,Y+60)
R("R218","15k8","SX-R-029","VPLUS","AGND",265,Y+60)
# DG413: SW1 (NO) duck, SW4 (NO) mute, SW2/SW3 unused
DG={"Manufacturer":"Vishay"}
S("Analog_Switch","DG413xY","U206","DG413DY",330,Y-20,SO16,"SX-IC-005",1,DG); N("DUCK_CTRL","U206.1"); N("DUCK_V","U206.2"); N("SC_ENV","U206.3")
S("Analog_Switch","DG413xY","U92062","DG413DY",330,Y+15,SO16,"SX-IC-005",2,DG); N("MUTE_CTRL","U92062.8"); N("MUTE_V","U92062.7"); N("-15V","U92062.6")
S("Analog_Switch","DG413xY","U92063","DG413DY",330,Y+50,SO16,"SX-IC-005",3,DG); N("AGND","U92063.9","U92063.10","U92063.11")
S("Analog_Switch","DG413xY","U92064","DG413DY",330,Y+85,SO16,"SX-IC-005",4,DG); N("AGND","U92064.16","U92064.15","U92064.14")
# buttons
def button(n,ref,sw,led,rl,rp,x,y,name):
    S("Switch","SW_Push_DPDT",sw,f"{name} (latching)",x,y,"","SX-SW-001")
    N(f"{n}_CTRL",sw+".3"); N("+5V",sw+".2"); N(f"{n}_LEDK",sw+".6"); N("PGND",sw+".5")
    S("Device","LED",led,f"{name} LED",x+30,y,"LED_THT:LED_D3.0mm","SX-D-002"); N(f"{n}_LEDK",led+".1"); N(f"{n}_LED",led+".2")
    R(rl,"12k","SX-R-008","+15V",f"{n}_LED",x+55,y)
    R(rp,"100k","SX-R-007","AGND",f"{n}_CTRL",x-25,y+15)
button("MUTE","",  "SW201","D203","R219","R220",60,375,"MUTE")
button("DUCK","",  "SW202","D204","R221","R222",175,375,"DUCK")
# power units
for t,part,pn,x in (("U92023","NE5532","SX-IC-004",380),("U92033","NE5532","SX-IC-004",395),("U92043","TL072","SX-IC-007",410),("U92053","TL072","SX-IC-007",425)):
    S("Amplifier_Operational",part,t,part,x,375,SO8,pn,3,{"Manufacturer":"Texas Instruments"}); N("+15V",t+".8"); N("-15V",t+".4")
S("Analog_Switch","DG413xY","U92065","DG413DY",445,375,SO16,"SX-IC-005",5,DG)
N("-15V","U92065.4"); N("AGND","U92065.5"); N("+5V","U92065.12"); N("+15V","U92065.13")
k=225
for i in range(6):
    x=330+i*14
    C(f"C{k}","100n","SX-C-002","+15V","AGND",x,140); k+=1
    C(f"C{k}","100n","SX-C-002","-15V","AGND",x,170); k+=1
for k,net in ((201,"VC"),(202,"VB"),(203,"L_POSTFADE"),(204,"R_POSTFADE"),(205,"SC_ENV")):
    S("Connector","TestPoint",f"TP{k}",net,500,k,"TestPoint:TestPoint_Pad_D1.5mm","none (PCB test pad)"); N(net,f"TP{k}.1")
netl=[]
for n,p in nets.items():
    d={"name":n,"pins":p}
    if n in ("L_POSTFILT","R_POSTFILT","SC_ENV"): d.update(scope="hierarchical",shape="input")
    elif n in ("L_POSTFADE","R_POSTFADE"): d.update(scope="hierarchical",shape="output")
    elif n not in ("+15V","-15V","+5V","AGND","PGND"): d["scope"]="local"
    netl.append(d)
out={"auto_layout":False,"max_paper":"A2","symbols":syms,"nets":netl}
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'
os.makedirs(T,exist_ok=True)
json.dump(out,open(T+'level.json','w'),separators=(',',':'))
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'level.kicad_sch'}],["sch_build_circuit",out]],open(T+'calls_level.json','w'))
print(len(syms),"symbols",len(netl),"nets")
for n,p in nets.items():
    if len(p)<2: print("single-pin net",n,p)
