# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
import json,os
R0805="Resistor_SMD:R_0805_2012Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"
CBIP="Capacitor_THT:C_Radial_D5.0mm_H11.0mm_P2.00mm"
PROV={"Note":"Provisional: set from the SSI2144 breadboard (simulation/filter/BREADBOARD.md)"}
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
NE={"Manufacturer":"Texas Instruments"}
def ne(ref,unit,x,y,temp=None):
    S("Amplifier_Operational","NE5532",temp or ref,"NE5532",x,y,"Package_SO:SOIC-8_3.9x4.9mm_P1.27mm","SX-IC-004",unit,NE)
    return temp or ref
# ---------------- per side
def side(P,o,dy,ssi,ota_unit,ota_ref,ota_pins,pre,iv,post,dgA,dgB):
    # o: ref offset; dy: y offset
    r=lambda n:f"R{n+o}"; c=lambda n:f"C{n+o}"
    y=lambda v:v+dy
    C(c(101),"10u bipolar","SX-C-003",f"{P}_PREFILT",f"{P}_FAC",40,y(70),CBIP)
    R(r(101),"10k","SX-R-002",f"{P}_FAC",f"{P}_PSUM",60,y(70))
    R(r(102),"10k","SX-R-002",f"{P}_PSUM",f"{P}_FIN",80,y(42))
    R(r(103),"16k9","SX-R-017",f"{P}_PSUM",f"{P}_DRVA",100,y(42))
    jp=f"JP{101+o}"
    S("Connector_Generic","Conn_02x02_Odd_Even",jp,"DRIVE (fit both = MEDIUM)",125,y(42),"Connector_PinHeader_2.54mm:PinHeader_2x02_P2.54mm_Vertical","SX-CONN-004")
    N(f"{P}_DRVA",jp+".1"); N(f"{P}_FIN",jp+".2"); N(f"{P}_PGN",jp+".3"); N("AGND",jp+".4")
    u,pins=pre; N(f"{P}_PSUM",f"{u}.{pins[0]}"); N("AGND",f"{u}.{pins[1]}"); N(f"{P}_FIN",f"{u}.{pins[2]}")
    R(r(104),"17k4","SX-R-009",f"{P}_FIN",f"{P}_SIN",120,y(75))
    R(r(105),"200","SX-R-010",f"{P}_SIN","AGND",140,y(90))
    R(r(106),"200","SX-R-010","AGND",f"{P}_SINN",140,y(118))
    U=ssi
    S("syntsamix","SSI2144",U,"SSI2144",175,y(85),"Package_SO:QSOP-16_3.9x4.9mm_P0.635mm","SX-IC-001",props={"Manufacturer":"Sound Semiconductor","MPN":"SSI2144SS-TU","Supplier":"Electrokit","SupplierPN":"41019301"})
    for pn,net in ((1,"SIN"),(2,"SINN"),(3,"OUTI"),(15,"FC"),(14,"QP"),(13,"C1A"),(12,"C1B"),(11,"C2A"),(10,"C2B"),(6,"C3A"),(7,"C3B"),(4,"C4A"),(5,"C4B")):
        N(f"{P}_{net}",f"{U}.{pn}")
    N("+15V",U+".16"); N("-15V",U+".8"); N("AGND",U+".9")
    C(c(102),"6n8 C0G","SX-C-006",f"{P}_C1A",f"{P}_C1B",210,y(68))
    C(c(103),"6n8 C0G","SX-C-006",f"{P}_C2A",f"{P}_C2B",222,y(82))
    C(c(104),"6n8 C0G","SX-C-006",f"{P}_C3A",f"{P}_C3B",210,y(96))
    C(c(105),"560p C0G","SX-C-007",f"{P}_C4A",f"{P}_C4B",222,y(110))
    R(r(107),"13k","SX-R-011",f"{P}_QP","AGND",155,y(135))
    R(r(108),"820 TFPT","SX-R-089",f"{P}_FC",f"{P}_TC",165,y(145),"Resistor_SMD:R_0603_1608Metric",{"Manufacturer":"Vishay","MPN":"TFPT0603L8200FV","Supplier":"Mouser","SupplierPN":"71-TFPT0603L8200FV","Note":"Vishay TFPT linear PTC thin film, +4110 ppm/K; in series with R122/R172 180R = 1k at about +3370 ppm/K (decision 130); place against the SSI2144"})
    R(r(122),"180","SX-R-090",f"{P}_TC","AGND",165,y(150),props={"Note":"Low-tempco part of the 1k tempco leg (decision 130); keep the TFPT next to the SSI2144, this one may sit further away"})
    R(r(109),"470k","SX-R-048",f"{P}_FC",f"{P}_OFS",145,y(145))
    rv=f"RV{101+o}"
    S("Device","R_Potentiometer_Trim",rv,"50k (OFFSET)",125,y(145),"Potentiometer_THT:Potentiometer_Bourns_3296W_Vertical","SX-TRIM-001",props={"Manufacturer":"Bourns","MPN":"3296W-1-503LF"})
    N("+15V",rv+".1"); N(f"{P}_OFS",rv+".2"); N("-15V",rv+".3")
    R(r(110),"100k","SX-R-007","FCV",f"{P}_FC",185,y(145))
    u,pins=iv; N(f"{P}_OUTI",f"{u}.{pins[0]}"); N("AGND",f"{u}.{pins[1]}"); N(f"{P}_IV",f"{u}.{pins[2]}")
    R(r(111),"8k66","SX-R-014",f"{P}_OUTI",f"{P}_IV",255,y(45),props=PROV)
    C(c(106),"100p C0G","SX-C-008",f"{P}_OUTI",f"{P}_IV",272,y(45))
    C(c(107),"10u bipolar","SX-C-003",f"{P}_IV",f"{P}_PA",290,y(75),CBIP)
    R(r(112),"100k","SX-R-007",f"{P}_PA","AGND",300,y(95))
    u,pins=post; N(f"{P}_PA",f"{u}.{pins[0]}"); N(f"{P}_PFB",f"{u}.{pins[1]}"); N(f"{P}_FILT",f"{u}.{pins[2]}")
    R(r(113),"6k04","SX-R-016",f"{P}_PFB",f"{P}_FILT",320,y(50))
    R(r(114),"10k","SX-R-002",f"{P}_PFB",f"{P}_PGN",338,y(50))
    # Q VCA (LM13700 half)
    pplus,pminus,pout,piabc=ota_pins
    S("Amplifier_Operational","LM13700",ota_ref,"LM13700",200,y(140),"Package_SO:SOIC-16_3.9x9.9mm_P1.27mm","SX-IC-006",ota_unit,{"Manufacturer":"Texas Instruments"})
    N(f"{P}_QPLUS",f"{ota_ref}.{pplus}"); N(f"{P}_QSUM",f"{ota_ref}.{pminus}"); N(f"{P}_SINN",f"{ota_ref}.{pout}"); N(f"{P}_IABC",f"{ota_ref}.{piabc}")
    R(r(115),"604","SX-R-012",f"{P}_QPLUS","AGND",215,y(160))
    R(r(116),"604","SX-R-012","AGND",f"{P}_QSUM",232,y(160))
    R(r(117),"17k4","SX-R-009",f"{P}_IV",f"{P}_QSUM",240,y(118))
    R(r(118),"52k3","SX-R-013",f"{P}_RHALF",f"{P}_FIN",255,y(150),props={"Note":"Half compensation (default)"})
    R(r(119),"17k4","SX-R-009",f"{P}_FIN",f"{P}_RFULL",272,y(150),props={"Note":"Full compensation"})
    jq=f"JP{102+o}"
    S("Connector_Generic","Conn_01x03",jq,"Q COMP (1-2 HALF, 2-3 FULL, open NONE)",295,y(135),"Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical","SX-CONN-005")
    N(f"{P}_RHALF",jq+".1"); N(f"{P}_QSUM",jq+".2"); N(f"{P}_RFULL",jq+".3")
    R(r(120),"41k2","SX-R-015",f"{P}_IABC","QW",185,y(125),props=PROV)
    R(r(121),"100k","SX-R-007",f"{P}_POSTFILT","AGND",395,y(90))
    for k,net in ((101,"SIN"),(102,"IV"),(103,"POSTFILT")):
        S("Connector","TestPoint",f"TP{k+o}",f"{P}_{net}",400,y(100),"TestPoint:TestPoint_Pad_D1.5mm","none (PCB test pad)"); N(f"{P}_{net}",f"TP{k+o}.1")
    for (u,unit,pin_in,pin_d,pin_s,src) in (dgA,dgB):
        S("Analog_Switch","DG413xY",u,"DG413DY",370,y(60 if src=='FAC' else 100),"Package_SO:SOIC-16_3.9x9.9mm_P1.27mm","SX-IC-005",unit,{"Manufacturer":"Vishay"})
        N("BYP",f"{u}.{pin_in}"); N(f"{P}_POSTFILT",f"{u}.{pin_d}"); N(f"{P}_{src}",f"{u}.{pin_s}")
# L: OTA A = unit 3 (+3,-4,out5,IABC1); R: OTA B = unit 1 (+14,-13,out12,IABC16)
side("L",0,0,"U101",3,"U103",(3,4,5,1),("U104",(2,3,1)),("U105",(2,3,1)),("U106",(3,2,1)),
     ("U108",1,1,2,3,"FAC"),("U91084",4,16,15,14,"FILT"))
side("R",50,165,"U102",1,"U91031",(14,13,12,16),("U91042",(6,5,7)),("U91052",(6,5,7)),("U91062",(5,6,7)),
     ("U91082",2,8,7,6,"FAC"),("U91083",3,9,10,11,"FILT"))
ne("U104",1,90,75); ne("U104",2,90,240,"U91042")
ne("U105",1,255,75); ne("U105",2,255,240,"U91052")
ne("U106",1,320,75); ne("U106",2,320,240,"U91062")
# ---------------- shared: cutoff summer
Y=355
S("Device","R_Potentiometer","RV181","50k lin (CUTOFF)",40,Y+15,"Potentiometer_THT:Potentiometer_Alpha_RD901F-40-00D_Single_Vertical","SX-POT-003",props={"Manufacturer":"Alpha","MPN":"RD901F-40-15K-B50K-0057","Supplier":"Thonk","Note":"Panel; clockwise end (pin 3) raises the cutoff"})
N("-15V","RV181.1"); N("CUTW","RV181.2"); N("+15V","RV181.3")
R("R181","301k","SX-R-018","CUTW","FSUM",62,Y+15)
S("Connector_Audio","AudioJack2_SwitchT","J181","CUTOFF CV (1 V/oct)",40,Y+45,"","SX-CONN-003",props={"Note":"6.3 mm mono switched jack on the top panel; part and footprint to choose"})
N("CVIN","J181.T"); N("AGND","J181.TN"); N("AGND","J181.S")
R("R182","100k","SX-R-007","CVIN","FSUM",62,Y+45)
S("Amplifier_Operational","TL072","U107","TL072",100,Y+30,"Package_SO:SOIC-8_3.9x4.9mm_P1.27mm","SX-IC-007",1,NE)
N("FSUM","U107.2"); N("AGND","U107.3"); N("FCV","U107.1")
R("R183","162k","SX-R-019","FSUM","FVO",90,Y)
S("Device","R_Potentiometer_Trim","RV182","50k (V/OCT)",112,Y,"Potentiometer_THT:Potentiometer_Bourns_3296W_Vertical","SX-TRIM-001",props={"Manufacturer":"Bourns","MPN":"3296W-1-503LF"})
N("FVO","RV182.1"); N("FCV","RV182.2"); N("FCV","RV182.3")
C("C181","22p C0G","SX-C-004","FSUM","FCV",130,Y)
S("Amplifier_Operational","TL072","U91072","TL072",130,Y+40,"Package_SO:SOIC-8_3.9x4.9mm_P1.27mm","SX-IC-007",2,NE)
N("AGND","U91072.5"); N("SPARE_OA","U91072.6"); N("SPARE_OA","U91072.7")
# resonance
R("R184","12k","SX-R-008","+15V","QTOP",160,Y+10,props={"Note":"R184 12k keeps RV183 within Alpha's 0.02 W non-B rating (17 mW, was 21 mW at 10k); provisional with R120/R170: set from the SSI2144 breadboard (simulation/filter/BREADBOARD.md)"})
S("Device","R_Potentiometer","RV183","10k rev. audio (RESONANCE)",180,Y+25,"Potentiometer_THT:Potentiometer_Alpha_RD901F-40-00D_Single_Vertical","SX-POT-012",props={"Manufacturer":"Alpha","MPN":"RD901F-40-15K-C10K","Supplier":"Tayda","SupplierPN":"A-5369","Note":"Reverse-audio (C) taper per SSI2144 datasheet Figure 3"})
N("QBOT","RV183.1"); N("QW","RV183.2"); N("QTOP","RV183.3")
S("Device","D","D181","1N4148W",200,Y+25,"Diode_SMD:D_SOD-123","SX-D-003"); N("QMID","D181.1"); N("QBOT","D181.2")
S("Device","D","D182","1N4148W",228,Y+25,"Diode_SMD:D_SOD-123","SX-D-003"); N("-15V","D182.1"); N("QMID","D182.2")
# bypass button
S("Switch","SW_Push_DPDT","SW181","FILTER BYPASS (latching)",260,Y+25,"","SX-SW-001")
N("BYP","SW181.3"); N("+5V","SW181.2"); N("BYP_LEDK","SW181.6"); N("PGND","SW181.5")
S("Device","LED","D183","BYPASS LED",290,Y+25,"LED_THT:LED_D3.0mm","SX-D-002"); N("BYP_LEDK","D183.1"); N("BYP_LED","D183.2")
R("R185","12k","SX-R-008","+15V","BYP_LED",305,Y+25)
R("R186","100k","SX-R-007","PGND","BYP",245,Y+40)
for k,net in ((181,"FCV"),(182,"QW"),(183,"AGND")):
    S("Connector","TestPoint",f"TP{k}",net,500,Y+k-180,"TestPoint:TestPoint_Pad_D1.5mm","none (PCB test pad)"); N(net,f"TP{k}.1")
# power units and unused LM13700 parts
S("Amplifier_Operational","LM13700","U91035","LM13700",335,Y+25,"Package_SO:SOIC-16_3.9x9.9mm_P1.27mm","SX-IC-006",5,{"Manufacturer":"Texas Instruments"}); N("-15V","U91035.6"); N("+15V","U91035.11")
S("Amplifier_Operational","LM13700","U91034","LM13700",350,Y+10,"Package_SO:SOIC-16_3.9x9.9mm_P1.27mm","SX-IC-006",4,{"Manufacturer":"Texas Instruments"}); N("AGND","U91034.7")
S("Amplifier_Operational","LM13700","U91032","LM13700",350,Y+40,"Package_SO:SOIC-16_3.9x9.9mm_P1.27mm","SX-IC-006",2,{"Manufacturer":"Texas Instruments"}); N("AGND","U91032.10")
for i,(t,x) in enumerate((("U91043",370),("U91053",382),("U91063",394),("U91073",406))):
    ne(t[:2]+t[3:5] if False else "U10"+t[4],3,x,Y+25,t); N("+15V",t+".8"); N("-15V",t+".4")
S("Analog_Switch","DG413xY","U91085","DG413DY",425,Y+25,"Package_SO:SOIC-16_3.9x9.9mm_P1.27mm","SX-IC-005",5,{"Manufacturer":"Vishay"})
N("-15V","U91085.4"); N("AGND","U91085.5"); N("+5V","U91085.12"); N("+15V","U91085.13")
# decoupling: 100n from each rail per IC
k=191
for i in range(8):
    x=455+i*13
    C(f"C{k}","100n","SX-C-002","+15V","AGND",x,Y+12); k+=1
    C(f"C{k}","100n","SX-C-002","-15V","AGND",x,Y+38); k+=1
netl=[]
for n,p in nets.items():
    d={"name":n,"pins":p}
    if n in ("L_PREFILT","R_PREFILT"): d.update(scope="hierarchical",shape="input")
    elif n in ("L_POSTFILT","R_POSTFILT"): d.update(scope="hierarchical",shape="output")
    elif n not in ("+15V","-15V","+5V","AGND","PGND"): d["scope"]="local"
    netl.append(d)
out={"auto_layout":False,"max_paper":"A2","symbols":syms,"nets":netl}
CARD=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'
os.makedirs(T,exist_ok=True)
json.dump(out,open(T+'filter.json','w'),separators=(',',':'))
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'filter.kicad_sch'}],["sch_build_circuit",out]],open(T+'calls_filter.json','w'))
print(len(syms),"symbols",len(netl),"nets")
# sanity: nets with a single pin
for n,p in nets.items():
    if len(p)<2: print("single-pin net",n,p)
