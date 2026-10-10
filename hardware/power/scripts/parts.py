# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Power board parts: project part number, BOM fields and footprint per part type (docs/parts.csv).

Parts from the 2026-10-07 datasheet and stock checks (decision 100). MPN and SupplierPN stay
blank where the part is still to choose.
"""
R0805="Resistor_SMD:R_0805_2012Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"; C1210="Capacitor_SMD:C_1210_3225Metric"
def lcsc(pn,mfr,mpn,code): return {"ProjectPN":pn,"Manufacturer":mfr,"MPN":mpn,"Supplier":"LCSC","SupplierPN":code}
P={
 # resistors (1 % 0805 thick film; generic, JLC basic where available)
 "10k":("SX-R-002",R0805,{}), "100k":("SX-R-007",R0805,{}), "4k7":("SX-R-004",R0805,{}), "1k":("SX-R-035",R0805,{}),
 "16k":("SX-R-005",R0805,lcsc("SX-R-005","UNI-ROYAL","0805W8F1602T5E","C17490")), "27k":("SX-R-065",R0805,{}),
 "1M":("SX-R-060",R0805,{}),
 "240k":("SX-R-084",R0805,{}),
 "680k":("SX-R-036",R0805,lcsc("SX-R-036","UNI-ROYAL","0805W8F6803T5E","C17797")), "39k":("SX-R-104",R0805,lcsc("SX-R-104","UNI-ROYAL","0805W8F3902T5E","C25826")),
 # capacitors
 "100n":("SX-C-002",C0805,{}), "100n 100V":("SX-C-013",C0805,{}), "1u":("SX-C-010",C0805,{}), "220n":("SX-C-014",C0805,{}),
 "560p":("SX-C-007",C0805,{}), "100p":("SX-C-008",C0805,{}), "47n":("SX-C-016",C0805,{}), "10p":("SX-C-029","Capacitor_SMD:C_0603_1608Metric",lcsc("SX-C-029","Samsung Electro-Mechanics","CL10C100JB8NNNC","C1634")),
 "4u7 100V":("SX-C-018",C1210,lcsc("SX-C-018","Taiyo Yuden","HMK325C7475KMHPE","C385986")),
 "330u 35V":("SX-C-019","Capacitor_SMD:CP_Elec_10x10.5",lcsc("SX-C-019","Panasonic","EEHZK1V331P","C278516")),
 "100u 35V":("SX-C-020","Capacitor_THT:CP_Radial_D6.3mm_P2.50mm",lcsc("SX-C-020","KNSCHA","KNM2100UF35V149EC0055","C2982822")),
 "100u 50V":("SX-C-028","Capacitor_THT:CP_Radial_D8.0mm_P3.50mm",lcsc("SX-C-028","Nichicon","UHE1H101MPD","C116229")),
 # inductors and fuses
 "2u2":("SX-L-001","Inductor_SMD:L_Bourns_SRP7028A_7.3x6.6mm",lcsc("SX-L-001","Bourns","SRP7028A-2R2M","C1329579")),
 "15u":("SX-L-002","",lcsc("SX-L-002","Bourns","SRP1265A-150M","C189912")),
 "22u":("SX-L-003","",lcsc("SX-L-003","Bourns","SRP1265A-220M","C2041465")),
 "PTC 4A":("SX-F-001","Fuse:Fuse_2920_7451Metric",lcsc("SX-F-001","LUTE","2920L400/30GR","C19078761")),
 "PTC 2A":("SX-F-002","Fuse:Fuse_1812_4532Metric",lcsc("SX-F-002","BHFUSE","BSMD1812-200-33V","C7433877")),
 # semiconductors
 "TPS54560":("SX-IC-018","Package_SO:Texas_R-PDSO-G8_EP2.95x4.9mm_Mask2.4x3.1mm_ThermalVias",lcsc("SX-IC-018","Texas Instruments","TPS54560DDAR","C31966")),
 "74HC14":("SX-IC-019","Package_SO:SOIC-14_3.9x8.7mm_P1.27mm",lcsc("SX-IC-019","Nexperia","74HC14D,653","C5605")),
 "L78M05":("SX-IC-020","Package_TO_SOT_SMD:TO-252-2",lcsc("SX-IC-020","STMicroelectronics","L78M05ABDT-TR","C58069")),
 "SQJ457EP":("SX-Q-002","Package_SO:PowerPAK_SO-8L_Single",lcsc("SX-Q-002","Vishay","SQJ457EP-T1_GE3","C511548")),
 "SMBJ24A":("SX-D-009","Diode_SMD:D_SMB",lcsc("SX-D-009","","SMBJ24A","C19077578")),
 "BZT52C12":("SX-D-010","Diode_SMD:D_SOD-123",lcsc("SX-D-010","","BZT52C12","C19077410")),
 "LED green":("SX-D-011","LED_SMD:LED_0805_2012Metric",lcsc("SX-D-011","","KT-0805G","C2297")),
 "1N4148W":("SX-D-003","Diode_SMD:D_SOD-123",{}),
 "SS54":("SX-D-012","Diode_SMD:D_SMA",lcsc("SX-D-012","MDD","SS54","C22452")),
 "SS510C":("SX-D-013","Diode_SMD:D_SMC",lcsc("SX-D-013","MDD","SS510C","C19229")),
 # connectors and switch
 "KPJX-4S":("SX-CONN-011","",{"ProjectPN":"SX-CONN-011","Manufacturer":"Kycon","MPN":"KPJX-4S","Supplier":"DigiKey","SupplierPN":""}),
 "HDR 2x4":("SX-CONN-008","Connector_IDC:IDC-Header_2x04_P2.54mm_Vertical",{"ProjectPN":"SX-CONN-008","Manufacturer":"Wurth Elektronik","MPN":"61200821621","Supplier":"","SupplierPN":""}),
 "XH 2P":("SX-CONN-016","Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical",lcsc("SX-CONN-016","JST","B2B-XH-A(LF)(SN)","C158012")),
}
def part(key,**extra):
    pn,fp,f=P[key]; d={"ProjectPN":pn}; d.update(f)
    if not fp: d["Note"]="Footprint to draw from the maker's drawing at PCB layout"
    d.update(extra); return fp,d
